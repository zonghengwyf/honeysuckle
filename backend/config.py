import os


CPU_SEPARATION = os.getenv('CPU_SEPARATION', '1') == '1'

PROJECT_DIR = os.getenv("PROJECT_DIR") or "/opt/honeysuckle"
BACKEND_DIR = os.path.join(PROJECT_DIR, "backend")
APP_DIR = os.path.join(BACKEND_DIR, "app")
API_DIR = os.path.join(APP_DIR, "api")
DATA_DIR = os.getenv("DATA_DIR") or "/var/data"
MEDIA_DATA_DIR = os.path.join(DATA_DIR, "media")

class DbConfig:
    DB_HOST = '192.168.0.4'
    DB_PORT = 3306
    DB_USER = 'honeysuckle'
    DB_PASS = 'honeysuckle123'
    DB_NAME = 'honeysuckle_db'
    DB_CHARSET = 'utf8mb4'
    DB_APT_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(DB_USER, DB_PASS, 'mysql', DB_PORT, DB_NAME)

class SeparatorConfig:
    SPLEETER = 'spleeter'
    SPLEETER_PIANO = 'spleeter_5stems'
    D3NET = 'd3net'
    XUMX = 'xumx'

    DEMUCS4_HT = 'htdemucs'
    DEMUCS4_HT_FT = 'htdemucs_ft'
    DEMUCS3_MMI = 'hdemucs_mmi'
    DEMUCS3_MDX = 'mdx'
    DEMUCS3_MDX_EXTRA = 'mdx_extra'
    DEMUCS3_MDX_Q = 'mdx_q'
    DEMUCS3_MDX_EXTRA_Q = 'mdx_extra_q'

    # Deprecated
    DEMUCS = 'demucs'
    DEMUCS_HQ = 'demucs48_hq'
    DEMUCS_EXTRA = 'demucs_extra'
    DEMUCS_QUANTIZED = 'demucs_quantized'
    TASNET = 'tasnet'
    TASNET_EXTRA = 'tasnet_extra'
    DEMUCS_LIGHT = 'light'
    DEMUCS_LIGHT_EXTRA = 'light_extra'

    DEMUCS_FAMILY = [
        DEMUCS4_HT, DEMUCS4_HT_FT, DEMUCS3_MMI,
        DEMUCS3_MDX, DEMUCS3_MDX_EXTRA, DEMUCS3_MDX_Q, DEMUCS3_MDX_EXTRA_Q,
        DEMUCS, DEMUCS_HQ, DEMUCS_EXTRA, DEMUCS_QUANTIZED, TASNET, TASNET_EXTRA,
        DEMUCS_LIGHT, DEMUCS_LIGHT_EXTRA
    ]

    UPLOAD_DIR = os.path.join(MEDIA_DATA_DIR, "audio/separator/uploads")
    TRACK_DIR = os.path.join(MEDIA_DATA_DIR, "audio/separator/tracks")

    AUDIO_SIZE_LIMIT = 10*1024*1024

class SeparatorModel:
    model_path = "/var/model"


class ApiConfig:
    pass

class AudioOutputFormat:
    """
    输出格式的常量类。
    """
    WAV = 0
    FLAC = 1
    MP3_192 = 192
    MP3_256 = 256
    MP3_320 = 320