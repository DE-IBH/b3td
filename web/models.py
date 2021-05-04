from django.db import models
from django.utils.crypto import get_random_string
from django.conf import settings
from django.utils import timezone


def get_random_room_id():
    if settings.B3TD_ROOM_LENGTH % 2 == 1 and settings.B3TD_ROOM_LENGTH > 1:
        string_length = int(settings.B3TD_ROOM_LENGTH / 2)
        return "{}-{}".format(get_random_string(string_length, settings.B3TD_ROOM_ID_ALLOWED_CHARS), get_random_string(string_length, settings.B3TD_ROOM_ID_ALLOWED_CHARS))
    elif settings.B3TD_ROOM_LENGTH > 0:
        return get_random_string(get_random_string(settings.B3TD_ROOM_LENGTH, settings.B3TD_ROOM_ID_ALLOWED_CHARS))


def get_random_pin():
    return get_random_string(settings.B3TD_PIN_LENGTH, settings.B3TD_PIN_ALLOWED_CHARS)


def get_eol():
    return timezone.now() + timezone.timedelta(seconds=settings.B3TD_MEETING_MAX_LIFETIME)


class Meeting(models.Model):
    RUNNING = "running"
    FINISHED = "finished"

    STATUS_CHOICES = [
        (RUNNING, "Meeting is currently running"),
        (FINISHED, "Meeting has been finished")
    ]

    room_id = models.CharField(primary_key=True, max_length=7, default=get_random_room_id)
    meeting_id = models.CharField(max_length=100, null=True)
    pin = models.IntegerField()
    joins = models.SmallIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    end_of_life = models.DateTimeField(default=get_eol, editable=False)
