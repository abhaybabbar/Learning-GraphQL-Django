from tabnanny import verbose
from django.db import models

# Create your models here.
class Books(models.Model):
    title = models.CharField(max_length=100)
    excerpt = models.TextField()
    
    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"
        
    def __str__(self):
        return self.title