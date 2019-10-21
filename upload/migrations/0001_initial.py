# Generated by Django 2.2.4 on 2019-10-19 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('pid', models.AutoField(primary_key=True, serialize=False)),
                ('style', models.CharField(max_length=30)),
                ('img', models.CharField(max_length=500)),
                ('top_name', models.CharField(max_length=500)),
                ('top_url', models.URLField()),
                ('bot_name', models.CharField(max_length=500)),
                ('bot_url', models.URLField()),
            ],
        ),
    ]