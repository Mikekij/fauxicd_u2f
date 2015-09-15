# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='TfaRegistration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_id', models.IntegerField()),
                ('key_handle', models.CharField(max_length=128)),
                ('public_key', models.TextField()),
                ('certificate', models.TextField()),
                ('counter', models.IntegerField(default=0)),
                ('last_authenticated_at', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
