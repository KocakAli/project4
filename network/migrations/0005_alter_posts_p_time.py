# Generated by Django 3.2.5 on 2021-09-04 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_posts_p_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='p_time',
            field=models.CharField(max_length=64),
        ),
    ]
