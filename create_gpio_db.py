import sqlite3

connection = sqlite3.connect('gpio_.db')
cursor = connection.cursor()
cursor.execute('DROP TABLE IF EXISTS gpio_data')
cursor.execute('CREATE TABLE gpio_data (id INTEGER PRIMARY KEY AUTOINCREMENT,\
	channel TEXT, value REAL, timestamp DATETIME, pin TEXT, pin_scheme TEXT, test BOOL)')
cursor.execute('CREATE unique INDEX time_and_id ON gpio_data(timestamp ASC, id)')
connection.close()
