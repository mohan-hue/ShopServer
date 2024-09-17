# Generated by Django 4.2.7 on 2024-09-06 09:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0005_beautypersonalcare_product_classify_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopproductclassify',
            name='shop',
            field=models.ForeignKey(blank=True, help_text='店铺ID', on_delete=django.db.models.deletion.CASCADE, to='Shop.shop', verbose_name='店铺ID'),
        ),
    ]
