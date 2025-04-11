import os
import os.path
import pathlib
import shutil
from typing import Dict, List
import traceback
from sqlalchemy.orm import Session

from billiard.context import Process
from billiard.exceptions import SoftTimeLimitExceeded

from logger import setup_logger
from app.celery_worker import celery_app
from app.base.db import DbBase
from app.api.audio.separator.models import AudioSeparatorFile, AudioSeparatorTrack, AudioSeparatorTask, TaskStatus
# from app.core.separators.d3net_separator import D3NetSeparator
# from app.core.separators.demucs_separator import DemucsSeparator
from app.core.separators.spleeter_separator import SpleeterSeparator
# from app.core.separators.x_umx_separator import XUMXSeparator
from app.utils.util import ALL_PARTS, ALL_PARTS_5, output_format_to_ext, get_valid_filename
from app.utils.util import current_strftime
from app.utils.audio_util import get_audio_duration
from config import SeparatorConfig, CPU_SEPARATION

celery_logger = setup_logger("celery", "separator_celery.log")

def get_separator(separator: str, separator_args: Dict, bitrate: int, cpu_separation: bool):
    """Returns separator object for corresponding source separation model."""
    if separator.lower() == SeparatorConfig.SPLEETER.lower():
        return SpleeterSeparator(cpu_separation, bitrate, False)
    # elif separator == SeparatorConfig.SPLEETER_PIANO:
    #     return SpleeterSeparator(cpu_separation, bitrate, True)
    # elif separator == SeparatorConfig.D3NET:
    #     return D3NetSeparator(cpu_separation, bitrate)
    # elif separator == SeparatorConfig.XUMX:
    #     softmask = separator_args['softmask']
    #     alpha = separator_args['alpha']
    #     iterations = separator_args['iterations']
    #     return XUMXSeparator(cpu_separation, bitrate, softmask, alpha, iterations)
    # else:
    #     random_shifts = separator_args['random_shifts']
    #     return DemucsSeparator(separator, cpu_separation, bitrate,
    #                            random_shifts)

@celery_app.task()
def create_separator_voices(task_id: int):
    db = DbBase()
    task = db.get(AudioSeparatorTask, task_id)
    if not task:
        return False, "任务不存在"

    task.status = TaskStatus.IN_PROGRESS
    db.update(task)

    ext = output_format_to_ext(task.bitrate)

    try:
        # Get paths
        rel_path_dir  = task.tracks_dir()
        filename = get_valid_filename(task.formatted_name()) + f'.{ext}'
        rel_path = task.tracks_path(filename)
        pathlib.Path(rel_path_dir).mkdir(parents=True, exist_ok=True)
        separator = get_separator(task.separator,
                                  task.separator_args,
                                  task.bitrate,
                                  CPU_SEPARATION)

        parts = {
            'vocals': task.vocals,
            'drums': task.drums,
            'bass': task.bass,
            'other': task.other
        }
        if task.separator == SeparatorConfig.SPLEETER_PIANO:
            parts['piano'] = task.piano

        path = task.source_path()

        if not CPU_SEPARATION:
            # For GPU separation, do separation in separate process.
            # Otherwise, GPU memory is not automatically freed afterwards
            process_eval = Process(target=separator.create_static_mix,
                                   args=(parts, path, rel_path))
            process_eval.start()
            try:
                process_eval.join()
            except SoftTimeLimitExceeded as e:
                # Kill process if user aborts task
                process_eval.terminate()
                raise e
        else:
            separator.create_static_mix(parts, path, rel_path)

        # Check file exists
        if os.path.exists(rel_path):
            task.status = TaskStatus.DONE
            task.finish_time = current_strftime()
            db.update(task)
            db.add(AudioSeparatorFile, {"file_name": filename, "file_path": rel_path,
                                        "size": os.path.getsize(rel_path),
                                        "duration": get_audio_duration(rel_path)}, False, False)
            db.add(AudioSeparatorTrack, {"audio_file_id": task.audio_file_id, "task_id": task.id})
        else:
            raise Exception('Error writing to file')
    except FileNotFoundError as error:
        celery_logger.error(f'Please make sure you have FFmpeg and FFprobe installed, {error}')
        task.status = TaskStatus.ERROR
        task.finish_time = current_strftime()
        task.error = str(error)
        db.update(task)
    except SoftTimeLimitExceeded:
        celery_logger.error('Aborted!')
    except Exception as error:
        celery_logger.exception(error)
        task.status = TaskStatus.ERROR
        task.finish_time = current_strftime()
        task.error = str(error)
        db.update(task)

