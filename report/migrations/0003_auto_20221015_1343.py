# Generated by Django 2.2 on 2022-10-15 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("report", "0002_report_comment"),
    ]

    operations = [
        migrations.AlterField(
            model_name="report",
            name="dateTimeOfResolution",
            field=models.DateTimeField(blank=True),
        ),
    ]
