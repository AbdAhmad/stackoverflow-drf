# Generated by Django 3.2.9 on 2021-12-26 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stack_app', '0002_auto_20211225_0710'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='answers',
            field=models.ManyToManyField(blank=True, to='stack_app.Answer'),
        ),
    ]