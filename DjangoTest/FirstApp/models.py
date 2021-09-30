from django.db import models

# creamos el modelo Animals para guardar información de estos objectos en la base de
# datos que maneja Django internamente.
class Animals(models.Model):
    name = models.CharField(max_length=50)
    weight = models.IntegerField()
