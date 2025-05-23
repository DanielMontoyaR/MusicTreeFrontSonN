from django.db import models

# Create your models here.
class TodoItem(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)

class ClusterGenero(models.Model):
    cluster_id = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=300)
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=30)
    
    
    

