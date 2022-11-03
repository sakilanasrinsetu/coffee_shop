from django.db import models

# Create your models here.


# ............***............ Slider ............***............

class Slider(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to='slider',
                            null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# ............***............ About Us ............***............

class AboutUs(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# ............***............ Gallery ............***............


class Gallery(models.Model):
    title = models.CharField(max_length=250)
    image = models.FileField(upload_to='gallery',
                             null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# ............***............ Owner Information ............***............


class OwnerInformation(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    image = models.FileField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# ............***............ Blog ............***............


class Blog(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    image = models.FileField(upload_to='blog',
                             null=True, blank=True)
    serial_no = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# ............***............ How to Arabika Work ............***............


class ArabikaWork(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# ............***............ Arabika History ............***............


class ArabikaHistory(models.Model):
    title = models.CharField(max_length=250)
    serial_no = models.CharField(max_length=20)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title