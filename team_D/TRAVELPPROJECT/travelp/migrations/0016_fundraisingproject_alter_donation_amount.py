# Generated by Django 4.0 on 2025-02-07 02:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travelp', '0015_alter_comment_user_alter_like_user_alter_plan_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='FundraisingProject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('goal_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('collected_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name='donation',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(50)]),
        ),
    ]
