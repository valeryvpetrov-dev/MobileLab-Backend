import datetime

datetime_str_format = "%Y-%m-%dT%H:%M:%S.%fZ"


def dt2str(dt: datetime) -> str:
    return datetime.datetime.strftime(dt, datetime_str_format)


def str2dt(dt_str: str) -> datetime:
    return datetime.datetime.strptime(dt_str, datetime_str_format).replace(tzinfo=datetime.timezone.utc)
