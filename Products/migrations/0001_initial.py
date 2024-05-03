# Generated by Django 4.2.6 on 2024-04-26 05:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Category', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Product_name', models.CharField(max_length=200, unique=True)),
                ('Slug', models.CharField(max_length=200, unique=True)),
                ('Description', models.CharField(blank=True, max_length=500)),
                ('Images', models.CharField(max_length=250)),
                ('Is_available', models.BooleanField(default=True)),
                ('Created_date', models.DateTimeField(auto_now_add=True)),
                ('Modified_date', models.DateTimeField(auto_now=True)),
                ('Category', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='Category.category')),
                ('SubCategory', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='Category.subcategory')),
            ],
        ),
    ]
