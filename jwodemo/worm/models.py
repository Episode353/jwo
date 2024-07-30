from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

class Worm(models.Model):
    # Automatically created unique identifier for each Worm
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    
    # Boolean field to indicate if the worm is alive (True) or dead (False)
    is_alive = models.BooleanField(default=True)

    # The Number of times the worm was revived.
    times_revived = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(9), MinValueValidator(0)]
    )

    # Setting up fields with max 10 and min 0 constraints
    health = models.PositiveIntegerField(
        default=5,
        validators=[MaxValueValidator(10), MinValueValidator(0)]
    )
    
    sleep = models.PositiveIntegerField(
        default=5,
        validators=[MaxValueValidator(10), MinValueValidator(0)]
    )
    
    hunger = models.PositiveIntegerField(
        default=5,
        validators=[MaxValueValidator(10), MinValueValidator(0)]
    )
    
    happiness = models.PositiveIntegerField(
        default=5,
        validators=[MaxValueValidator(10), MinValueValidator(0)]
    )
    
    # Badge Variable
    badge = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(10), MinValueValidator(0)]
    )

    # Timestamps for various activities
    last_fed = models.DateTimeField(null=True, blank=True)
    last_slept = models.DateTimeField(null=True, blank=True)
    last_played = models.DateTimeField(null=True, blank=True)
    
    # Created at timestamp
    created_at = models.DateTimeField(default=timezone.now)
    # Updated at timestamp
    updated_at = models.DateTimeField(auto_now=True)
    # Time of death timestamp
    time_of_death = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Worm {self.id} - {self.name or 'Unnamed'}"

    class Meta:
        ordering = ['id']
