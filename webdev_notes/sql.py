"""
# STRUCTURED QUERY LANGUAGE (SQL)

    a type of relational database, which is now the prominent type of databases in the world

    database relationships

        one to one, one to many, many to many

        eg.
            a user only has one email (one to one)
            a user has only one first name and last name (one to many)
            many users may have multiple products in their cart (many to many)


    major database systems: Postgres, MySQL, Oracle, SQLServer,
    simple projects: SQLite, HSQL,
    - built on top of the SQL requirements

    4 Principles of Databases: CREATE, RETRIEVE, UPDATE, DELETE data

    some SQL syntax that you may not know / need a recap:
        data types:
            VARCHAR(128) - allows text up to 128 chars in length

        commands:
            .tables - list all available tables
            .schema - list the data scheme of all available tables

        queries:
            INSERT INTO Users(name, email) VALUES ('Ryan', 'ryan@harvard.edu');
            - allows you to add data into a table called 'Users' in the columns 'name' and 'email'

            DELETE FROM Users WHERE email='ryan@harvard.edu';
            - removes the user if its email is 'ryan@harvard.edu'

            SELECT * FROM Users WHERE email='ryan@harvard.edu';
            - find all the users with the email 'ryan@harvard.edu'

            SELECT * FROM Users ORDER BY email;
            - organise alphanumerically the users table by the email

            UPDATE Users SET name='charles' WHERE email='ryan@harvard.edu';
            - change the name in the Users table where the email is 'ryan@harvard.edu'

    # Object relational mapping

        - to map tables to objects and columns in python
        - allows you to have multiple kinds of SQL databases within the same project

        In Python:

            from django.db import models

            class User(models.Model):
                name = models.CharField(max_length=128)
                email = models.CharField(max_length=128)

        - models is a library that translates python methods into SQL commands

        In SQL:
            CREATE TABLE Users(
                name VARCHAR(128),
                email VARCHAR(128)
            );

        translating Python to SQL

        CREATE in Django

        u = User(name='Sally', email='sally@gmail.com')
        u.save()

        READ in Django

        User.objects.values()
        User.objetcs.filter(email='sally@gmail.com').values()
        User.objects.values().order_by('email')

        UPDATE in Django
        User.objects.filter(email='sally@gmail.com').update(name='Sally Gan')

        DELETE in Django
        User.drop()
"""