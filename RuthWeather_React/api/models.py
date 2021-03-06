from django.db import models

# Create your models here.

class City(models.Model):
    name = models.CharField(max_length=25,default='York, GB')
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'cities'

#####################################################

class Am(models.Model):
    date = models.DateField(auto_now=True,null=True)
    temp = models.IntegerField(null=True)
    prec = models.PositiveIntegerField(null=True)

    def __str__(self):
        return f"Weather for {self.date} (morning)"


class Pm(models.Model):
    date = models.DateField(auto_now=True,null=True)
    temp = models.IntegerField(null=True)
    prec = models.PositiveIntegerField(null=True)

    def __str__(self):
        return f"Weather for {self.date} (afternoon)"


class Eve(models.Model):
    date = models.DateField(auto_now=True,null=True)
    temp = models.IntegerField(null=True)
    prec = models.PositiveIntegerField(null=True)

    def __str__(self):
        return f"Weather for {self.date} (evening)"


class Report(models.Model):
    date = models.DateField(auto_now=True,null=True)
    city = models.ForeignKey(City,on_delete=models.CASCADE, null=True)
    outlook = models.CharField(max_length=300,null=True)
    eve_temp = models.IntegerField(null=True)
    am = models.ForeignKey(Am,on_delete=models.CASCADE,null=True)
    pm = models.ForeignKey(Pm,on_delete=models.CASCADE,null=True)
    eve = models.ForeignKey(Eve,on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Report for {self.date}"
