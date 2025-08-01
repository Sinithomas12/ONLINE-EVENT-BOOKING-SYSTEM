# Generated by Django 4.2 on 2025-06-27 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('image', models.ImageField(null=True, upload_to='')),
                ('description', models.TextField()),
                ('datetime', models.DateTimeField()),
                ('venue', models.CharField(max_length=255)),
                ('capacity', models.IntegerField()),
                ('regdead', models.DateTimeField()),
            ],
        ),
    ]
