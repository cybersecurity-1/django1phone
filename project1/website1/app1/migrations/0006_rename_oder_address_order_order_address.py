# Generated by Django 5.0.7 on 2024-08-10 10:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0005_rename_oder_adress_order_oder_address'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='oder_address',
            new_name='order_address',
        ),
    ]