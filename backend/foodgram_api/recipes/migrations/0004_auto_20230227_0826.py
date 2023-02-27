# Generated by Django 3.2.16 on 2023-02-27 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_cart_uniq_cart_recipe'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='ingredient',
            index=models.Index(fields=['name'], name='recipes_ing_name_164c6a_idx'),
        ),
        migrations.AddIndex(
            model_name='recipe',
            index=models.Index(fields=['-pub_data'], name='recipes_rec_pub_dat_45009a_idx'),
        ),
        migrations.AddIndex(
            model_name='tag',
            index=models.Index(fields=['name'], name='recipes_tag_name_56fd94_idx'),
        ),
    ]
