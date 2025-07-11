# Generated by Django 4.2.7 on 2025-06-21 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("habitusapp", "0003_alter_admin_foto_perfil_alter_aluno_foto_perfil_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="admin",
            name="foto_perfil",
            field=models.ImageField(
                blank=True, null=True, upload_to="foto-perfil-admin/"
            ),
        ),
        migrations.AlterField(
            model_name="aluno",
            name="foto_perfil",
            field=models.ImageField(
                blank=True, null=True, upload_to="foto-perfil-aluno/"
            ),
        ),
        migrations.AlterField(
            model_name="professor",
            name="foto_perfil",
            field=models.ImageField(
                blank=True, null=True, upload_to="foto-perfil-professor/"
            ),
        ),
    ]
