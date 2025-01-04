from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver


# class Phone(models.Model):
#     name = models.CharField(max_length=100, null=False)
#     image = models.URLField()
#     price = models.IntegerField()
#     release_date = models.DateField()
#     lte_exists = models.BooleanField()
#     slug = models.SlugField(max_length=100, unique=True)
class Phone(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=60)
    image = models.URLField()
    price = models.IntegerField()
    release_date = models.DateField(blank=True, null=True)
    lte_exists = models.BooleanField()
    slug = models.SlugField(unique=True, blank=True, max_length=100)

    def __str__(self):
        return f'{self.name}'


@receiver(pre_save, sender=Phone)
def pre_save_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)


