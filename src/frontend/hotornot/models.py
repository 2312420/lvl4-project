from django.db import models

# Create your models here.


class Company(models.Model):
    stock_code = models.TextField(primary_key=True)
    short_hand = models.TextField()
    verdict = models.TextField()
    predictions = models.JSONField()

    class Meta:
        db_table = "company"

    def __str__(self):
        return self.stock_code


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
