# Generated by Django 5.0.7 on 2024-07-28 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pro_name', models.CharField(max_length=250)),
                ('pro_price', models.FloatField()),
                ('pro_image', models.FileField(null=True, upload_to='products')),
            ],
        ),
    ]
