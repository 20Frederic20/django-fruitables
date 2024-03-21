from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name.lower())
        super(Category, self).save(*args, **kwargs)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"


class Product(models.Model):
    class TypeProduct(models.TextChoices):
     # Actual value ↓      # ↓ Displayed on Django Admin
        ORGANIC = 'Or', 'Organic'
        FRESH = 'Fa', 'Fresh'
        SALES = 'Sa', 'Sales'
        DISCOUNT = 'Di', 'Discount'
        EXPIRED = 'Ex', 'Expired'
        OTHER = 'Ot', 'Other'
        UNKNOWN = 'Un', 'Unknown'

    name = models.CharField(max_length=255)
    price = models.FloatField(max_length=10, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="tmp/", blank=True, null=True)
    type = models.CharField(
        max_length=255, choices=TypeProduct, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Products"
