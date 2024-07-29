from datetime import datetime, timedelta
import sqlite3


def run():
    for scheme in ["new_", "old_", "sn_"]:
        for hour in range(10,16):

            sql = """\
            SELECT name, round(avg(value), 3) as avg_value,\
            datetime("now", "localtime", "start of day", "+%s hour") as hour, scheme FROM
            (SELECT * FROM vkt_data WHERE timestamp > datetime("now", "localtime", "start of day")\
            AND timestamp < datetime("now", "localtime", "start of day", "+%s hour")\
            AND scheme = '%s' AND quality = "Good" ORDER by name)
            GROUP by name;"""%(str(hour), str(hour), scheme)

            cursor.execute(sql)
            result = cursor.fetchall()

            for el in result:
                name, value, hourr, schemee = el
                # cursor.execute("INSERT INTO avg_hour (name, value, hour, scheme) VALUES (?,?,?,?)",el)
                print name, value, hourr
                # print len(el)
            print "-"*100



# connection = sqlite3.connect('vkt.db')
# cursor = connection.cursor()
# run()
# connection.commit()
# cursor.close()

from_string = "26 Nov 2019 17:11:17.000"
to_string = "27 Nov 2019 23:59:59.000"
from_time = datetime.strptime(from_string, "%d %b %Y  %H:%M:%S.%f")
to_time = datetime.strptime(to_string, "%d %b %Y  %H:%M:%S.%f")

def split_time(from_time, to_time):

    print from_time
    print to_time
    difference = to_time - from_time
    print "difference is:", difference

    minutes = timedelta(minutes=from_time.minute)
    seconds = timedelta(seconds=from_time.second)
    first_delta = timedelta(hours=1) if (seconds == 0 or minutes == 0) else timedelta(hours=1) - seconds - minutes
    hour = timedelta(hours=1)
    print "to whole hour delta:", first_delta
    print "minutes delta:",minutes
    print "seconds delta:",seconds

    whole_from_time = from_time + first_delta
    print "whole from time:", whole_from_time
    whole_time = whole_from_time

    print "-"*100
    print from_time
    delta = timedelta()

    while delta < difference - first_delta:
        print whole_time
        whole_time += hour
        delta += hour
    print from_time + difference


split_time(from_time, to_time)