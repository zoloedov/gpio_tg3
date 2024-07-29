import os
import sys
import sqlite3

connection1 = sqlite3.connect("vkt_big.db")
cursor1 = connection1.cursor()
cursor1.execute("""SELECT name, value, timestamp, quality, test, report_order, scheme FROM vkt_data --WHERE timestamp >= datetime("now", "localtime", "start of day")""")
result = cursor1.fetchall()

connection2 = sqlite3.connect("vkt_basic.db")
cursor2 = connection2.cursor()

print len(result)
for el in result:

    average_query = "INSERT INTO vkt_data (name,\
                                           value,\
                                           timestamp,\
                                           quality,\
                                           test,\
                                           report_order,\
                                           scheme)\
                    VALUES ('%s','%s','%s', '%s', '%s', '%s', '%s');"%el
    cursor2.execute(average_query)

connection2.commit()
connection2.close()
connection1.close()
print "done..."