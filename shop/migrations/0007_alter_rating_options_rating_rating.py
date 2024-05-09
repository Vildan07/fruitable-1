# Generated by Django 5.0.4 on 2024-05-09 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_rating'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rating',
            options={'ordering': ['-pk'], 'verbose_name': 'Рейтинг', 'verbose_name_plural': 'Рейтинги продуктов'},
        ),
        migrations.AddField(
            model_name='rating',
            name='rating',
            field=models.IntegerField(default=0),
        ),
    ]
