# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='work_or_study',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
