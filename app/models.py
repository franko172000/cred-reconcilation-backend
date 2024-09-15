from datetime import datetime

from django.db import models


# Create your models here.
class Upload(models.Model):
    title = models.CharField(max_length=100)
    source = models.FileField(upload_to='uploads/')
    target = models.FileField(upload_to='uploads/')
    description = models.TextField(blank=True, null=True)
    discrepancies = models.JSONField(blank=True, null=True)
    missing_in_source = models.JSONField(blank=True, null=True)
    missing_in_target = models.JSONField(blank=True, null=True)

    class Meta:
        db_table = 'uploads'


class Record(models.Model):
    name = models.CharField(max_length=100, null=False)
    account_number = models.CharField(max_length=50, null=False)
    transaction_date = models.DateField(null=False)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    description = models.TextField(blank=True, null=True)
    upload = models.ForeignKey(Upload, on_delete=models.CASCADE)

    class Meta:
        db_table = 'records'
