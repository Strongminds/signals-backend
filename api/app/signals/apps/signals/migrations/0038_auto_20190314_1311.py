# Generated by Django 2.1.7 on 2019-03-14 12:11

from django.db import migrations


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
        migrations.AlterUniqueTogether(
            name='category',
            unique_together={('parent', 'slug')},
        ),
    ]