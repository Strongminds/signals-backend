# SPDX-License-Identifier: MPL-2.0
# Copyright (C) 2019 - 2023 Gemeente Amsterdam
# Generated by Django 2.1.7 on 2019-05-03 08:53

import django.db.models.deletion
from django.db import migrations, models
from django_extensions.db.fields import AutoSlugField  # type: ignore


class Migration(migrations.Migration):

    dependencies = [
        ('signals', '0045_category_changes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='handling',
            field=models.CharField(choices=[('A3DMC', 'A3DMC'), ('A3DEC', 'A3DEC'),
                                            ('A3WMC', 'A3WMC'), ('A3WEC', 'A3WEC'),
                                            ('I5DMC', 'I5DMC'), ('STOPEC', 'STOPEC'),
                                            ('KLOKLICHTZC', 'KLOKLICHTZC'), ('GLADZC', 'GLADZC'),
                                            ('A3DEVOMC', 'A3DEVOMC'), ('WS1EC', 'WS1EC'),
                                            ('WS2EC', 'WS2EC'), ('WS3EC', 'WS3EC'),
                                            ('REST', 'REST'), ('ONDERMIJNING', 'ONDERMIJNING'),
                                            ('EMPTY', 'EMPTY')], default='REST', max_length=20),
        ),
        migrations.AlterField(
            model_name='category',
            name='parent',
            field=models.ForeignKey(blank=True, null=True,
                                    on_delete=django.db.models.deletion.PROTECT,
                                    related_name='children', to='signals.Category'),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=AutoSlugField(blank=True, editable=False, populate_from=['name']),
        ),
    ]
