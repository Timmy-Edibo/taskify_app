# Generated by Django 5.0.3 on 2024-03-12 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tasks", "0003_task_created_by"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="task_identifier",
            field=models.IntegerField(
                blank=True, editable=False, null=True, unique=True
            ),
        ),
    ]