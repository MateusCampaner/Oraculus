# Generated by Django 4.2.4 on 2023-09-15 21:52

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Analise",
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
                ("N", models.IntegerField()),
                ("P", models.IntegerField()),
                ("K", models.IntegerField()),
                ("Temperatura", models.FloatField()),
                ("Umidade", models.FloatField()),
                ("pH", models.FloatField()),
                ("Chuva", models.FloatField()),
            ],
        ),
    ]