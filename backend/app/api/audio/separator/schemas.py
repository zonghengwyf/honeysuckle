from pydantic import BaseModel, conint, constr, validator, ValidationError
from typing import Optional, List, Dict, Any
from datetime import datetime

class SourceFileBase(BaseModel):
    file: str

class SourceFileCreate(SourceFileBase):
    pass

class SourceTrackBase(BaseModel):
    artist: str
    title: str

class SourceTrackCreate(SourceTrackBase):
    source_file_id: int

class StaticMixBase(BaseModel):
    separator: Optional[str] = 'Spleeter'
    separator_args: Optional[Dict[str, Any]] = {}
    bitrate: Optional[conint(ge=0)] = 256  # 比特率，必须为正整数
    source_track_id: int
    vocals: Optional[bool] = False
    drums: Optional[bool] = False
    bass: Optional[bool] = False
    other: Optional[bool] = False
    piano: Optional[bool] = None

    @validator('separator')
    def separator_validator(cls, v):
        if not v:
            raise ValueError('separator不能为空')
        return v

class StaticMixCreate(StaticMixBase):
    pass

class StaticMixList(StaticMixBase):
    pass

class DynamicMixBase(BaseModel):
    separator: Optional[str] = 'Spleeter'
    separator_args: Optional[Dict[str, Any]] = {}
    bitrate: Optional[conint(ge=0)] = 256
    source_track_id: int
    vocals_file: Optional[str]
    other_file: Optional[str]
    piano_file: Optional[str]
    bass_file: Optional[str]
    drums_file: Optional[str]

class DynamicMixCreate(DynamicMixBase):
    pass

class SourceFile(SourceFileBase):
    id: int
    class Config:
        from_attributes = True

class SourceTrack(SourceTrackBase):
    id: int
    date_created: datetime

    class Config:
        from_attributes = True

class StaticMix(StaticMixBase):
    id: int
    celery_id: str
    status: int
    date_created: datetime
    date_finished: Optional[datetime]

    class Config:
        from_attributes = True

class DynamicMix(DynamicMixBase):
    id: int
    celery_id: str
    status: int
    date_created: datetime
    date_finished: Optional[datetime]

    class Config:
        from_attributes = True