import os
import uuid
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Integer, Float, Enum, Column, String, Boolean, ForeignKey, Text, DateTime, JSON

from app.base.db import ModelBase
from config import SeparatorConfig

class TaskStatus(Enum):
    QUEUED = 0
    IN_PROGRESS = 1
    DONE = 2
    ERROR = -1


class OutputFormat(Enum):
    WAV = 0
    FLAC = 1
    MP3_192 = 192
    MP3_256 = 256
    MP3_320 = 320


class AudioSeparatorFile(ModelBase):
    __tablename__ = 'audio_separator_files'

    file_name = Column(String(255), nullable=True)
    file_path = Column(String(255), nullable=False)
    duration = Column(Float, nullable=True)
    size = Column(Float, nullable=True, comment="unit KB")
    bitrate = Column(Integer, default=256)

    tracks = relationship('AudioSeparatorTrack', back_populates='audio_file')
    tasks = relationship('AudioSeparatorTask', back_populates='audio_file')


class AudioSeparatorTrack(ModelBase):
    __tablename__ = 'audio_separator_tracks'

    audio_file_id = Column(String(36), ForeignKey('audio_separator_files.id'), nullable=False)
    task_id = Column(String(36), ForeignKey('audio_separator_tasks.id'), nullable=True)

    audio_file = relationship('AudioSeparatorFile', back_populates='tracks')
    task = relationship('AudioSeparatorTask', back_populates='tracks')


class AudioSeparatorTask(ModelBase):
    __tablename__ = 'audio_separator_tasks'

    task_uuid = Column(String(255), nullable=True, index=True)
    status = Column(Integer, default=0)  # 默认状态为 QUEUED
    audio_file_id = Column(String(36), ForeignKey('audio_separator_files.id'), nullable=False)
    separator = Column(String(20), default='Spleeter')
    separator_args = Column(JSON, default=dict)
    bitrate = Column(Integer, default=256)  # 默认比特率为 256kbps
    vocals = Column(Boolean, default=False)
    drums = Column(Boolean, default=False)
    bass = Column(Boolean, default=False)
    other = Column(Boolean, default=False)
    piano = Column(Boolean, default=False)
    error = Column(Text, nullable=True)
    start_time = Column(DateTime, nullable=True)
    finish_time = Column(DateTime, nullable=True)

    audio_file = relationship('AudioSeparatorFile', back_populates='tasks')
    tracks = relationship('AudioSeparatorTrack', back_populates='task')

    def formatted_name(self):
        return str(uuid.uuid4())

    def tracks_dir(self):
        return os.path.join(SeparatorConfig.TRACK_DIR, str(self.id))

    def tracks_path(self, filename=f'{str(uuid.uuid4())}.mp3'):
        return os.path.join(self.tracks_dir(), filename)

    def source_path(self):
        return os.path.join(SeparatorConfig.UPLOAD_DIR, self.audio_file.file_path)

