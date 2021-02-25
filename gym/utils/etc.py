import datetime


def time_stamp():
    return str(datetime.datetime.utcnow()).replace(':', '-').replace('.', '-')
