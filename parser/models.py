
import datetime
import asyncio
import peewee
from peewee_async import Manager, PostgresqlDatabase

try:
    loop = asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
database = PostgresqlDatabase(
    'postgres',
    user='postgres',
    password='postgres',
    host='db',
)
objects = Manager(database, loop=loop)

class User(peewee.Model):
    email = peewee.CharField(max_length=254)
    first_name = peewee.CharField(max_length=50)
    last_name = peewee.CharField(max_length=50)
    password = peewee.CharField(max_length=128)
    is_superuser = peewee.BooleanField(default=False)
    email_is_activate = peewee.BooleanField(default=False)
    is_staff = peewee.BooleanField(default=False)
    is_active = peewee.BooleanField(default=False)

    class Meta:
        database=database
        table_name = 'user_user'


class Precedent(peewee.Model):
    name = peewee.CharField(max_length=50)
    attitude = peewee.IntegerField()
    importance = peewee.IntegerField()
    user_id = peewee.IntegerField()
    updated_at = peewee.DateTimeField(default=datetime.datetime.now())

    class Meta:
        database=database
        table_name = 'user_precedent'

