# Generated by Django 4.1.1 on 2023-10-14 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("userapp", "0002_remove_user_address_address"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="address",
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.DeleteModel(
            name="Address",
        ),
    ]
