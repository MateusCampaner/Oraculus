# Generated by Django 4.2.4 on 2023-09-16 06:08

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Colheita",
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
                ("nome_colheita", models.CharField(max_length=50)),
                ("nome_colheita_dataset", models.CharField(max_length=50)),
            ],
        ),
    ]