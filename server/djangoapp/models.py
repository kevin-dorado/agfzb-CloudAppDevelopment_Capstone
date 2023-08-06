from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _




# Creamos el modelo CarMake para guardar datos sobre una marca de coche
class CarMake(models.Model):
    # Definimos los campos que queremos incluir
    name = models.CharField(max_length=50, verbose_name=_("name")) # El nombre de la marca
    description = models.TextField(verbose_name=_("description")) # Una descripción de la marca
    # Puedes añadir otros campos que te interesen, como el país de origen, el logo, etc.

    # Definimos el método __str__ para imprimir un objeto CarMake
    def __str__(self):
        return f"{self.name}: {self.description}"

    # Definimos los metadatos del modelo
    class Meta:
        verbose_name = _("car make")
        verbose_name_plural = _("car makes")

# Creamos una enumeración para los tipos de coche posibles
class CarType(models.TextChoices):
    SEDAN = 'sedan', _('Sedan')
    SUV = 'suv', _('SUV')
    WAGON = 'wagon', _('Wagon')

# Creamos el modelo CarModel para guardar datos sobre un modelo de coche
class CarModel(models.Model):
    # Definimos los campos que queremos incluir
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE, related_name="car_models", verbose_name=_("car make")) # Una relación muchos a uno con el modelo CarMake
    dealer_id = models.IntegerField(verbose_name=_("dealer id")) # Un campo entero que hace referencia a un concesionario creado en la base de datos Cloudant
    name = models.CharField(max_length=50, verbose_name=_("name")) # El nombre del modelo
    type = models.CharField(max_length=10, choices=CarType.choices, default=CarType.SEDAN, verbose_name=_("type")) # El tipo de coche, con opciones limitadas por la enumeración CarType
    year = models.DateField(verbose_name=_("year")) # El año de fabricación del coche
    # Puedes añadir otros campos que te interesen, como el color, la potencia, el precio, etc.

    # Definimos el método __str__ para imprimir un objeto CarModel
    def __str__(self):
        return f"{self.car_make.name} {self.name} ({self.type}) - {self.year}"

    # Definimos los metadatos del modelo
    class Meta:
        verbose_name = _("car model")
        verbose_name_plural = _("car models")


























# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object


# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
