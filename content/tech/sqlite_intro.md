Date: 2017-06-20 08:35
Title: Introduction to SQLite
Description: Straight forward introduction to SQLite to build a contacts database.
Tags: sqlite tutorial sql
Slug: sqlite_intro

[TOC]

### What Is SQLite?
[SQLite](https://www.sqlite.org) is a self-contained [SQL](https://en.wikipedia.org/wiki/SQL) database engine. This means that an application is able to make use of all of the benefits of a [rational database](https://en.wikipedia.org/wiki/Relational_database_management_system) without needing to provide additional server installations like [PostgreSQL](https://www.postgresql.org/) or Microsofts [SQL Server](https://www.microsoft.com/en-us/sql-server). This means that you are easily able to share the database between multiple operating systems, and architectures (32/64 bit) simply by coping the file on to the target machine. As with all things; there are [appropriate uses of SQLite](https://sqlite.org/whentouse.html), which are many, there are also times when a client/server rational database management system may work better.

Much of this page however; will cover [SQL](https://en.wikipedia.org/wiki/SQL) in general and be appropriate for any system.

### What will we do?
As a introduction to SQLite we'll make use of [SQLite Browser](http://sqlitebrowser.org/) to create a contacts database which we'll add some test contacts too. This page will focus on using SQL directly to create the tables, and information stored in them. However all of this can be done, one way or another by using the SQLite Browser UI. All of the following will be done within the 'Execute SQL' tab, with the exception of creating the database file itself.

### Creating the database
Within [SQLite Browser](http://sqlitebrowser.org/) you need to choose the "New Database" option, doing so will open a save dialogue. This will be the location on disk that the contacts database file gets stored; choose any location and name the file `contacts.db`. Once you have chosen the file location you'll be prompted to create a new table, cancel this for the time being and then select the 'Execute SQL' tab.

### Creating tables
Each database is made up of one, or more, tables while a table is a set of data elements. The data stored within a table is stored in rows, each row is made up a selection of values, columns. Each of the columns will have an associated data type, which get defined while creating the table and is known as the [schema](https://en.wikipedia.org/wiki/Database_schema). SQLite has a number of available [data types](https://www.sqlite.org/datatype3.html).

The SQL `CREATE TABLE` statement is used to create a new table. Creating a table involves naming the table and then defining the column names and data types. As an example, to create a table called `contacts` which stores a first name and family name we'd run:

```sql
CREATE TABLE "contacts" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "firstname" TEXT NOT NULL,
    "family_name" TEXT
);
```

This will create a new table with 3 columns:

* id - The ID is used as a unique identifier for the table; each time we create a entry in the table it will automatically create a unique [integer](https://en.wikipedia.org/wiki/Integer) value and store it in the column. This column will allow us to link tables together

* firstname - A text column that must have a value, here we're saying that each of our contacts must at least have a first name.

* family_name - A optional text column for a family name.

The final two tables we're creating will look very similar and can be created with the following statements:

```sql
CREATE TABLE "numbers" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "number" TEXT NOT NULL,
    "contact_id" INTEGER NOT NULL,
    FOREIGN KEY("contact_id") REFERENCES contacts("id") ON DELETE CASCADE
);
CREATE TABLE "email_addresses" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "address" TEXT NOT NULL,
    "contact_id" INTEGER NOT NULL,
    FOREIGN KEY("contact_id") REFERENCES contacts("id") ON DELETE CASCADE
);
```

These statements will create two tables `numbers` and `email_addresses`. The numbers table will be used to store all telephone numbers associated with a contact. You may notice that we're storing numbers in a `TEXT` field instead of a `INTEGER` or `NUMBER`, while this might seem a little strange at first there is a good reason for it. Both `INTEGER` and `NUMERIC` fields are designed to store a particular type of number (1, or 1.0 for example). Phone numbers are a little more tricky, if we wanted to store a international dialling code for example we'd need to do so in a separate column. Telephone numbers such as "+44 (0)1234 123456" would not be stored in anything by a `TEXT` field. So because of the diversity of available numbers it's much simpler for the end user to not have to worry.

Both of these tables also have a `contact_id` column, this is going to hold special meaning within the table. We're setting it as a `FOREIGN KEY` which is a reference to another tables `PRIMARY KEY` and provides a link between records in different tables. Here we're saying that each entry in either table must link back to a valid `contact` by referencing the `id` primary key in the `contacts` table. The value of the `contacts` primary key, will be stored locally in the `contact_id` column. When we later remove a record from the `contacts` table the removal will cascade through each table that has a `FOREIGN KEY` and remove it as well, therefore keeping our data consistent.

#### Enabling Foreign Key constraints
As of version [3.6.19 of SQLite](http://www.sqlite.org/releaselog/3_6_19.html) foreign key constraints are disabled by default and require the `foreign_key_pragma` option to enable them. To do this select the 'Edit Pragmas' tab and check the 'Foreign Keys' and hit save. If you don't enable this; then there will be no enforced link between `numbers` and `email_addresses` with `contacts`.

#### Why use different tables?
When you're creating your database you don't know how many phone numbers someone might have; or how many email addresses they have. So it's impossible for you to correctly determine the number of columns you need. You could specify just a Home, Mobile and Work number then a Personal and Work email address but that's not very user-friendly, after all I might have two work numbers!

By using different tables we're able to offer a unlimited number of phone numbers and email addresses for each contact and cleanly reference them from any contact. So if you're in a situation where you don't know how many items of a particular type separate tables might be exactly what you need.

### Saving changes
Once all of the changes required have been made to the `contacts` database you need to commit the changes, to do this choose 'Write Changes' or press `Ctrl+S`. SQLite Browser works on a memory copy of the data, so any changes you made will not be saved to the file until you have done this. This process is known as committing the changes.

### Adding Contacts
Contacts are added using the `INSERT` query is used to add new records into a table; it has one of two basic forms:

```sql
INSERT INTO table(col1, col2) VALUES(1, 2);
INSERT INTO table VALUES(1, 2);
```

The second variation will only work if you are insert values into all of the columns for a given table, and when doing it you need to make sure that the values are in the correct order. The recommendation would be to use the first form always however; so that you're being explicit in what you're attempting to do.

To insert a new contact, we would run:

```sql
INSERT INTO contacts(firstname, family_name) VALUES('Adam', 'Jefferiss');
```

If you attempt to insert solely into the `family_name` column we'd get a error shown in the SQL output.
![NOT Null constraint failed error](/theme/images/intro_sqlite/insert_not_null_constraint.png "NOT NULL constraint when inserting record")

Before we insert records into the other tables we need to know the `id` of the newly inserted row so that we can use it as the `FOREIGN KEY` constraint. To do this immediately after running the `INSERT` query you can run:

```sql
SELECT last_insert_rowid();
```

Once you have this number; you can use it to create records in the other tables like so:

```sql
INSERT INTO numbers(number, contact_id) VALUES("+44 (0)1234 567890", 1);
```

You'll notice that for this insert statement, we're not putting single or double quotes around the `contact_id`. The basic rule is that an strings (words, characters, etc) need to be quoted using either single or double quotes. While integers do not.

If you attempt to create a record with an invalid contact ID you'll be present with a error message about a failed `FOREIGN KEY` constraint like so:
`FOREIGN KEY constraint failed: INSERT INTO numbers(number, contact_id) VALUES('22222222', -111);`

If you have multiple values you want to insert into a given table you can do so by providing a `VALUES` list for each entry, for example if we wanted to add 2 numbers for contact 1 we could run:

```sql
INSERT INTO numbers(number, contact_id) VALUES('+44 12345 678931', 1), ('+44 12345 678932', 1);
```

If you do insert multiple record bear in mind that `SELECT last_insert_rowid();` will only return the last row inserted, not the ids of the rows effected by the last statement. So if you need to retrieve the `PRIMARY KEY` for a record inserting multiple values is not the way to go!

### Finding Contacts
To find contacts within the database we need to use the `SELECT` SQL command; this command has two basic forms:

```sql
SELECT id, firstname, family_name FROM contacts;
SELECT * FROM contacts;
```

The first form is provided a list of columns you wish to retrieve information about; and the second uses an asterisk, `*`, to mean 'all columns'. In the example above both commands will return all of the information from within the `contacts` table. Considering the following table:
<table class="table">
    <thead>
        <tr>
            <th>id</th>
            <th>Firstname</th>
            <th>Family Name</th>
        </tr>
    </thead>
    <tbody>
        <tr><td>1</td><td>Adam</td><td>Jefferiss</td></tr>
        <tr><td>2</td><td>Luke</td><td>Skywalker</td></tr>
        <tr><td>3</td><td>Han</td><td>Solo</td></tr>
        <tr><td>4</td><td>R2D2</td><td></td></tr>
        <tr><td>5</td><td>C3PO</td><td></td></tr>
        <tr><td>6</td><td>Ben</td><td>skywalker</td></tr>
    </tbody>
</table>

Using the [WHERE](https://www.tutorialspoint.com/sqlite/sqlite_where_clause.htm) clause we're able to limit the results of our select statements; there's a number of [logical operators](https://www.tutorialspoint.com/sqlite/sqlite_logical_operators.htm) that can be used to limit the results. If we knew, for example, that the `firstname` of our contact contained a 'a' we could `SELECT` all contacts with an 'a' in the `firstname` using the `LIKE` operator:

```sql
SELECT id, firstname, family_name FROM contacts WHERE firstname LIKE '%a%';
```

From our table above; this would give us records 1 and 3. Within the `LIKE` statement there are two special characters, the percent sign (&#37;) and a underscore (&#95;). The percent sign represents zero or more numbers or characters while the underscore represents a single number or character. So if we reran our `SELECT` query with a `LIKE` value of `_a%` we'd only get the single row back for Han Solo. The reason for this is that we're saying there must be only 1 character, or number, in the `firstname` before the 'a', but there can be any number of characters or numbers after the first 'a'.

If we wanted to find all of the Skywalker family; we'd use:

```sql
SELECT id, firstname, family_name FROM contacts WHERE family_name = 'Skywalker';
```

If we run this on our current set of data though we'd miss off the record for Ben Skywalker! This might seem a little confusing given what we've seen with the `LIKE` condition. The `LIKE` condition has the `case_sensitive_like` pragma which by default is `false`, this means that `LIKE` does case insensitive comparisions, so 'A' and 'a' are both the same in the eyes of `LIKE`. Using `=` however is a exact match against the entry you've put. To get around this we can make use of two functions in SQLite, [upper](https://sqlite.org/lang_corefunc.html#upper) and [lower](https://sqlite.org/lang_corefunc.html#lower). These functions return a copy of a string as either upper or lower case. The following SQL will take a copy of the `family_name` column, and turn it to lower case before comparing it against 'skywalker'. Doing so will return us all of the rows we expect!

```sql
SELECT id, firstname, family_name FROM contacts WHERE LOWER(family_name) = 'skywalker';
```

Finally we can use the `IS` or `IS NOT`, which behave like `=` and `!=` to see what columns have values. If a column does not have a value, it is considered to be [NULL](https://en.wikipedia.org/wiki/Null_(SQL)), as such we can write the following two queries

```sql
SELECT id, firstname, family_name FROM contacts WHERE family_name IS NULL;
SELECT id, firstname, family_name FROM contacts WHERE family_name IS NOT NULL;
```

These queries will return the opposite records of each other; the first will return records for R2D2 and C3PO from the table above; while the second will return everything else.

#### Finding contacts phone numbers and email addresses

So far we've only been querying the `contacts` table; which doesn't actually do anything helpful. After all we need to find the email addresses and phone numbers of our contacts! Once you've created a few entries in both tables you can query them using [JOINS](https://www.tutorialspoint.com/sqlite/sqlite_using_joins.htm) or [SUBQUERIES](https://www.tutorialspoint.com/sqlite/sqlite_sub_queries.htm). Beyond our `contacts` table above, we're going to be executing the following SQL against the `numbers` and `email_addresses` tables with the following information.
<table class="table">
    <thead>
        <tr>
            <th>id</th>
            <th>Number</th>
            <th>Contact ID</th>
        </tr>
    </thead>
    <tbody>
        <tr><td>1</td><td>012345 6789012</td><td>1</td></tr>
        <tr><td>2</td><td>+99 11223344</td><td>2</td></tr>
        <tr><td>3</td><td>1234567</td><td>2</td></tr>
        <tr><td>4</td><td>(0)2345 112299</td><td>3</td></tr>
        <tr><td>5</td><td>01010111</td><td>4</td></tr>
        <tr><td>6</td><td>11110011</td><td>5</td></tr>
    </tbody>
</table>

<table class="table">
    <thead>
        <tr>
            <th>id</th>
            <th>Email Address</th>
            <th>Contact ID</th>
        </tr>
    </thead>
    <tbody>
        <tr><td>1</td><td>adam@open-moments.co.uk</td><td>1</td></tr>
        <tr><td>2</td><td>l.skywalker@rebels.gal</td><td>2</td></tr>
        <tr><td>3</td><td>nerfherder@rebels.gal</td><td>3</td></tr>
        <tr><td>4</td><td>r2@d2.net</td><td>4</td></tr>
        <tr><td>5</td><td>r2d2@rebels.gal</td><td>4</td></tr>
        <tr><td>6</td><td>c3po@translate.rebel.gal</td><td>5</td></tr>
    </tbody>
</table>

#### Joins
There are three types of [JOINS](https://www.tutorialspoint.com/sqlite/sqlite_using_joins.htm) available in SQLite

* Cross Join - Matches ever row of the first table; with every row on the second table; because these joins have the potential to generate extremely large tables care needs to be taken to only use them when appropriate

![CROSS JOIN SQLite example](/theme/images/intro_sqlite/cross_join_example.png "CROSS JOIN SQLite example")

* Inner Join  - Creates a new result table by combining column values of two tables based upon a join condition, these joins compare every row of the first table, with each row of the second table to find all pairs of rows which satisfy the join condition.

![INNER JOIN SQLite example](/theme/images/intro_sqlite/inner_join_example.png "INNER JOIN SQLite example")

* Outer Join - An outer join is an extension of `INNER JOIN`, through there are technically three types of outer joins defined within the SQL standard SQLite only supports a `LEFT OUTER JOIN`. The condition used by an outer join are identical those of an inner join, however once the primary join has been calculated an outer join will take any unjoined rows and pad them with NULLS before appending them to the resulting table.

![OUTER JOIN SQLite example](/theme/images/intro_sqlite/outer_join_example.png "OUTER JOIN SQLite example")

#### Subqueries
A sub-query could also be known as either a nester or inner query, and is a query embedded within the `WHERE` clause of a query. A sub-query is used to return data that will be used in the main query as a condition to restrict retrieved data. There are a few rules that each sub-query must follow:

* Sub-queries must be within parentheses '()'
* A sub-query can only select one column; unless there are multiple columns in the main query for the sub-query to compare against.
* Sub-queries cannot use `ORDER BY` clauses
* Sub-queries that return more than one row can only be used within the `IN` operator
* Sub-queries cannot used `BETWEEN` operators

To return the number of a specific person; we could use:

```sql
SELECT number FROM numbers WHERE contact_id IN (
    SELECT id FROM contacts WHERE firstname = 'Adam' AND family_name = 'Jefferiss'
);
```

To return the numbers of anyone in the Skywalker family we could use the following query:

```sql
SELECT number FROM numbers WHERE contact_id IN (
	SELECT id FROM contacts WHERE LOWER(family_name) = 'skywalker'
);
```

To return the numbers and email address for a given we could use:

```sql
SELECT
	n.number, e.address 
FROM
	numbers n, email_addresses e
WHERE
	n.contact_id IN (SELECT id FROM contacts WHERE firstname = 'R2D2')
AND
	e.contact_id IN (SELECT id FROM contacts WHERE firstname = 'R2D2')
```

### Removing Contacts
The command to remove a row from the `contacts` table we'll use the `DELETE` SQL command, this command takes the table name and optionally a condition to match via the [WHERE](https://www.tutorialspoint.com/sqlite/sqlite_where_clause.htm) clause. If you do not limit the `DELETE` it will remove everything from the table!

Knowing the `id` of the contact you want to remove you can execute a statement like the following, which will remove all `numbers` and `email_addresses` for the contact as well, as an example to remove everything for contact 9 we'd run:

```sql
DELETE FROM contacts WHERE id = 9;
```

If you do not know the `id` of a contact; you can remove it using any of the other columns; but doing so may be risky as you will remove any rows with a matching column. For example if we had two rows, one for 'Adam Jefferiss' and another for 'Adam Smith' we'd end up deleting both records if we ran:

```sql
DELETE FROM contacts WHERE firstname = 'Adam';
```

So it is worth finding the ID of the record before attempting any deletes. If you just wanted to remove all of the numbers for a given contact, for example, you could run.

```sql
DELETE FROM numbers WHERE contact_id = 9;
```
