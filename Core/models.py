from django.db import models
from django.contrib.auth.models import User

# Create your models here.




class Center(models.Model):
    ref_number = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    num_students = models.IntegerField(default=0)
    def __str__(self):
        return self.name


class Student(models.Model):
    ref_number = models.CharField(max_length=10, unique=True)
    full_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=10)
    email = models.EmailField()
    date_of_birth = models.DateField()
    preferred_location = models.CharField(max_length=100)
    street_address = models.CharField(max_length=200)
    state = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    guardian_name = models.CharField(max_length=100)
    guardian_phone_number = models.CharField(max_length=20)
    id_proof = models.ImageField(upload_to='id_proof/')
    age_group = models.CharField(max_length=100)
    mode_of_travel = models.CharField(max_length=100)
    football_playing_position = models.CharField(max_length=100)
    center = models.ForeignKey(Center, on_delete=models.CASCADE)
    # education
    school_Name = models.CharField(max_length=75,null=True)
    school_Address = models.CharField(max_length=100,null=True)
    study_Standard = models.IntegerField(null=True)
    study_Devision = models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.full_name


class Coordinator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    primary_mobile = models.CharField(max_length=20)
    secondary_mobile = models.CharField(max_length=20)
    place = models.CharField(max_length=100)
    centers = models.ManyToManyField(Center)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    def center1_name(self):
        try:
            return self.centers.all()[0].name
        except IndexError:
            return ""

    def center2_name(self):
        try:
            return self.centers.all()[1].name
        except IndexError:
            return ""
