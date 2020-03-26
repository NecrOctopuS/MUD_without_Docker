from django.test import TestCase
from pages.models import Item, Room, Character


class ItemModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Item.objects.create(name='bag')

    def test_name_label(self):
        item = Item.objects.get(id=1)
        field_label = item._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'название предмета')

    def test_name_max_length(self):
        item = Item.objects.get(id=1)
        max_length = item._meta.get_field('name').max_length
        self.assertEquals(max_length, 200)


class CharacterModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        item = Item.objects.create(name='bag')
        room = Room.objects.create(name='test_room', description='test_room for testing')
        room.items.add(item)
        character = Character.objects.create(name='bag', room=room)
        character.items.add(item)

    def test_name_label(self):
        character = Character.objects.get(id=1)
        field_label = character._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'имя')

    def test_name_max_length(self):
        character = Character.objects.get(id=1)
        max_length = character._meta.get_field('name').max_length
        self.assertEquals(max_length, 200)

    def test_room_label(self):
        character = Character.objects.get(id=1)
        field_label = character._meta.get_field('room').verbose_name
        self.assertEquals(field_label, 'комната, где находится персонаж')

    def test_items_label(self):
        character = Character.objects.get(id=1)
        field_label = character._meta.get_field('items').verbose_name
        self.assertEquals(field_label, 'предметы в инвентаре')


class RoomModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        item = Item.objects.create(name='bag')
        room = Room.objects.create(name='test_room', description='test_room for testing')
        room.items.add(item)
        character = Character.objects.create(name='bag', room=room)
        character.items.add(item)

    def test_name_label(self):
        room = Room.objects.get(id=1)
        field_label = room._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'название комнаты')

    def test_name_max_length(self):
        room = Room.objects.get(id=1)
        max_length = room._meta.get_field('name').max_length
        self.assertEquals(max_length, 200)

    def test_description_label(self):
        room = Room.objects.get(id=1)
        field_label = room._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'описание комнаты')

    def test_items_label(self):
        room = Room.objects.get(id=1)
        field_label = room._meta.get_field('items').verbose_name
        self.assertEquals(field_label, 'предметы в комнате')
