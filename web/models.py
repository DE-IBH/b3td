from django.db import models
from django.utils.crypto import get_random_string
from django.conf import settings
from django.utils import timezone
from uuid import uuid4


def set_default_eol():
    return timezone.now() + timezone.timedelta(minutes=settings.B3TD_MEETING_MAX_LIFETIME)


def set_default_joins():
    return settings.B3TD_MEETING_MAX_JOINS


def set_default_random_room_id():
    if settings.B3TD_ROOM_ID_LENGTH % 2 == 1 and settings.B3TD_ROOM_ID_LENGTH > 1:
        string_length = int(settings.B3TD_ROOM_ID_LENGTH / 2)
        return "{}-{}".format(get_random_string(string_length, settings.B3TD_ROOM_ID_ALLOWED_CHARS), get_random_string(string_length, settings.B3TD_ROOM_ID_ALLOWED_CHARS))
    elif settings.B3TD_ROOM_ID_LENGTH > 0:
        return get_random_string(get_random_string(settings.B3TD_ROOM_ID_LENGTH, settings.B3TD_ROOM_ID_ALLOWED_CHARS))


def set_default_random_room_name():
    return "Meeting {}".format(timezone.now().strftime("%Y%m%d%H%M%S"))


def set_default_random_pin():
    return get_random_string(settings.B3TD_PIN_LENGTH, settings.B3TD_PIN_ALLOWED_CHARS)


class Meeting(models.Model):
    RUNNING = "running"
    FINISHED = "finished"

    STATUS_CHOICES = [
        (RUNNING, "Meeting is currently running"),
        (FINISHED, "Meeting has been finished")
    ]

    room_id = models.CharField(primary_key=True, max_length=7, default=set_default_random_room_id)
    meeting_id = models.UUIDField(default=uuid4)
    room_name = models.CharField(max_length=100, default=set_default_random_room_name)
    pin = models.IntegerField(default=set_default_random_pin)
    joins = models.SmallIntegerField(default=set_default_joins)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=RUNNING)
    end_of_life = models.DateTimeField(default=set_default_eol, editable=False)

    @property
    def room_url(self):
        return "{}{}".format(settings.B3TD_BASE_URL, self.room_id)
