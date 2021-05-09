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

from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from web.views import main, create_meeting, join_meeting

urlpatterns = [
    path('admin/', admin.site.urls),
    url('', main, name="home"),
    url('create', create_meeting),
    url(r'^(?P<room_id>[a-z0-9]{1,3}(-[a-z0-9]{1,3})*)$', join_meeting)
]
