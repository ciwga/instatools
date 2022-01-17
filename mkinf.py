import hashlib
import os
from datetime import datetime


def sha256(filename):

    if os.path.isfile(filename) is False:
        pass

    BLOCK_SIZE = 65536
    f_sha256 = hashlib.sha256()
    try:
        with open(filename, 'rb') as f:

            byte = f.read(BLOCK_SIZE)
            f_sha256.update(byte)
    except FileNotFoundError:
        pass

    return f_sha256.hexdigest()


def timestamp():
    return datetime.timestamp(datetime.now())


def timestamp2date(timestmp=timestamp()):
    return datetime.fromtimestamp(timestmp)
