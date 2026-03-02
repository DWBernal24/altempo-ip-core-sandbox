from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True, max_length=500)

    def __str__(self):
        return self.name


class Category(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    name = models.CharField(max_length=100, unique=True)
    display_name = models.CharField(max_length=100, unique=True, blank=True, null=True)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name="categories")
    description = models.TextField(blank=True, null=True, max_length=500)
    image = models.ImageField(upload_to='services/categories/', blank=True, null=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    name = models.CharField(max_length=150, unique=True)
    display_name = models.CharField(max_length=100, unique=True, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="items")
    category_name = models.ForeignKey(Category, on_delete=models.CASCADE, to_field="name", blank=True, null=True)
    description = models.TextField(blank=True, null=True, max_length=500)
    image = models.ImageField(upload_to='orders/items/', blank=True, null=True)

    def __str__(self):
        return self.name


class SpecificService(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    name = models.CharField(max_length=150, unique=True)
    display_name = models.CharField(max_length=100, unique=False, blank=True, null=True)
    item_name = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="specific_services", to_field="name", blank=True, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True, max_length=500)
    image = models.ImageField(upload_to='orders/specific_services/', blank=True, null=True)


    """
        Example:
        {
            "extra_fields": [
                {
                  "field_key": "musician_voice_type",
                  "fiel_display_name": "Tipo de voz requerida",
                  "field_type": "select",
                  "model": "core.MusicianVoiceType",
                  "api_url": "musician-voices-types/"
                },
                {
                  "field_key": "vocal_style",
                  "fiel_display_name": "Estilo de canto",
                  "field_type": "select",
                  "model": "core.VocalStyle",
                  "api_url": "vocal-styles/"
                },
                {
                  "field_key": "quantity",
                  "fiel_display_name": "Cantidad de vocalista solista",
                  "field_type": "number",
                  "model": "",
                  "api_url": ""
                },
                {
                  "field_key": "instruments",
                  "fiel_display_name": "Tipo de instrumento requerido",
                  "field_type": "select",
                  "model": "core.Instrument",
                  "api_url": "instruments/"
                }
            ]
        }
    """
    extra_fields = models.JSONField(default=dict, null=True, blank=True)

    def __str__(self):
        return self.name


class ServiceMode(models.Model):
    VIRTUAL = 'virtual'
    ON_SITE = 'on_site'

    name = models.CharField(max_length=20, unique=True)
    display_name = models.CharField(max_length=100, unique=True, blank=True, null=True)

    def __str__(self):
        return self.name

class PricingInterval(models.Model):
    duration = models.PositiveIntegerField()
    unit = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_base = models.BooleanField(default=False)

    # the service related to these pricing intervals
    music_project_service = models.ForeignKey('musicians.MusicProjectService', on_delete=models.CASCADE, related_name="pricing_intervals", null=True, blank=True)

    def __str__(self):
        return f"{self.duration} {self.unit}"



"""
Attribute class of the taxonomy has been left out for better information
management inside the same "MusicProjectService" table.
This means that any fields related to a personalized structure for each service
lives inside that table directly, and can be queried using JSON.
"""
class Attribute(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    name = models.CharField(max_length=100, unique=True, db_index=True)
    display_name = models.CharField(max_length=100, unique=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True, max_length=500)
    specific_service = models.ForeignKey(SpecificService, on_delete=models.CASCADE, related_name="attributes", to_field="name")

    def __str__(self):
        return self.name
