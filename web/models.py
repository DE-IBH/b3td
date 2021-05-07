# B3TD - BigBlueButton Test Drive
# Copyright (C) 2020-2021 IBH IT-Service GmbH
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License
# for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

from django.db import models
from django.contrib import admin
from django.utils.crypto import get_random_string
from django.conf import settings
from django.utils import timezone
from uuid import uuid4


def set_default_eol():
    return timezone.now() + timezone.timedelta(minutes=settings.B3TD_MEETING_MAX_LIFETIME)


def set_default_joins():
    return settings.B3TD_MEETING_MAX_JOINS


def set_default_random_room_id():
    allowed_chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
    string_parts = []
    for index in range(0, settings.B3TD_ROOM_ID_LENGTH, 3):
        if index + 3 < settings.B3TD_ROOM_ID_LENGTH:
            string_parts.append(get_random_string(3, allowed_chars))
        else:
            string_parts.append(get_random_string(settings.B3TD_ROOM_ID_LENGTH - index, allowed_chars))
    return "-".join(string_parts)


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


class MeetingAdmin(admin.ModelAdmin):
    model = Meeting
    list_display = ["room_id", "room_name", "status", "end_of_life"]
