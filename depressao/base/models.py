from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return self.name


class Configs(models.Model):
    FUNCAO_TRANSFERENCIA = (
        ('SG', 'Sigmóide'),
        ('TH', 'Tangente Hiperbólica'),)

    INTERVALOS = (
        ('1', '[0, 1]'),
        ('2', '[-1, 0]'),
        ('3', '[-1, 1]'),
        ('4', '[-0.1, 0.1]'),)

    bias = models.BooleanField(default=False)
    momento = models.BooleanField(default=False)
    funcao_transferencia = models.CharField(
        max_length=1, choices=FUNCAO_TRANSFERENCIA, default='SG')
    intervalo = models.CharField(
        max_length=1, choices=INTERVALOS, default='1')

    def __str__(self):
        return "Config: ({}, {}, {}, {})".format(
            self.bias, self.momento, self.funcao_transferencia, self.intervalo)
