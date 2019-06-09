from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=25, help_text='Customer facing name of product')
    code = models.CharField(unique=True, max_length=10, help_text='Internal facing reference to product')
    price = models.PositiveIntegerField(help_text='Default price of product in cents')

    def __str__(self):
        return '{} - {}'.format(self.name, self.code)


class GiftCard(models.Model):
    code = models.CharField(unique=True, max_length=30)
    amount = models.PositiveIntegerField(help_text='Value of gift card in cents.')
    date_start = models.DateField()
    date_end = models.DateField(blank=True, null=True)

    def __str__(self):
        return '{} - {}'.format(self.code, self.formatted_amount)

    @property
    def formatted_amount(self):
        return '${0:.2f}'.format(self.amount / 100)

class ProductPrice(models.Model):
     name = models.CharField(max_length=25, help_text='Name of price change')
     product = models.ForeignKey(Product, on_delete=models.CASCADE)
     date_start = models.DateField()
     date_end = models.DateField(blank=True, null=True)
     price = models.PositiveIntegerField(help_text='Price of product in cents')

     def __str__(self):
         return '{} : {} : {} - {} : {}'.format(self.product.code, self.name,
            self.date_start, self.date_end, self.formatted_price)

     @property
     def formatted_price(self):
         return '${0:.2f}'.format(self.price / 100)
