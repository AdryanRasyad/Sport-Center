import uuid
from django.db import models

class Items(models.Model):
    CATEGORY_CHOICES = [
        ('footwear', 'Footwear'),
        ('clothing', 'Clothing'),
        ('accessories', 'Accessories'),
        ('limited_collection', 'Limited Collection'),
    ]
    
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    thumbnail = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=255)
    is_featured = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    