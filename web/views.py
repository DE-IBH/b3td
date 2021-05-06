from django.shortcuts import render
from django.conf import settings
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
    else:
        content = {
            "titel": settings.B3TD_HTML_TITLE,
            "body_text": settings.B3TD_HTML_TEXT_NO_MEETINGS
        }
        return render(request, "web/error.html", content)


def join_meeting():
    return 0
