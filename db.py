import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS people (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    age INTEGER NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NULL
)
''')

# create C
cursor.execute('''
INSERT INTO people (name, age, created_at) VALUES ("Anton Loginov", 28, DATE('now'))
''')
connection.commit()

# read R
cursor.execute('''
SELECT * FROM people
''')

rows = cursor.fetchall()
for row in rows:
    print(row)

cursor.execute('''
UPDATE people SET age = 27 WHERE name = "Anton Loginov"
''')
connection.commit()


# read R
cursor.execute('''
SELECT * FROM people
''')

rows = cursor.fetchall()
for row in rows:
    print(row)

cursor.execute('''
DELETE FROM people WHERE id = 1
''')
connection.commit()

# read R
cursor.execute('''
SELECT * FROM people
''')

rows = cursor.fetchall()
if len(rows) == 0:
    print('No data')
else:
    for row in rows:
        print(row)


class Database:
    def __init__(self, database):
        self.connection = sqlite3.connect(database=database)
