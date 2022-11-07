from django.db import models

# Create your models here.
class Stock(models.Model):
    ticker = models.CharField(max_length=30)
    stock_data = models.FileField(upload_to='stocks/')

    def __str__(self):
        return self.ticker
