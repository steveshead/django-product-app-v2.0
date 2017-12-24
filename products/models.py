from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.validators import FileExtensionValidator
from django.core import validators
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
import os


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    biography = models.TextField(max_length=500, blank=True, default='Tell us about you...')
    tagline = models.CharField(max_length=200, blank=True, default=' ')
    image = models.ImageField(upload_to='profile_image', blank=True)

    def __str__(self):
        return ' '


def get_image_path(instance, filename):
    return '/'.join(['product_images', str(instance.name), filename])


product_types = (
    ('Choose','Choose'),
    ('T-Shirt','T-Shirt'),
    ('PSD Template','PSD Template'),
    ('HTML Website', 'HTML Website'),
    ('Python','Python'),
    ('Other','Other')
)


class Product(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    url = models.CharField(max_length=200, blank=True)
    product_type = models.CharField(max_length=15, choices=product_types, default='choose')
    image = models.ImageField(upload_to='product_images', blank=True, null=True)
    image_url = models.CharField(max_length=200, blank=True)
    product_file = models.FileField(upload_to='product_files', blank=True, null=True, validators=[FileExtensionValidator(['zip'])])
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('index', kwargs={})


def _delete_file(path):
    # Deletes file from filesystem.
    if os.path.isfile(path):
        os.remove(path)


@receiver(pre_delete, sender=Product)
def delete_assets(sender, instance, *args, **kwargs):
    if instance.image:
        _delete_file(instance.image.path)
    if instance.product_file:
        _delete_file(instance.product_file.path)
