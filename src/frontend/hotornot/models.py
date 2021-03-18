from django.db import models


class Company(models.Model):
    stock_code = models.TextField(primary_key=True)
    short_hand = models.TextField()
    verdict = models.TextField()
    predictions = models.JSONField()
    change = models.FloatField()
    sector = models.TextField()
    industry = models.TextField()

    class Meta:
        db_table = "company"

    def __str__(self):
        return self.stock_code

    def not_change(self):
        return self.change * -1

class Sentence(models.Model):
    id = models.IntegerField(primary_key=True)
    text = models.TextField()
    sentiment = models.FloatField()
    status = models.TextField()
    article_id = models.TextField()
    context = models.TextField()
    date = models.DateField()
    time = models.TimeField()

    class Meta:
        db_table = "sentence"

    def __str__(self):
        return self.id


class Article(models.Model):
    id = models.TextField(primary_key=True)
    title = models.TextField()
    transcript = models.TextField()
    date = models.DateField()
    status = models.TextField()
    source_id = models.IntegerField()
    time = models.TimeField()
    context = models.TextField()

    class Meta:
        db_table = "article"

    def __str__(self):
        return self.id


class Source(models.Model):
    id = models.IntegerField(primary_key=True)
    short_hand = models.TextField()
    rss = models.TextField()

    class Meta:
        db_table = "source"

    def __str__(self):
        return self.short_hand


class Tag(models.Model):
    tag_id = models.IntegerField(primary_key=True)
    tag_title = models.TextField()

    class Meta:
        db_table = "tags"

    def __str__(self):
        return self.tag_title


class CompanyTag(models.Model):
    company_code = models.TextField()
    tag_id = models.IntegerField()
    id = models.IntegerField(primary_key=True)

    class Meta:
        db_table = "company_tags"

    def __str__(self):
        return self.company_code
