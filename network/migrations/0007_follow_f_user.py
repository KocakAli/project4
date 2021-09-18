# Generated by Django 3.2.5 on 2021-09-15 15:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0006_follow'),
    ]

    operations = [
        migrations.AddField(
            model_name='follow',
            name='f_user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='users_f', to='network.user'),
            preserve_default=False,
        ),
    ]
