from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class License(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Пользователь'))
    license_key = models.CharField(max_length=255, unique=True, verbose_name=_('Ключ лицензии'))
    expiry_date = models.DateField(verbose_name=_('Дата окончания'))
    is_active = models.BooleanField(default=True, verbose_name=_('Активна'))

    class Meta:
        verbose_name = _('Лицензию')
        verbose_name_plural = _('Лицензии')

    def __str__(self):
        return self.license_key


class Statistics(models.Model):
    full_name = models.CharField(max_length=255, verbose_name=_('ФИО'))
    date = models.DateTimeField(verbose_name=_('Дата и время прохождения теста'))  # Изменено на DateTimeField
    time = models.CharField(max_length=5, verbose_name=_('Время прохождения'), help_text=_("Формат: ММ:СС"))  # Изменено на CharField с примером


    respirator_provided = models.BooleanField(default=False, verbose_name=_('Выдан самоспасатель'))
    headlamp_provided = models.BooleanField(default=False, verbose_name=_('Выдана головная лампа'))
    respirator_used = models.BooleanField(default=False, verbose_name=_('Использован самоспасатель'))
    phone_message = models.BooleanField(default=False, verbose_name=_('Сообщил о ЧС'))

    class Meta:
        verbose_name = _('Статистику')
        verbose_name_plural = _('Статистики')

    def __str__(self):
        return self.full_name