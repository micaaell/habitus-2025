# Generated by Django 4.2.7 on 2025-06-27 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("habitusapp", "0011_alter_admin_tipo_trabalho_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="professor",
            name="altura",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="professor",
            name="nivel",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Iniciante", "Iniciante"),
                    ("Intermediário", "Intermediário"),
                    ("Avançado", "Avançado"),
                ],
                max_length=20,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="professor",
            name="objetivo",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Ganho de Massa", "Ganho de Massa"),
                    ("Perda de peso", "Perda de peso"),
                    ("Saúde", "Saúde"),
                    ("Outro", "Outro"),
                ],
                max_length=20,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="professor",
            name="peso",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="admin",
            name="tipo_trabalho",
            field=models.CharField(default="Professor(a)", max_length=20),
        ),
        migrations.AlterField(
            model_name="professor",
            name="tipo_trabalho",
            field=models.CharField(default="Professor(a)", max_length=20),
        ),
    ]
