# Generated by Django 4.0 on 2022-05-26 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Machine_api', '0002_machine_owner_user_created_at_project_organisation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organisation',
            name='projects',
            field=models.ManyToManyField(null=True, to='Machine_api.Project'),
        ),
    ]
