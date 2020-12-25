# Generated by Django 2.1.5 on 2019-10-04 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoogleBook',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('book_id', models.IntegerField()),
                ('best_book_id', models.IntegerField()),
                ('work_id', models.IntegerField()),
                ('books_count', models.IntegerField()),
                ('isbn', models.CharField(blank=True, max_length=20, null=True)),
                ('isbn13', models.CharField(blank=True, max_length=50, null=True)),
                ('authors', models.CharField(blank=True, max_length=100, null=True)),
                ('original_publication_year', models.SmallIntegerField(blank=True, null=True)),
                ('original_title', models.CharField(blank=True, max_length=500, null=True)),
                ('title', models.TextField(blank=True, null=True)),
                ('language_code', models.CharField(blank=True, max_length=10, null=True)),
                ('average_rating', models.FloatField()),
                ('ratings_count', models.FloatField()),
                ('work_ratings_count', models.IntegerField()),
                ('work_text_reviews_count', models.IntegerField()),
                ('ratings_1', models.IntegerField()),
                ('ratings_2', models.IntegerField()),
                ('ratings_3', models.IntegerField()),
                ('ratings_4', models.IntegerField()),
                ('ratings_5', models.IntegerField()),
                ('image_url', models.CharField(max_length=200)),
                ('small_image_url', models.CharField(max_length=200)),
            ],
        ),
    ]