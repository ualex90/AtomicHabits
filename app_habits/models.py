from django.db import models

from app_users.models import NULLABLE
from config import settings
from django.utils.translation import gettext_lazy as _


class Periodicity(models.TextChoices):
    DAY_1 = 1, _('1 Day')
    DAY_2 = 2, _('2 Day')
    DAY_3 = 3, _('3 Day')
    DAY_4 = 4, _('4 Day')
    DAY_5 = 5, _('5 Day')
    DAY_6 = 6, _('6 Day')
    DAY_7 = 7, _('7 Day')


class Habit(models.Model):
    # Создатель привычки
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('Owner'),
        **NULLABLE
    )
    # Действие привычки
    task = models.TextField(
        verbose_name=_('Task')
    )
    # Время начала выполнения. ДЛЯ ПОЛЕЗНОЙ привычки
    start_time = models.TimeField(
        verbose_name=_('Time for task'),
        **NULLABLE
    )
    # Место выполнения действия
    location = models.CharField(
        max_length=50,
        verbose_name=_('Task location')
    )
    # Признак приятной привычки
    is_nice_habit = models.BooleanField(
        default=False,
        verbose_name=_('Is nice habit')
    )
    # Привязка приятной привычки, только ДЛЯ ПОЛЕЗНОЙ привычки
    related_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        verbose_name=_('Related nice habit'),
        **NULLABLE
    )
    # Периодичность. Минимум - 1 день, максимум - 7 дней с шагом в 1 день ДЛЯ ПОЛЕЗНОЙ привычки
    periodicity = models.CharField(
        default=Periodicity.DAY_1,
        max_length=2,
        choices=Periodicity.choices,
        verbose_name=_('Periodicity'),
        **NULLABLE
    )
    # Вознаграждение ДЛЯ ПОЛЕЗНОЙ привычки
    reward = models.CharField(
        max_length=50,
        verbose_name="Reward for tasks",
        **NULLABLE
    )
    # Продолжительность выполнения задачи (не более 120 секунд)
    lead_time = models.SmallIntegerField(
        default=60,
        verbose_name=_("Lead time")
    )
    # Признак публичности. При установке привычку видят все пользователи.
    is_public = models.BooleanField(
        default=False,
        verbose_name="Is public"
    )
