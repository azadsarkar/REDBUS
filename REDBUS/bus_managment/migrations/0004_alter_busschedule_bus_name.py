# Generated by Django 5.1.1 on 2024-11-13 11:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bus_managment", "0003_busschedule_bus_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="busschedule",
            name="bus_name",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="bus_managment.bus",
            ),
        ),
    ]