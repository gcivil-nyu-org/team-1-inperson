# Generated by Django 2.2 on 2022-10-15 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("report", "0003_auto_20221015_1343"),
    ]

    operations = [
        migrations.AlterField(
            model_name="report",
            name="dateTimeOfResolution",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
