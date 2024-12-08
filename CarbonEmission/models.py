import random
import string
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import transaction


class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=6, unique=True)  # 6-digit token field
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        with transaction.atomic():
            # Ensure no active token exists for this user
            PasswordResetToken.objects.select_for_update().filter(
                user=self.user, is_used=False
            ).update(is_used=True)

            # Generate a new token if necessary
            if not self.token:
                self.token = self.generate_confirmation_code()
            super().save(*args, **kwargs)

    def generate_confirmation_code(self, length=6):
        """Generate a 6-digit confirmation code."""
        return ''.join(random.choices(string.digits, k=length))  # Only digits

    def is_valid(self):
        """Check if the token is valid (valid for 10 minutes and not used)."""
        return (timezone.now() - self.created_at).total_seconds() < 600 and not self.is_used

    def __str__(self):
        return f"Token for {self.user.username}: {self.token}"


class EmissionFactor(models.Model):
    category = models.CharField(max_length=50)
    sub_category = models.CharField(max_length=50)
    factor = models.FloatField(help_text="Emission factor per unit")

    class Meta:
        unique_together = ('category', 'sub_category')

    def __str__(self):
        return f"{self.category} - {self.sub_category} : {self.factor}"


class UserActivity(models.Model):
    CATEGORY_CHOICES = [
        ('Transport', 'Transportation'),
        ('Buildings', 'Buildings'),
        ('Industry', 'Industry'),
    ]

    SUBCATEGORY_CHOICES = {
        'Transport': [('Car', 'Car'), ('Bus', 'Bus'), ('Train', 'Train')],
        'Buildings': [('Electricity', 'Electricity'), ('Heating', 'Heating')],
        'Industry': [('Manufacturing', 'Manufacturing'), ('Construction', 'Construction')],
    }

    UNIT_CHOICES = {
        'Car': 'KM',
        'Bus': 'KM',
        'Train': 'KM',
        'Electricity': 'KWH',
        'Heating': 'KWH',
        'Manufacturing': 'Units',
        'Construction': 'Hours',
    }

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    sub_category = models.CharField(max_length=100)
    quantity = models.FloatField()
    unit = models.CharField(max_length=50, default='KM')  # Default value for the unit field
    date = models.DateTimeField(auto_now_add=True)
    version = models.IntegerField(default=0)  # For optimistic locking

    def calculate_emission(self):
        # Emission factors for each subcategory (in kg CO2 per unit)
        emission_factors = {
            'Car': 0.2,         # 0.2 kg CO2 per km
            'Bus': 0.05,        # 0.05 kg CO2 per km
            'Train': 0.01,      # 0.01 kg CO2 per km
            'Electricity': 0.4, # 0.4 kg CO2 per kWh
            'Heating': 0.15,    # 0.15 kg CO2 per kWh
            'Manufacturing': 2.0,  # 2 kg CO2 per unit
            'Construction': 0.5,   # 0.5 kg CO2 per hour
        }

        # Calculate emission based on the sub_category and quantity
        emission_factor = emission_factors.get(self.sub_category, 0)
        emission = emission_factor * self.quantity
        emission = round(emission, 2)
        return emission

    def save(self, *args, **kwargs):
        with transaction.atomic():
            # Optimistic locking: Ensure the version hasn't changed
            if self.pk:
                current = UserActivity.objects.select_for_update().get(pk=self.pk)
                if current.version != self.version:
                    raise ValueError("The record has been updated by another transaction.")
                self.version += 1

            # Automatically set the unit based on sub_category
            if not self.unit and self.sub_category in self.UNIT_CHOICES:
                self.unit = self.UNIT_CHOICES[self.sub_category]

            super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'category', 'sub_category', 'date'],
                name='unique_user_activity'
            )
        ]
        indexes = [
            models.Index(fields=['user', 'category', 'sub_category']),
            models.Index(fields=['date']),
        ]

    def __str__(self):
        return f"{self.category} - {self.sub_category} - {self.quantity} {self.unit}"

class SubCategoryEffect(models.Model):
    category = models.CharField(max_length=50)
    sub_category = models.CharField(max_length=50)
    effect_title = models.CharField(max_length=100)
    effect_description = models.TextField()

    class Meta:
        unique_together = ('category', 'sub_category', 'effect_title')

    def __str__(self):
        return f"{self.category} - {self.sub_category}: {self.effect_title}"


class SubCategorySolution(models.Model):
    category = models.CharField(max_length=50)
    sub_category = models.CharField(max_length=50)
    solution_title = models.CharField(max_length=100)
    solution_description = models.TextField()

    class Meta:
        unique_together = ('category', 'sub_category', 'solution_title')

    def __str__(self):
        return f"{self.category} - {self.sub_category}: {self.solution_title}"



class StepCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)  # e.g., Transport, Buildings, Industry
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class StepSubCategory(models.Model):
    category = models.ForeignKey(StepCategory, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=100)  # e.g., Car, Bus, Electricity
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.category.name})"

class Step(models.Model):
    sub_category = models.ForeignKey(StepSubCategory, on_delete=models.CASCADE, related_name='steps')
    case = models.CharField(max_length=50)  # e.g., Good, Average, Poor
    description = models.TextField()  # Details of the step

    def __str__(self):
        return f"{self.case} - {self.sub_category.name}"