# Generated by Django 5.1.1 on 2024-11-15 08:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bus_managment", "0008_rename_bus_name_busschedule_bus"),
    ]

    operations = [
        migrations.CreateModel(
            name="IntermidiateStop",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("stop_name", models.CharField(max_length=20)),
                ("inter_stop_id", models.IntegerField(unique=True)),
                (
                    "bus_route",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="bus_managment.busroute",
                    ),
                ),
            ],
        ),
    ]
