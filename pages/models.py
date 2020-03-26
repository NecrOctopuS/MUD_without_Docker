from django.db import models


class Room(models.Model):
    name = models.CharField('название комнаты', max_length=200)
    description = models.TextField('описание комнаты', )
    items = models.ManyToManyField('Item', verbose_name='предметы в комнате', blank=True, related_name='in_rooms')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Комната'
        verbose_name_plural = 'Комнаты'


class Character(models.Model):
    name = models.CharField('имя', max_length=200)
    room = models.ForeignKey('Room', verbose_name='комната, где находится персонаж', on_delete=models.CASCADE,
                             related_name='chars')
    items = models.ManyToManyField('Item', verbose_name='предметы в инвентаре', blank=True, related_name='in_inventory')

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField('название предмета', max_length=200)

    def __str__(self):
        return self.name
