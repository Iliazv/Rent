from django.db import models
from django.contrib.humanize.templatetags import humanize
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from django.utils import timezone
import datetime


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def get_name(self):
        return self.username


class Annoucement(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='announcements')
    date = models.DateTimeField('Created')
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=60)
    category = models.CharField(max_length=60)
    title = models.CharField(max_length=200)
    price = models.IntegerField()
    address = models.CharField(max_length=150)
    area = models.IntegerField(default=0)
    district = models.CharField(max_length=40, default='Центральный')
    ceil = models.IntegerField()
    ceilings = models.IntegerField(default=5)
    description = models.TextField(max_length=1000)
    building_year = models.CharField(max_length=20, default='')
    type = models.CharField(max_length=50, default='')
    heating = models.CharField(max_length=50, default='')
    main_image = models.ImageField(upload_to = 'announcement_images/', blank = True)

    def __str__(self):
        return self.title

    def get_url(self):
            try:
                 return self.main_image.url
            except IOError:
                 return None

    def slice_description(self):
        description = self.description
        sliced_description, counter_point, counter_comma = '', 0, 0
        for elem in description:
            if counter_point == 2 or counter_comma == 5:
                break
            elif elem == '.' or elem == '!':
                sliced_description += elem
                counter_point += 1
            elif elem == ',':
                sliced_description += elem
                counter_comma += 1
            else:
                sliced_description += elem
        return sliced_description

    def slice_address(self):
        address = self.address
        sliced_address, general_counter = '', 0
        for elem in address:
            if general_counter == 3: break
            elif elem == ',' or elem == '.':
                sliced_address += elem
                general_counter += 1
            else: sliced_address += elem
        return sliced_address

    def get_date(self):
        return humanize.naturaltime(self.date)


class Picture(models.Model):
    annoucement = models.ForeignKey(Annoucement, on_delete=models.CASCADE, related_name='pictures')
    image = models.ImageField(upload_to = 'announcement_images/', blank = True)

    def __str__(self):
        return self.annoucement.title


class Favorite(models.Model):
    annoucement = models.ForeignKey(Annoucement, on_delete=models.CASCADE, related_name='favorites')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')


    class Meta:
        unique_together = [['annoucement', 'user']]

    def __str__(self):
        return self.annoucement.title


class Compilation(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='compilations')
    title = models.CharField(max_length=45)
    favorite = models.ManyToManyField(Annoucement, related_name='saved_favorites')

    def __str__(self):
        return self.title


class Chat(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='renters')
    reciever = models.ForeignKey(User, on_delete=models.CASCADE, related_name='landlords')
    creation_date = models.DateTimeField('Created')

    def __str__(self):
        return str(self.sender) + ' + ' + str(self.reciever)


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='senders')
    message = models.TextField(max_length=1000)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.writer) + ' - ' + self.message[:20]