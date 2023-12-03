from django.db import models

from app_users.models import NULLABLE
from config import settings
from django.utils.translation import gettext_lazy as _


class Periodicity(models.TextChoices):
    DAY_1 = 'D1', _('1 Day')
    DAY_2 = 'D2', _('2 Day')
    DAY_3 = 'D3', _('3 Day')
    DAY_4 = 'D4', _('4 Day')
    DAY_5 = 'D5', _('5 Day')
    DAY_6 = 'D6', _('6 Day')
    DAY_7 = 'D7', _('7 Day')


class LeadTime(models.TextChoices):
    SEC_10 = 'S10', _('10 Second')
    SEC_20 = 'S20', _('20 Second')
    SEC_30 = 'S30', _('30 Second')
    SEC_40 = 'S40', _('40 Second')
    SEC_50 = 'S50', _('50 Second')
    SEC_60 = 'S60', _('60 Second')
    SEC_70 = 'S70', _('70 Second')
    SEC_80 = 'S80', _('80 Second')
    SEC_90 = 'S90', _('90 Second')
    SEC_100 = 'S100', _('100 Second')
    SEC_110 = 'S110', _('110 Second')
    SEC_120 = 'S120', _('120 Second')


class Habit(models.Model):
    # Создатель привычки
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              verbose_name=_('Owner'), **NULLABLE)

    # Действие привычки
    task = models.TextField(verbose_name=_('Task'))

    # Время начала выполнения. По умолчанию 12:00
    start_time = models.TimeField(default="12:00", verbose_name=_('Time for task'))

    # Место выполнения действия
    location = models.CharField(max_length=50, verbose_name=_('Task location'))

    # Признак приятной привычки
    is_nice_habit = models.BooleanField(verbose_name=_('Is nice habit'))

    # Привязка приятной привычки, только ДЛЯ ПОЛЕЗНОЙ привычки
    related_habit = models.ForeignKey('self', on_delete=models.SET_NULL,
                                      verbose_name=_('Related nice habit'), **NULLABLE)

    # Периодичность. Минимум - день, максимум - 6 дней с шагом в 1 день
    periodicity = models.CharField(default=Periodicity.DAY_1, max_length=2, choices=Periodicity.choices,
                                   verbose_name=_('Periodicity'))

    # Вознаграждение ДЛЯ ПОЛЕЗНОЙ привычки
    reward = models.CharField(max_length=50, verbose_name="Reward for tasks", **NULLABLE)

    # Продолжительность выполнения задачи (не более 120 секунд. Устанавливается с шагом в 10 секунд)
    lead_time = models.TimeField(default=LeadTime.SEC_60, max_length=4, choices=LeadTime.choices,
                                 verbose_name=_("Lead time"))

    # Признак публичности. При установке привычку видят все пользователи.
    is_public = models.BooleanField(default=False, verbose_name="Is public")
