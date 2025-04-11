import os.path
from pathlib import Path

import numpy as np
from spleeter import *
from spleeter.audio.adapter import AudioAdapter
from spleeter.separator import Separator
from spleeter.utils import *

from config import APP_DIR, AudioOutputFormat, SeparatorModel
from app.utils.util import output_format_to_ext, is_output_format_lossy

from app.core.log import logger

class SpleeterSeparator:
    """Performs source separation using Spleeter API."""
    def __init__(self, cpu_separation: bool, output_format=AudioOutputFormat.MP3_256, with_piano: bool = False,
                 spleeter_stem=None):
        """Default constructor.
        :param config: Separator config, defaults to None
        """
        self.audio_bitrate = f'{output_format}k' if is_output_format_lossy(
            output_format) else None
        self.audio_format = output_format_to_ext(output_format)
        self.sample_rate = 44100
        if not spleeter_stem:
            self.spleeter_stem = 'data/separators/5stems-16kHz.json' if with_piano else 'data/separators/4stems-16kHz.json'
            self.spleeter_stem = os.path.join(APP_DIR, self.spleeter_stem)
        else:
            self.spleeter_stem = spleeter_stem
        self.separator = Separator(self.spleeter_stem, multiprocess=False)
        self.audio_adapter = AudioAdapter.default()

    def check_and_remove_empty_model_dirs(self):
        model_paths = [
            Path(SeparatorModel.model_path, '4stems'),
            Path(SeparatorModel.model_path, '5stems')
        ]
        for model_path in model_paths:
            if model_path.exists() and not any(model_path.iterdir()):
                model_path.rmdir()

    def create_static_mix(self, parts, input_path, output_path):
        """Creates a static mix by performing source separation and adding the
           parts to be kept into a single track.

        :param parts: List of parts to keep
        :param input_path: Path to source file
        :param output_path: Path to output file
        :raises e: FFMPEG error
        """
        waveform, _ = self.audio_adapter.load(input_path,
                                              sample_rate=self.sample_rate)
        self.check_and_remove_empty_model_dirs()
        prediction = self.separator.separate(waveform, '')
        out = np.zeros_like(prediction['vocals'])

        # Add up parts that were requested
        for key in prediction:
            if parts[key]:
                out += prediction[key]

        self.audio_adapter.save(output_path, out, self.sample_rate,
                                self.audio_format, self.audio_bitrate)

    def separate_into_parts(self, input_path, output_path):
        """Creates a dynamic mix

        :param input_path: Input path
        :param output_path: Output path
        """
        self.check_and_remove_empty_model_dirs()
        self.separator.separate_to_file(input_path,
                                        output_path,
                                        self.audio_adapter,
                                        codec=self.audio_format,
                                        duration=None,
                                        bitrate=self.audio_bitrate,
                                        filename_format='{instrument}.{codec}',
                                        synchronous=False)
        self.separator.join(600)
