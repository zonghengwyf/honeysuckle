import subprocess
from pydub import AudioSegment
from logger import logger


def get_audio_duration(file_path: str) -> float:
    """
    获取音频文件的时长（以秒为单位）。

    :param file_path: 音频文件的路径（支持 MP3、WAV 等格式）
    :return: 音频时长（秒）
    """
    try:
        # 加载音频文件
        audio = AudioSegment.from_file(file_path)

        # 获取音频时长（以毫秒为单位）
        duration_in_ms = len(audio)

        # 转换为秒
        duration_in_seconds = duration_in_ms / 1000

        return duration_in_seconds
    except Exception as e:
        logger.exception(f"无法读取音频文件 {file_path}: {e}")
        return 0



def get_audio_bitrate(file_path: str) -> int:
    """
    获取音频文件的比特率（以 kbps 为单位）。

    :param file_path: 音频文件的路径（支持 MP3、WAV 等格式）
    :return: 音频比特率（kbps），如果无法获取则返回 -1
    """
    try:
        # 使用 ffmpeg 获取音频文件信息
        command = [
            "ffmpeg", "-i", file_path
        ]
        result = subprocess.run(command, stderr=subprocess.PIPE, text=True)

        # 从输出中解析比特率
        for line in result.stderr.splitlines():
            if "bitrate:" in line:
                bitrate_info = line.split("bitrate:")[1].strip()
                if "kb/s" in bitrate_info:
                    bitrate = int(bitrate_info.split("kb/s")[0].strip())
                    return bitrate
        return -1  # 如果未找到比特率信息
    except Exception as e:
        logger.exception(f"无法获取音频文件 {file_path} 的比特率: {e}")
        return -1