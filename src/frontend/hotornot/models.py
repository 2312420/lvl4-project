from django.db import models

# Create your models here.


class Company(models.Model):
    stock_code = models.TextField(primary_key=True)
    short_hand = models.TextField()
    verdict = models.TextField()
    class Meta:
        db_table = "company"

    def __str__(self):
        return self.stock_code

