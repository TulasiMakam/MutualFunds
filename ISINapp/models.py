from django.db import models

# Create your models here.

class MutualFunds(models.Model):
    ISIN = models.CharField(max_length=100, unique=True)
    mutual_funds_name = models.CharField(max_length=100, default=None)
    date = models.DateField(auto_now_add=True)
    price = models.FloatField(max_length=100, default=None)
    status = models.CharField(max_length=100, default=None)

    class Meta:
        verbose_name = 'MutualFunds'


    def __str__(self):
        ret = self.ISIN
        return ret

    def __unicode__(self):
        return self.id()
