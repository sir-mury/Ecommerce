from accounts.models import BusinessProfile
from django.db import models
from django.conf import settings

# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=65)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('title',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=65)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('title',)
        verbose_name = 'tag'
        verbose_name_plural = 'tags'

    def __str__(self):
        return self.title


class Product(models.Model):
    name = models.CharField(max_length=255)
    brandIcon = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    able_to_sell = models.BooleanField(default=False)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='product')
    tags = models.ManyToManyField(Tag, related_name='product', blank=True)
    #video = mode
    percentage_off = models.IntegerField(null=True, blank=True)
    specifications = models.CharField(blank=True, max_length=255)
    is_price_fixed = models.BooleanField(default=True)
    # color
    image = models.ImageField(blank=True, null=True)
    negotiable = models.BooleanField(default=False)
    # review
    previous_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    #business = models.ForeignKey(BusinessProfile,on_delete=models.CASCADE,related_name='business')
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_created',)
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


