# Generated by Django 5.0.7 on 2024-08-06 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_delete_customdepartmentstudent_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='address',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]