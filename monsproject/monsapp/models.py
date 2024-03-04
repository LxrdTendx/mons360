from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Название продукта'))
    file = models.FileField(upload_to='products/%Y/%m/%d/', verbose_name=_('Файл продукта'), null=True, blank=True)  # Путь, куда будут сохраняться файлы
    release_date = models.DateTimeField(verbose_name=_('Дата и время релиза'), null=True, blank=True)  # Изменено на DateTimeField
    version = models.CharField(max_length=20, verbose_name=_('Версия'), null=True, blank=True)
    class Meta:
        verbose_name = _('Продукт')
        verbose_name_plural = _('Продукты')

    def __str__(self):
        return self.name


class License(models.Model):
    LICENSE_TYPES = (
        ('regular', _('Регулярная')),
        ('unlimited', _('Бессрочная')),
        # Add more types as needed
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Пользователь'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт', related_name='licenses', null=True)
    license_type = models.CharField(max_length=50, choices=LICENSE_TYPES, default='regular', verbose_name=_('Тип лицензии'))
    license_key = models.CharField(max_length=255, unique=True, verbose_name=_('Ключ лицензии'))
    expiry_date = models.DateField(null=True, blank=True, verbose_name=_('Дата окончания'))  # Allow null for unlimited licenses
    is_active = models.BooleanField(default=True, verbose_name=_('Активна'))

    class Meta:
        verbose_name = _('Лицензию')
        verbose_name_plural = _('Лицензии')

    def __str__(self):
        return "{} - {}".format(self.license_key, self.get_license_type_display())


class Statistics(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт', related_name='statistics', null=True)
    full_name = models.CharField(max_length=255, verbose_name='ФИО')
    date = models.DateTimeField(verbose_name='Дата и время прохождения теста')
    time = models.CharField(max_length=5, verbose_name='Время прохождения', help_text="Формат: ММ:СС")
    respirator_provided = models.BooleanField(default=False, verbose_name='Выдан самоспасатель')
    headlamp_provided = models.BooleanField(default=False, verbose_name='Выдана головная лампа')
    respirator_used = models.BooleanField(default=False, verbose_name='Использован самоспасатель')
    phone_message = models.BooleanField(default=False, verbose_name='Сообщил о ЧС')

    class Meta:
        verbose_name = 'Статистику Mons360'
        verbose_name_plural = 'Статистика Mons360'

    def __str__(self):
        return f"{self.product.name if self.product else 'Без продукта'} - {self.full_name}"