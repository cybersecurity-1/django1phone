# Generated by Django 5.0.7 on 2024-08-10 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_cart_alter_register_reg_psw'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_prouser', models.CharField(default=None, max_length=250)),
                ('order_proname', models.CharField(max_length=250)),
                ('order_proprice', models.FloatField(max_length=250)),
                ('order_proimage', models.FileField(null=True, upload_to='')),
                ('order_proqty', models.IntegerField()),
                ('order_proamount', models.FloatField()),
                ('oder_adress', models.TextField(null=True)),
                ('order_paytype', models.CharField(max_length=10, null=True)),
                ('order_status', models.IntegerField(default=0)),
            ],
        ),
    ]
