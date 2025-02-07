# Generated by Django 4.0 on 2025-01-29 03:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_customuser_nickname'),
        ('travelp', '0010_remove_post_user_post_latitude_post_longitude_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='accounts.customuser'),
            preserve_default=False,
        ),
    ]
