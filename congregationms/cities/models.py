from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name


class State(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    import_code = models.CharField(max_length=10, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
