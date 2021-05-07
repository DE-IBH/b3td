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

from urllib.parse import urlencode
import hashlib

# symbols not to be encoded to match bbb's checksum calculation
SAFE_QUOTE_SYMBOLS = '*'


def get_endpoint_str(endpoint, params, secret):
    parameter_str = ""

    if params:
        parameter_str = urlencode(params, safe=SAFE_QUOTE_SYMBOLS)

    sha_1 = hashlib.sha1()
    sha_1.update("{}{}{}".format(endpoint, parameter_str, secret).encode())

    if params:
        return "{}?{}&checksum={}".format(endpoint, parameter_str, sha_1.hexdigest())
    else:
        return "{}?checksum={}".format(endpoint, sha_1.hexdigest())
