from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
class Weights(models.model):
    user_id = models.IntegerField(db_index=True)
    weight_value = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(500)])
    weight_type = models.CharField(choices=[("kg", "kg"), ("lb", "lb")], default="kg")
    date_recored = models.DateField(default=timezone.now, db_index=True)
    note = models.CharField(max_length=255, blank=True)
    class Meta:
        ordering = ["-date_recorded"]
        indexes = [models.Index(fields=["user_id", "date_recorded"])]
