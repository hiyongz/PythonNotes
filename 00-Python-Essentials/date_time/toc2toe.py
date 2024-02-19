

import datetime


def toc2toe():
    d1 = '2024-02-19 20:29:00'
    date1 = datetime.datetime.strptime(d1, "%Y-%m-%d %H:%M:%S")  ##datetime.date(2018, 1, 6)
    weekday = date1.weekday() + 1
    toe = weekday * 24 * 3600 + date1.hour * 3600 + date1.minute * 60 + date1.second
    print(toe)


toc2toe()