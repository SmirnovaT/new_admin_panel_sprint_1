from django.db import models
import uuid


class TimeStampedMixin(models.Model):
    "Класс-миксин для Даты создания и Даты редактирования."
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CreatedTimeStampedMixin(models.Model):
    "Класс-миксин для Даты создания."
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    "Класс-миксин для id."
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True
