# Generated by Django 4.2.6 on 2023-10-29 02:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0002_alter_review_reviewer_name'),
        ('recommendation', '0008_recommendation_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recommendation',
            name='user',
        ),
        migrations.AddField(
            model_name='recommendation',
            name='review',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='review.review'),
        ),
    ]