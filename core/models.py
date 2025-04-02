from django.db import models
from django.contrib.auth.models import User

# Ejemplo de modelo
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Agrega los campos que necesites