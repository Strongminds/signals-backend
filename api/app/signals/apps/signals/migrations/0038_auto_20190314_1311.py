# Generated by Django 2.1.7 on 2019-03-14 12:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('signals', '0037_auto_20190313_1538'),
    ]

    operations = [
        migrations.RenameField(
            model_name='signal',
            old_name='sub_categories',
            new_name='categories',
        ),
        migrations.RenameField(
            model_name='category',
            old_name='main_category',
            new_name='parent',
        ),
        migrations.AlterField(
            model_name='category',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT,
                                    related_name='categories', to='signals.Category'),
        ),
        migrations.AlterUniqueTogether(
            name='category',
            unique_together={('parent', 'slug')},
        ),
        migrations.AlterField(
            model_name='category',
            name='handling',
            field=models.CharField(
                choices=[('A3DMC', 'A3DMC'), ('A3DEC', 'A3DEC'), ('A3WMC', 'A3WMC'),
                         ('A3WEC', 'A3WEC'), ('I5DMC', 'I5DMC'), ('STOPEC', 'STOPEC'),
                         ('KLOKLICHTZC', 'KLOKLICHTZC'), ('GLADZC', 'GLADZC'),
                         ('A3DEVOMC', 'A3DEVOMC'), ('WS1EC', 'WS1EC'), ('WS2EC', 'WS2EC'),
                         ('REST', 'REST')], default='REST', max_length=20),
        ),
    ]
