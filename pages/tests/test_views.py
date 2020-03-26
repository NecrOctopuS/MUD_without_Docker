from pages.models import Item, Room, Character
from pages.serializers import NameRoomSerializer, DescriptionRoomSerializer, CharsRoomSerializer, ItemsRoomSerializer, \
    NameCharacterSerializer
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
import json

client = Client()


class NameRoomViewTest(TestCase):

    def setUp(self):
        Room.objects.create(name='hall', description='hall for testing')
        Room.objects.create(name='kitchen', description='kitchen for testing')
        Room.objects.create(name='garage', description='garage for testing')
        Room.objects.create(name='bedroom', description='bedroom for testing')

    def test_get_all_room_names(self):
        response = client.get(reverse('get_rooms_names'))
        rooms = Room.objects.all()
        serializer = NameRoomSerializer(rooms, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DescriptionRoomViewTest(TestCase):

    def setUp(self):
        self.hall = Room.objects.create(name='hall', description='hall for testing')
        self.kitchen = Room.objects.create(name='kitchen', description='kitchen for testing')
        self.garage = Room.objects.create(name='garage', description='garage for testing')
        self.bedroom = Room.objects.create(name='bedroom', description='bedroom for testing')

    def test_get_single_room_description(self):
        response = client.get(reverse('get_single_room_description', kwargs={'pk': self.garage.pk}))
        room = Room.objects.get(pk=self.garage.pk)
        serializer = DescriptionRoomSerializer(room)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_room_description(self):
        response = client.get(reverse('get_single_room_description', kwargs={'pk': 100}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CharsRoomViewTest(TestCase):

    def setUp(self):
        self.hall = Room.objects.create(name='hall', description='hall for testing')
        self.kitchen = Room.objects.create(name='kitchen', description='kitchen for testing')
        self.garage = Room.objects.create(name='garage', description='garage for testing')
        self.bedroom = Room.objects.create(name='bedroom', description='bedroom for testing')
        self.anton = Character.objects.create(name='anton', room=self.bedroom)

    def test_get_chars_in_room(self):
        response = client.get(reverse('get_chars_in_room', kwargs={'pk': self.bedroom.pk}))
        room = Room.objects.get(pk=self.bedroom.pk)
        serializer = CharsRoomSerializer(room)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_chars_in_invalid_room(self):
        response = client.get(reverse('get_chars_in_room', kwargs={'pk': 100}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ItemsRoomViewTest(TestCase):

    def setUp(self):
        self.hall = Room.objects.create(name='hall', description='hall for testing')
        self.kitchen = Room.objects.create(name='kitchen', description='kitchen for testing')
        self.garage = Room.objects.create(name='garage', description='garage for testing')
        self.bedroom = Room.objects.create(name='bedroom', description='bedroom for testing')
        self.knife = Item.objects.create(name='knife')
        self.fork = Item.objects.create(name='fork')
        self.kitchen.items.add(self.knife)
        self.kitchen.items.add(self.fork)

    def test_get_items_in_room(self):
        response = client.get(reverse('get_items_in_room', kwargs={'pk': self.kitchen.pk}))
        room = Room.objects.get(pk=self.kitchen.pk)
        serializer = ItemsRoomSerializer(room)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_items_in_invalid_room(self):
        response = client.get(reverse('get_items_in_room', kwargs={'pk': 100}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class NameCharacterViewTest(TestCase):

    def setUp(self):
        self.hall = Room.objects.create(name='hall', description='hall for testing')
        self.kitchen = Room.objects.create(name='kitchen', description='kitchen for testing')
        self.garage = Room.objects.create(name='garage', description='garage for testing')
        self.bedroom = Room.objects.create(name='bedroom', description='bedroom for testing')
        Character.objects.create(name='anton', room=self.bedroom)
        Character.objects.create(name='danton', room=self.bedroom)
        Character.objects.create(name='avanton', room=self.bedroom)
        Character.objects.create(name='ganton', room=self.bedroom)

    def test_get_all_character_names(self):
        response = client.get(reverse('get_all_character_names'))
        characters = Character.objects.all()
        serializer = NameCharacterSerializer(characters, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class RoomCharacterViewTest(TestCase):

    def setUp(self):
        self.garage = Room.objects.create(name='garage', description='garage for testing')
        self.bedroom = Room.objects.create(name='bedroom', description='bedroom for testing')
        self.anton = Character.objects.create(name='anton', room=self.bedroom)
        self.valid_payload = {
            'room': 1
        }

        self.invalid_payload = {
            'room': '2garage1111'
        }

    def test_valid_update_characters_room(self):
        response = client.put(
            reverse('update_characters_room', kwargs={'pk': self.anton.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_characters_room(self):
        response = client.put(
            reverse('update_characters_room', kwargs={'pk': self.anton.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        print(response.status_code)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TakeItemCharacterViewTest(TestCase):
    def setUp(self):
        self.bedroom = Room.objects.create(name='bedroom', description='bedroom for testing')
        self.anton = Character.objects.create(name='anton', room=self.bedroom)
        self.knife = Item.objects.create(name='knife')
        self.fork = Item.objects.create(name='fork')
        self.bedroom.items.add(self.knife)
        self.bedroom.items.add(self.fork)
        self.valid_payload = {
            'items': [1, 2]
        }

        self.invalid_payload = {
            'items': ['knife', 'forksss']
        }

    def test_valid_take_item(self):
        response = client.put(
            reverse('take_item', kwargs={'pk': self.anton.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_take_item(self):
        response = client.put(
            reverse('take_item', kwargs={'pk': self.anton.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PutOutItemCharacterViewTest(TestCase):
    def setUp(self):
        self.bedroom = Room.objects.create(name='bedroom', description='bedroom for testing')
        self.anton = Character.objects.create(name='anton', room=self.bedroom)
        self.knife = Item.objects.create(name='knife')
        self.fork = Item.objects.create(name='fork')
        self.anton.items.add(self.knife)
        self.anton.items.add(self.fork)
        self.valid_payload = {
            'items': [1, 2]
        }

        self.invalid_payload = {
            'items': ['knife', 'forksss']
        }

    def test_valid_put_out_item(self):
        response = client.put(
            reverse('put_out_item', kwargs={'pk': self.anton.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_put_out_item(self):
        response = client.put(
            reverse('put_out_item', kwargs={'pk': self.anton.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
