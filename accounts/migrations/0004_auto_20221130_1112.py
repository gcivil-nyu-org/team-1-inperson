# Generated by Django 2.2 on 2022-11-30 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20221122_2031'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeleteAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password_confirmation', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='editpassword',
            name='confirm_password',
            field=models.CharField(default=None, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='editfname',
            name='new_first_name',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='editlname',
            name='new_last_name',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='editpassword',
            name='new_password',
            field=models.CharField(max_length=50),
        ),
    ]
