from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, UpdateAPIView
from .models import Room, Character
from .serializers import NameRoomSerializer, NameCharacterSerializer, DescriptionRoomSerializer, \
    CharsRoomSerializer, ItemsRoomSerializer, RoomCharacterSerializer, TakeItemCharacterSerializer
from rest_framework.response import Response


class NameRoomView(ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = NameRoomSerializer


class DescriptionRoomView(RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = DescriptionRoomSerializer


class CharsRoomView(RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = CharsRoomSerializer


class ItemsRoomView(RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = ItemsRoomSerializer


class NameCharacterView(ListCreateAPIView):
    queryset = Character.objects.all()
    serializer_class = NameCharacterSerializer


class RoomCharacterView(UpdateAPIView):
    queryset = Character.objects.all()
    serializer_class = RoomCharacterSerializer


class TakeItemCharacterView(UpdateAPIView):
    queryset = Character.objects.all()
    serializer_class = TakeItemCharacterSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        if Room.objects.filter(id=instance.room.id, items__in=serializer.validated_data['items']):
            items_to_remove = serializer.validated_data['items'].copy()
            character_items_id = [character_item.id for character_item in instance.items.all()]
            serializer.validated_data['items'].extend(character_items_id)
            self.perform_update(serializer)
            for item_to_remove in items_to_remove:
                instance.room.items.remove(item_to_remove)
            return Response(serializer.data)
        else:
            return Response({"error": "Нет таких предметов"})


class PutOutItemCharacterView(UpdateAPIView):
    queryset = Character.objects.all()
    serializer_class = TakeItemCharacterSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        items_to_put_out = serializer.validated_data['items'].copy()
        if Character.objects.filter(id=instance.id, items__in=items_to_put_out):
            items_in_inventory = [character_item.id for character_item in instance.items.all() if
                                  character_item not in items_to_put_out]
            serializer.validated_data['items'] = items_in_inventory
            self.perform_update(serializer)
            for item in items_to_put_out:
                instance.room.items.add(item)
            return Response(serializer.data)
        else:
            return Response({"error": "Нет таких предметов"})
