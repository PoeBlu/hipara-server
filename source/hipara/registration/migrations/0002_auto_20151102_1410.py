# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from ..models import UserMetaData, Role

from django.contrib.auth.models import User

from django.contrib.auth.hashers import make_password

def data_seeder(apps, schema_editor):
    role1 = Role.objects.create(name='Super Admin')
    role2 = Role.objects.create(name='Admin')
    role3 = Role.objects.create(name='User')
    password = make_password('bitroots')
    superuser = User.objects.create(
        password=password,
        is_superuser=1,
        username='abhijeet',
        first_name='Abhijeet',
        last_name='Kohakade',
        email='abhijeet@dev.bitroots.co',
        is_staff=1
    )
    superusermetadata = UserMetaData.objects.create(
        user=superuser,
        role=role1,
        created_by=superuser,
        updated_by=superuser
    )
    superadmin = User.objects.create(
        password=password,
        username='kohakade',
        first_name='Abhijeet',
        last_name='Kohakade',
        email='abhijeet.kohakade99@gmail.com'
    )
    superadminmetadata = UserMetaData.objects.create(
        user=superadmin,
        role=role1,
        created_by=superadmin,
        updated_by=superadmin
    )



def data_revert(apps, schema_editors):
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute('SET FOREIGN_KEY_CHECKS=0')
    cursor.execute('TRUNCATE TABLE {0}'.format(UserMetaData._meta.db_table))
    cursor.execute('TRUNCATE TABLE {0}'.format(User._meta.db_table))
    cursor.execute('TRUNCATE TABLE {0}'.format(Role._meta.db_table))
    cursor.execute('SET FOREIGN_KEY_CHECKS=1')



class Migration(migrations.Migration):



    dependencies = [
        ('registration', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(code=data_seeder, reverse_code=data_revert),
    ]
