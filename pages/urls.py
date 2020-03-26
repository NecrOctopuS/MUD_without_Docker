from django.urls import path
from .views import NameRoomView, NameCharacterView, DescriptionRoomView, CharsRoomView, ItemsRoomView, \
    RoomCharacterView, TakeItemCharacterView, PutOutItemCharacterView

urlpatterns = [
    path('rooms/', NameRoomView.as_view(), name='get_rooms_names'),
    path('rooms/<int:pk>/description', DescriptionRoomView.as_view(), name='get_single_room_description'),
    path('rooms/<int:pk>/chars', CharsRoomView.as_view(), name='get_chars_in_room'),
    path('rooms/<int:pk>/items', ItemsRoomView.as_view(), name='get_items_in_room'),
    path('characters/', NameCharacterView.as_view(), name='get_all_character_names'),
    path('characters/<int:pk>/room', RoomCharacterView.as_view(), name='update_characters_room'),
    path('characters/<int:pk>/take_item', TakeItemCharacterView.as_view(), name='take_item'),
    path('characters/<int:pk>/put_out_item', PutOutItemCharacterView.as_view(), name='put_out_item'),
]
