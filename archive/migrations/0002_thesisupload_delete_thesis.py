# Generated by Django 4.2.11 on 2024-04-03 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ThesisUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=200, null=True)),
                ('author', models.CharField(blank=True, max_length=200, null=True)),
                ('author1', models.CharField(blank=True, max_length=200, null=True)),
                ('author2', models.CharField(blank=True, max_length=200, null=True)),
                ('author3', models.CharField(blank=True, max_length=200, null=True)),
                ('author4', models.CharField(blank=True, max_length=200, null=True)),
                ('abstract', models.TextField(blank=True, null=True)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('file_thesis', models.FileField(blank=True, null=True, upload_to='thesis_files/')),
            ],
        ),
        migrations.DeleteModel(
            name='Thesis',
        ),
    ]
