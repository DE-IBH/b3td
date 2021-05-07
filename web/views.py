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
import datetime

from django.shortcuts import render
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from web.models import Meeting
import web.b3td.utils as utils
import requests as rq


# Create your views here.
def main(request):
    content = {
        "title": settings.B3TD_HTML_TITLE,
        "base_url": settings.B3TD_BASE_URL
    }
    return render(request, "web/main.html", content)


def create_meeting(request):
    if Meeting.objects.filter(status=Meeting.RUNNING).count() < settings.B3TD_MEETING_MAX_MEETINGS:
        meeting = Meeting()
        meeting.save()
        params = {
            "meetingID": meeting.meeting_id,
            "name": meeting.room_name,
            "duration":  settings.B3TD_MEETING_MAX_LIFETIME,
            "breakoutRoomsEnabled": "false",
            "bannerText": settings.B3TD_MEETING_BANNER_TEXT,
            "attendeePW": meeting.pin,
            "welcome": """Welcome to BBB '%%CONFNAME%%'.

To invite other users share the following URL and PIN:

    URL: {}
    PIN: {}

The maximum number of possible joins of other users for this meeting is: {}

You can also invite others via phone by sharing the following phone number and PIN:

    TEL: %%DIALNUM%%
    PIN: %%CONFNUM%%
""".format(meeting.room_url, settings.B3TD_MEETING_MAX_JOINS, meeting.pin)
        }
        url = "{}{}".format(settings.B3TD_BBB_API_BASE_DOMAIN, utils.get_endpoint_str("create", params, settings.B3TD_BBB_SECRET))
        response = rq.get(url)

        url = "{}{}".format(settings.B3TD_BASE_URL, meeting.room_url)

        return HttpResponseRedirect(url)

    else:
        content = {
            "titel": settings.B3TD_HTML_TITLE,
            "body_text": settings.B3TD_HTML_TEXT_NO_MEETINGS
        }
        return render(request, "web/error.html", content)


def join_meeting(request, room_id=""):
    try:
        meeting = Meeting.objects.get(room_id=room_id)
    except ObjectDoesNotExist:
        return HttpResponse("Not Found", status=404)

    if timezone.now() > meeting.end_of_life or meeting.status == meeting.FINISHED:
        content = {
            "titel": settings.B3TD_HTML_TITLE,
            "body_text": "The meeting you try to join has ended!"
        }
        return render(request, "web/error.html", content)

    if meeting.joins == 0:
        content = {
            "titel": settings.B3TD_HTML_TITLE,
            "body_text": "The meeting's join capacity is exhausted!"
        }
        return render(request, "web/error.html", content)

    params = {
        "fullName": "Attendee {}".format(settings.B3TD_MEETING_MAX_JOINS - meeting.joins + 1),
        "meetingID": meeting.meeting_id,
        "password": meeting.pin,
        "joinViaHtml5": "true"
    }

    with transaction.atomic():
        Meeting.objects.update(room_id=room_id, defaults={"joins": meeting.joins - 1})

    url = "{}{}".format(settings.B3TD_BBB_API_BASE_DOMAIN, utils.get_endpoint_str("join", params, settings.B3TD_BBB_SECRET))

    return HttpResponseRedirect(url)
