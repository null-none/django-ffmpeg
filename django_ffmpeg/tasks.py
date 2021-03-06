import logging

from celery.task import task

from django_ffmpeg.models import (
    Video, ConvertingCommand,
    VIDEO_CONVERSION_STATUS_CHOICES as STATUSES
)
from django_ffmpeg.utils import Converter


logger = logging.getLogger(__name__)


@task(time_limit=7200)
def convert_video(command_id, video_id):
    command = ConvertingCommand.objects.get(pk=command_id)
    video = Video.objects.get(pk=video_id)
    started = STATUSES[1][0]
    if video.convert_status in [started]:
        logger.error('Video #{} already converting'.format(video_id))
        return
    converter = Converter()
    converter.convert_video_thumb(command, video)
    converter.convert_video_file(command, video)


@task(time_limit=7200) # replace this to settings
def convert_first_pending():
    Converter().convert_first_pending()
