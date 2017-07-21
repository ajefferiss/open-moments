Date: 2017-06-30 14:35
Title: Python and SQLite
Description: Introduction to SQLite and Python
Tags: sqlite tutorial sql python
Slug: python_sqlite_intro

[TOC]

### Before you begin
Afte a quick introduction to connecting to the database and managing the schema this page is going to expand upon the contacts database from the [Introduction to SQLite]({filename}/tech/sqlite_intro.md) so have a read of that before continuing. This introduction also assumes a basic understanding on [Python](https://www.python.org/), and make use of the [sqlite3](https://docs.python.org/3/library/sqlite3.html) module.

### Connect to the database
After importing the `sqlite3` module you can connect to the database by using the `connect` call, this [method](https://docs.python.org/3/library/sqlite3.html#sqlite3.connect) has a number of optional arguments; but in the most basic for you need to provide the path to the database file to open. If you want to use a in memory database, you can use `:memory:` as the argument to connect:

```python
db = sqlite3.connect("/path/to/file.db")
db = sqlite3.connect(":memory:")
```

Once you have finished working with the database you need to make sure the connection is closed: `db.close()`

### Schema changes
The schema can be [created](http://www.sqlite.org/lang_createtable.html), and [altered](http://www.sqlite.org/lang_altertable.html) using both the `CREATE TABLE` and `ALTER TABLE` statements. If you're unsure whether or not the table exists within a database being loaded; you can make use of `CREATE TABLE IF NOT EXISTS`. The `ALTER` statement in sqlite3 [omits](http://www.sqlite.org/omitted.html) support for certain operations so you can only rename tables and add columns. For more complex operations the suggestion is to create a new table with the correct requirements and then copy the data into it and `DROP` the old table. You can then rename the new table if required.

```python
import sqlite3

db = sqlite3.connect("my_database.db")
cursor = db.cursor()

cursor.execute('CREATE TABLE contact IF NOT EXISTS(id INTEGER, firstname TEXT, family_name TEXT)')
cursor.execute('ALTER TABLE contact ADD COLUMN title TEXT')

db.commit()
db.close()
```
