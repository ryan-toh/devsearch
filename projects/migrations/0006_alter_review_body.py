# Generated by Django 4.2.5 on 2023-10-09 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_alter_project_options_review_created_review_owner_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='body',
            field=models.TextField(default='default', max_length=200),
            preserve_default=False,
        ),
    ]
