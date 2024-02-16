from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class License(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Пользователь'))
    license_key = models.CharField(max_length=255, unique=True, verbose_name=_('Ключ лицензии'))
    expiry_date = models.DateField(verbose_name=_('Дата окончания'))
    is_active = models.BooleanField(default=True, verbose_name=_('Активна'))

    class Meta:
        verbose_name = _('Лицензия')
        verbose_name_plural = _('Лицензии')

    def __str__(self):
        return self.license_key
