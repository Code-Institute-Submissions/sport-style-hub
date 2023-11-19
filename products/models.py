from django.db import models

# Create your models here.

class Category(models.Model): 
    class Meta:
        verbose_name_plural = 'Categories'
        
    name = models.CharField(max_length=50)
    friendly_name = models.CharField(max_length=50, null=True, blank=False)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model): 
    category = models.ForeignKey('Category', null=True, blank=False, on_delete=models.SET_NULL)
    name = models.CharField(max_length=50)
    description = models.TextField()
    has_sizes = models.BooleanField(default=False, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=False)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=False)
    image_url = models.URLField(max_length=1000, null=True, blank=False)
    image = models.ImageField(null=True, blank=False)


    def __str__(self):
        return self.name