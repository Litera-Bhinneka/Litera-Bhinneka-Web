# Generated by Django 4.2.6 on 2023-10-28 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommendation', '0006_recommendation_another_book_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='recommendation',
            name='another_book_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='recommendation',
            name='book_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
