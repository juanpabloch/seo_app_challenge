# Generated by Django 4.2 on 2024-08-29 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UrlData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url_1', models.URLField()),
                ('url_2', models.URLField()),
                ('strategy', models.CharField(choices=[('desktop', 'Desktop'), ('mobile', 'Mobile')], max_length=10)),
                ('index_1', models.FloatField()),
                ('interactive_1', models.FloatField()),
                ('index_2', models.FloatField()),
                ('interactive_2', models.FloatField()),
            ],
            options={
                'db_table': 'url_data',
                'ordering': ['-id'],
            },
        ),
    ]
