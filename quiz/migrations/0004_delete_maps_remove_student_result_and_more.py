# Generated by Django 4.1.6 on 2023-08-03 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_maps_result_alter_regforcriteria_content_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Maps',
        ),
        migrations.RemoveField(
            model_name='student',
            name='result',
        ),
        migrations.AlterField(
            model_name='regforcriteria',
            name='content',
            field=models.TextField(default='Hello World'),
        ),
        migrations.AlterField(
            model_name='test',
            name='content',
            field=models.TextField(default='Hello World'),
        ),
        migrations.AlterField(
            model_name='uniquecriteria',
            name='content',
            field=models.TextField(default='Hello World'),
        ),
        migrations.AlterField(
            model_name='wordtocriteria',
            name='content',
            field=models.TextField(default='Hello World'),
        ),
        migrations.DeleteModel(
            name='Result',
        ),
        migrations.DeleteModel(
            name='Student',
        ),
    ]