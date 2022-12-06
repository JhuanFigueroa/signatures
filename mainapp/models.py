from django.db import models

# Create your models here.

class User(models.Model):
    """Model definition for User."""
    nombre=models.CharField(max_length=50)
    apellido=models.CharField(max_length=50)
    email=models.CharField(max_length=100) 
    firma = models.FileField(null=True)

    class Meta:
        """Meta definition for User."""

        verbose_name = 'User'
        verbose_name_plural = 'Users'
