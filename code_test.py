import numpy as np
import datetime as dt


def datetime64_to_datetime(time):
    """
    Given a numpy datetime64 array time series, return datetime (y, m, d, h, m, s)
    Code was adapted by Jenni Kyrouac from code developed by Brian Blaylock.
    Parameters
    ----------
    time: numpy datetime64 array
        The numpy array of date time values.
    Returns
    -------
    datetime: list
        Returns a list of datetimes (y, m, d, h, m, s) from a time series.
    References
    ----------
    Brian Blaylock
    GitHub Repository: blaylockbk/convert numpy.datetime to datetime, Sep. 10, 2018.
    https://gist.github.com/blaylockbk/1677b446bc741ee2db3e943ab7e4cabd
    """

    datetime_array = []
    for i in range(0, len(time)):
        timestamp = ((time[i] - np.datetime64('1970-01-01T00:00:00'))
                     / np.timedelta64(1, 's'))
        datetime_format = dt.datetime.utcfromtimestamp(timestamp)
        datetime_array.append(datetime_format)

    return datetime_array
