# Generated by Django 2.2 on 2019-05-07 02:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_student_account_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activity',
            options={'permissions': (('manage_activity', 'As a activity manager has a right of manage activity'),)},
        ),
    ]
