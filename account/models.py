from django.contrib.auth.models import User
from django.db import models


# Relacionamento entre conta e usuario
class Account(models.Model):
    SEXO = [
        (0, 'Não informar'),
        (1, 'Feminino'),
        (2, 'Masculino')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    url_site = models.CharField(max_length=100, null=True)
    sexo = models.IntegerField(choices=SEXO, null=True)

    def __str__(self):
        return self.user.username

