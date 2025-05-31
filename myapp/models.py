from django.db import models
# Create your models here.
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default="")
    phone = models.CharField(max_length=15, default="")
    email = models.CharField(max_length=50, default="")

    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        blank=True,
        null=True,
    )


    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.userprofile.save()

#@receiver(post_save, sender=User)
#def create_or_update_user_profile(sender, instance, created, **kwargs):
   # if created:
    #    from .models import UserProfile
    #    UserProfile.objects.create(user=instance)
    #instance.userprofile.save()




class Contact(models.Model):
    contact_id= models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    remarks = models.CharField(max_length=5000)
    phone = models.CharField(max_length=70)
    email = models.CharField(max_length=50)

    def __str__(self):
        return self.name





class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    destination = models.CharField(max_length=100)
    checkin = models.DateField()
    checkout = models.DateField()
    guests = models.PositiveIntegerField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} - {self.destination}"

class Destination(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    place = models.CharField(max_length=100, default="")
    rating = models.CharField(max_length=50)
    views = models.CharField(max_length=50)
    description = models.TextField()
    wow = models.TextField()
    woww = models.TextField()
    wowww = models.TextField()
    location = models.CharField(max_length=100)
    image = models.ImageField(upload_to='destinations/', blank=True, null=True)
    para = models.TextField(null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True)
    price = models.CharField(max_length=50, default='')

    def __str__(self):
        return self.name

class Feedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    remarks = models.CharField(max_length=5000)
    phone = models.CharField(max_length=70)
    email = models.CharField(max_length=50)
    rating = models.CharField(max_length=50)
    visit_date = models.DateField(max_length=50)
    best_part = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Hotels(models.Model):
    name = models.CharField(max_length=200)
    price = models.CharField(max_length=100)
    image = models.ImageField(upload_to='hotels/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    ratings = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Restaurants(models.Model):
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    ratings = models.CharField(max_length=100, null=True, default='5', blank=True)
    price = models.CharField(max_length=100)
    image = models.ImageField(upload_to='hotels/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
