# Generated by Django 4.2.4 on 2023-08-04 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0019_test_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='name',
            field=models.CharField(default='unnamed_test', max_length=100),
        ),
    ]
