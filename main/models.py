import uuid
from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('footwear', 'Footwear'),
        ('clothing', 'Clothing'),
        ('accessories', 'Accessories'),
        ('limited_collection', 'Limited Collection'),
    ]


    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    thumbnail = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=255, choices=CATEGORY_CHOICES, default='update')
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return self.title
    