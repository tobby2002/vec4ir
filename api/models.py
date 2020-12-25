from django.db import models


class GoogleBook(models.Model):
    id = models.AutoField(primary_key=True)
    book_id = models.IntegerField()
    best_book_id = models.IntegerField()
    work_id = models.IntegerField()
    books_count = models.IntegerField()
    isbn = models.CharField(max_length=20, null=True, blank=True)
    isbn13 = models.CharField(max_length=50, null=True, blank=True)
    authors = models.CharField(max_length=100, null=True, blank=True)
    original_publication_year = models.SmallIntegerField(null=True, blank=True)
    original_title = models.CharField(max_length=500, null=True, blank=True)
    title = models.TextField(null=True, blank=True)
    language_code = models.CharField(max_length=10, null=True, blank=True)
    average_rating = models.FloatField()
    ratings_count = models.FloatField()
    work_ratings_count = models.IntegerField()
    work_text_reviews_count = models.IntegerField()
    ratings_1 = models.IntegerField()
    ratings_2 = models.IntegerField()
    ratings_3 = models.IntegerField()
    ratings_4 = models.IntegerField()
    ratings_5 = models.IntegerField()
    image_url = models.CharField(max_length=200)
    small_image_url = models.CharField(max_length=200)


class LtrQueries(models.Model):
    label = models.IntegerField(default=0)
    qid = models.IntegerField()
    f1 = models.FloatField(max_length=10, default=0.0)
    f2 = models.FloatField(max_length=10, default=0.0)
    f3 = models.FloatField(max_length=10, default=0.0)
    f4 = models.FloatField(max_length=10, default=0.0)
    docid = models.IntegerField()
    q = models.TextField(null=True, blank=True)
    title = models.TextField(null=True, blank=True)
    status = models.SmallIntegerField()

class Sport(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Market(models.Model):
    name = models.CharField(max_length=100)
    sport = models.ForeignKey(Sport,related_name='markets', on_delete=models.CASCADE)

    def __str__(self):
        return self.name + ' | ' + self.sport.name

class Selection(models.Model):
    name = models.CharField(max_length=100)
    odds = models.FloatField()
    market = models.ForeignKey(Market,related_name='selections', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Match(models.Model):
    name = models.CharField(max_length=100)
    startTime = models.DateTimeField()
    sport = models.ForeignKey(Sport, related_name='matches', on_delete=models.CASCADE)
    market = models.ForeignKey(Market, related_name='matches', on_delete=models.CASCADE)

    class Meta:
        ordering = ('startTime',)
        verbose_name_plural = 'Matches'

    def __str__(self):
        return self.name
