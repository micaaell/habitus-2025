# Generated by Django 4.2.7 on 2025-06-27 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("habitusapp", "0010_remove_noticia_titulo_alter_noticia_categoria"),
    ]

    operations = [
        migrations.AlterField(
            model_name="admin",
            name="tipo_trabalho",
            field=models.CharField(
                choices=[("Administrador(a)", "Administrador(a)")],
                default="Administrador(a)",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="professor",
            name="tipo_trabalho",
            field=models.CharField(
                choices=[("Professor(a)", "Professor(a)")],
                default="Professor(a)",
                max_length=20,
            ),
        ),
    ]
