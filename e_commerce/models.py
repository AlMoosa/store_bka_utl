import itertools
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

User = get_user_model()


class SortCategories(MPTTModel):
    name = models.CharField(max_length=20, verbose_name='Name')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=256)
    price = models.PositiveIntegerField()
    category = models.ManyToManyField(SortCategories, related_name='items')
    in_basket = models.ManyToManyField('Basket', related_name='item_basket')

    def __str__(self):
        return self.name


class ColorOfItem(models.Model):
    name = models.CharField(max_length=32)
    amount = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    item = models.ForeignKey(Item, on_delete=models.CASCADE, blank=True,
                             null=True, related_name='colors')
    in_basket = models.ManyToManyField('Basket', related_name='color_basket')

    def __str__(self):
        return self.name


class SizeOfItem(models.Model):
    name = models.CharField(max_length=32)
    amount = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    item = models.ForeignKey(Item, on_delete=models.CASCADE,
                             blank=True, null=True, related_name='sizes')
    in_basket = models.ManyToManyField('Basket', related_name='size_basket')

    def __str__(self):
        return self.name


class Basket(models.Model):
    user = models.OneToOneField(User, related_name='basket', on_delete=models.CASCADE)


@receiver(post_save, sender=User)
def create_user_basket(sender, instance, created, **kwargs):
    if created:
        Basket.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_basket(sender, instance, **kwargs):
    instance.basket.save()


class Order(models.Model):

    DELIVERY_CHOICES = {
        (1, 'In 1 day'),
        (2, 'In 3 days'),
        (3, 'In a week'),
        (4, 'In a month'),
        (5, 'When my grandson is born')
    }
    delivery = models.IntegerField(choices=DELIVERY_CHOICES, default=3)
    slug = models.SlugField(max_length=50, blank=True)
    total_price = models.PositiveIntegerField()
    basket = models.ForeignKey(Basket, on_delete=models.SET_NULL, blank=True, null=True)

    def _generate_slug(self):
        max_length = self._meta.get_field('slug').max_length
        value = self.basket.user.username
        slug_candidate = slug_original = slugify(value, allow_unicode=True)
        for i in itertools.count(1):
            if not Order.objects.filter(slug=slug_candidate).exists():
                break
            slug_candidate = '{}-{}'.format(slug_original, i)

        self.slug = slug_candidate

    def save(self, *args, **kwargs):
        if not self.pk:
            self._generate_slug()

        super().save(*args, **kwargs)
