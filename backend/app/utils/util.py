import re
import datetime
import aiofiles
from fastapi import UploadFile

from config import AudioOutputFormat

ALL_PARTS = ['vocals', 'other', 'bass', 'drums']
ALL_PARTS_5 = ['vocals', 'other', 'piano', 'bass', 'drums']

def current_strftime(fmt="%Y-%m-%d %H:%M:%S"):
    return datetime.datetime.now().strftime(fmt)

def get_valid_filename(s):
    """
    Return the given string converted to a string that can be used for a clean
    filename. Remove leading and trailing spaces; remove anything that is not an
    alphanumeric, dash, whitespace, comma, bracket, underscore, or dot.
    >>> get_valid_filename("john's portrait in 2004.jpg")
    'johns_portrait_in_2004.jpg'
    """
    s = str(s).strip()
    return re.sub(r'(?u)[^-\w\s.,[\]()]', '', s)

def is_output_format_lossy(output_format: int):
    """Return whether OutputFormat enum is a lossy format."""
    return output_format != AudioOutputFormat.FLAC and output_format != AudioOutputFormat.WAV

def output_format_to_ext(output_format: int):
    """Resolve OutputFormat enum to a file extension."""
    if output_format == AudioOutputFormat.FLAC:
        return 'flac'
    elif output_format == AudioOutputFormat.WAV:
        return 'wav'
    else:
        return 'mp3'

async def write_file(file: UploadFile, save_path: str) -> None:
    async with aiofiles.open(save_path, "wb") as buffer:
        chunk = await file.read()
        await buffer.write(chunk)