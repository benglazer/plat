import datetime

from tzlocal import get_localzone


def has_timezone(dt):
    """Return true if dt has a timezone, false otherwise."""
    return dt.tzinfo is not None and dt.tzinfo.utcoffset(dt) is not None


def apply_local_timezone(dt):
    """Set dt's timezone to the computer's local timezone."""
    return get_localzone().localize(dt)


def now_local_timezone():
    """Return the current time in the computer's local timezone."""
    return datetime.datetime.now(get_localzone())


def strip_seconds(dt):
    """Return the floor of the datetime to the nearest minute."""
    return dt + datetime.timedelta(seconds=-dt.second,
                                   microseconds=-dt.microsecond)
