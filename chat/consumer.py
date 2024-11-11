import json
import base64
import uuid
from django.core.files.base import ContentFile

from channels.db import database_sync_to_async
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework import mixins
from djangochannelsrestframework.observer.generics import (ObserverModelInstanceMixin, action)
from djangochannelsrestframework.observer import model_observer
from rest_framework.exceptions import ValidationError

from .models import Room, Message
from django.contrib.auth.models import User
from .serializers import MessageSerializer, RoomSerializer, UserSerializer


class RoomConsumer(ObserverModelInstanceMixin, GenericAsyncAPIConsumer):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    lookup_field = "pk"

    async def disconnect(self, code):
        if hasattr(self, "room_subscribe"):
            await self.remove_user_from_room(self.room_subscribe)
            await self.notify_users()
        await super().disconnect(code)

    @action()
    async def join_room(self, pk, **kwargs):
        self.room_subscribe = pk
        try:
            await self.add_user_to_room(pk)
        except Exception as e:
            return ValidationError({"message": "In this room not found"})
        await self.notify_users()

    @action()
    async def leave_room(self, pk, **kwargs):
        await self.remove_user_from_room(pk)

    @action()
    async def create_message(self, message, image=None, file=None, **kwargs):
        room: Room = await self.get_room(pk=self.room_subscribe)

        with open(image, "rb") as image_file:  # sending images with base54 format
            base64_encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
        mime_type = image.split('.')[-1]
        base64_image_str = f"data:image/{mime_type};base64,{base64_encoded_image}"
        if file != None:
            with open(file, "rb") as file_path:  # sending files with base64 format
                base64_encoded_file = base64.b64encode(file_path.read()).decode("utf-8")
            mime_type = file.split('.')[-1]
            base64_file_str = f"data:application/{mime_type};base64,{base64_encoded_file}"
        else:
            base64_file_str = None

        await database_sync_to_async(Message.objects.create)(
            room=room,
            user=self.scope["user"],
            text=message,
            image=base64_image_str,
            file=base64_file_str
        )

    @action()
    async def subscribe_to_messages_in_room(self, pk, **kwargs):
        await self.message_activity.subscribe(room=pk)

    @action()
    async def update_message(self, message_id, new_message, pk, **kwargs):
        message: Message = await self.get_message(message_id=message_id)
        user = self.scope['user']
        if message and message.user.id == user.id:
            message.text = new_message
            await self.save_message(message)
        else:
            await self.send_json({"message": "Sorry you can not update message"})

    @action()
    async def delete_message(self, message_id, **kwargs):
        message: Message = await self.get_message(message_id=message_id)
        user = self.scope['user']
        if message and message.user.id == user.id:
            await self.delete_message_from_db(message)
        else:
            await self.send_json({"message": "Sorry, you cannot delete this message"})

    @model_observer(Message)
    async def message_activity(self, message, observer=None, **kwargs):
        await self.send_json(message)

    @message_activity.groups_for_signal
    def message_activity(self, instance: Message, **kwargs):
        yield f'room__{instance.room_id}'
        yield f'pk__{instance.pk}'

    @message_activity.groups_for_consumer
    def message_activity(self, room=None, **kwargs):
        if room is not None:
            yield f'room__{room}'

    @message_activity.serializer
    def message_activity(self, instance: Message, action, **kwargs):
        return dict(data=MessageSerializer(instance).data, action=action.value, pk=instance.pk)

    async def notify_users(self):
        room: Room = await self.get_room(self.room_subscribe)
        for group in self.groups:
            await self.channel_layer.group_send(
                group,
                {
                    'type': 'update_users',
                    'usuarios': await self.current_users(room)
                }
            )

    async def update_users(self, event: dict):
        await self.send(text_data=json.dumps({'usuarios': event["usuarios"]}))

    @database_sync_to_async
    def get_room(self, pk: int) -> Room:
        return Room.objects.get(pk=pk)

    @database_sync_to_async
    def save_message(self, message: Message):
        message.save()

    @database_sync_to_async
    def delete_message_from_db(self, message: Message):
        message.delete()

    @database_sync_to_async
    def get_message(self, message_id: int) -> Message:
        return Message.objects.get(pk=message_id)

    @database_sync_to_async
    def get_message(self, message_id: int) -> Message:
        return Message.objects.filter(id=message_id).select_related('user').first()

    def decode_base64_file(self, data):
        """
        Decode a base64 encoded file and return a ContentFile instance.
        Expects data as "data:<mime>;base64,<encoded_content>"
        """
        if not data:
            return None

        format, file_str = data.split(';base64,')
        ext = format.split('/')[-1]  # Extract file extension
        file_content = base64.b64decode(file_str)
        return ContentFile(file_content, name=f"{uuid.uuid4()}.{ext}")

    @database_sync_to_async
    def current_users(self, room: Room):
        return [UserSerializer(user).data for user in room.current_users.all()]

    @database_sync_to_async
    def remove_user_from_room(self, room):
        user: User = self.scope["user"]
        user.current_rooms.remove(room)

    @database_sync_to_async
    def add_user_to_room(self, pk):
        user: User = self.scope["user"]
        if not user.current_rooms.filter(pk=self.room_subscribe).exists():
            user.current_rooms.add(Room.objects.get(pk=pk))









