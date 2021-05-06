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
