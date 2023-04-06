# Generated by Django 4.2 on 2023-04-06 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_user_bio'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='podcast',
            name='genre',
        ),
        migrations.DeleteModel(
            name='Genre',
        ),
        migrations.AddField(
            model_name='podcast',
            name='genre',
            field=models.CharField(default='culture', max_length=100),
        ),
    ]
