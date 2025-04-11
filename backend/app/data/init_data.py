import os
from config import MEDIA_DATA_DIR, SeparatorConfig

def init_directory():
    # common
    common_dir = [MEDIA_DATA_DIR]


    # separator
    separator_dir = [getattr(SeparatorConfig, i) for i in vars(SeparatorConfig) if i.endswith("DIR")]

    dirs = common_dir + separator_dir
    for item in dirs:
        if not os.path.exists(item):
            os.makedirs(item)

