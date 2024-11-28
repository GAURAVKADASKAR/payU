from django.db import models


class payment(models.Model):
    status=models.CharField(max_length=200)
    amount=models.TextField()
    txnid=models.TextField()



    def __str__(self):
        return self.txnid