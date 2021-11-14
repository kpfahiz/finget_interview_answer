from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):

    zero, one, five, ten = 0, 1, 5, 10
    TAX = [(zero, '0%'), (one, '1%'), (five, '5%'), (ten, '10%')]

    name = models.CharField(max_length=255)
    unit_price = models.FloatField()
    tax = models.SmallIntegerField(choices=TAX, default=zero)
    quantity = models.IntegerField(default=1)


    

    def __str__(self):
        return self.name

class Invoice(models.Model):
    
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        items = models.ForeignKey(Item, on_delete=models.CASCADE)
        date = models.DateField()

        def get_total(self):
            total = 0
            for item in self.items.all():
                total += item.unit_price
            return total
    
        def __str__(self):
            return self.user.username

