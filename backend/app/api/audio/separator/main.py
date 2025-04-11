import os.path
import shutil
from datetime import datetime
from app.base.db import DbBase

from logger import logger
from .models import AudioSeparatorTask, AudioSeparatorTrack, AudioSeparatorFile

class SeparatorCRUD:
    def __init__(self, db=DbBase()):
        self.db = db

    def separator_task_list(self):
        r = self.db.session.query(AudioSeparatorTask.id,
                              AudioSeparatorTask.task_uuid,
                              AudioSeparatorTask.status,
                              AudioSeparatorTask.separator,
                              AudioSeparatorTask.separator_args,
                              AudioSeparatorTask.bitrate,
                              AudioSeparatorTask.create_time,
                              AudioSeparatorTask.update_time,
                              AudioSeparatorTask.start_time,
                              AudioSeparatorTask.finish_time,
                              AudioSeparatorTask.error,
                              AudioSeparatorTask.audio_file_id,
                              AudioSeparatorFile.file_name,
                              AudioSeparatorFile.size.label('file_size')).join(
                              AudioSeparatorFile,
                              AudioSeparatorTask.audio_file_id==AudioSeparatorFile.id
                              ).all()
        data = []
        for item in r:
            row = item._asdict()
            row = {k: v.strftime("%Y-%m-%d %H:%M:%S") if isinstance(v, datetime) else v for  k, v in row.items()}
            data.append(row)
        return True, data

    def delete_separator_voice(self, task_id):
        try:
            task_r = self.db.get(AudioSeparatorTask, task_id)
            if not task_r:
                return False, "删除音频不存在"
            source_file = task_r.source_path()
            track_dir = task_r.tracks_dir()
            source_file_id = task_r.audio_file_id

            if os.path.exists(track_dir):
                shutil.rmtree(track_dir)
            task_all_track = self.db.session.query(AudioSeparatorTrack.audio_file_id).filter(
                AudioSeparatorTrack.task_id == task_id).all()
            track_file_ids = [item.audio_file_id for item in task_all_track]
            self.db.session.query(AudioSeparatorTrack).filter(AudioSeparatorTrack.task_id == task_id).delete()
            self.db.session.query(AudioSeparatorTask).filter(AudioSeparatorTask.id == task_id).delete()
            if track_file_ids:
                self.db.session.query(AudioSeparatorFile).filter(AudioSeparatorFile.id.in_(track_file_ids)).delete()

            file_r = self.db.get(AudioSeparatorFile, source_file_id)
            if os.path.exists(source_file):
                os.remove(source_file)
            if file_r:
                self.db.session.query(AudioSeparatorFile).filter(AudioSeparatorFile.id == source_file_id).delete()
            self.db.session.commit()
            return True, "删除音频成功"
        except Exception as err:
            logger.exception(err)
            self.db.session.rollback()
            return False, "删除音频失败"

    def get_tracks_by_task(self, task_id):
        r = self.db.session.query(AudioSeparatorTrack.id,
                                  AudioSeparatorFile.file_name,
                                  AudioSeparatorFile.size.label('file_size'),
                                  AudioSeparatorFile.id.label('file_id')
                                  ).join(
                                  AudioSeparatorFile,
                                  AudioSeparatorTrack.audio_file_id == AudioSeparatorFile.id
                                ).filter(AudioSeparatorTrack.task_id==task_id).all()
        data = []
        for item in r:
            row = item._asdict()
            row = {k: v.strftime("%Y-%m-%d %H:%M:%S") if isinstance(v, datetime) else v for k, v in row.items()}
            data.append(row)
        return True, data

    def get_file_by_id(self, file_id):
        r = self.db.session.query(AudioSeparatorFile).filter(AudioSeparatorFile.id == file_id).first()
        return r