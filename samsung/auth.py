import logging
import os

from samsungtvws import SamsungTVWS

# Increase debug level
logging.basicConfig(level=logging.INFO)


def connect(host):
    # Normal constructor
    tv = SamsungTVWS(host=host)

    # Autosave token to file

    token_file = "tv-token.txt"
    tv = SamsungTVWS(host=host, port=8002, token_file=token_file)
    return tv
