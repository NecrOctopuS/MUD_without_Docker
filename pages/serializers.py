from rest_framework import serializers
from .models import Room, Item, Character


class NameRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('name',)


class DescriptionRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('description',)


class CharsRoomSerializer(serializers.ModelSerializer):
    chars = serializers.StringRelatedField(many=True)

    class Meta:
        model = Room
        fields = ('chars',)


class ItemsRoomSerializer(serializers.ModelSerializer):
    items = serializers.StringRelatedField(many=True)

    class Meta:
        model = Room
        fields = ('items',)


class NameCharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ('name',)


class RoomCharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ('room',)


class TakeItemCharacterSerializer(serializers.ModelSerializer):
    items = serializers.PrimaryKeyRelatedField(many=True, read_only=False, queryset=Item.objects.all())

    class Meta:
        model = Character
        fields = ('items',)
