from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response

from .models import Notification
from .openai_integration import get_parsed_user_message
from .serializers import NotificationCreateViewSerializer, NotificationRetrieveViewSerializer


class NotificationCreateView(CreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationCreateViewSerializer

    def create(self, request, *args, **kwargs):
        parsed_user_message = get_parsed_user_message(self.request.data['text'])

        chat_id = request.data['chat_id']
        notification_text = parsed_user_message['text']
        notification_time = parsed_user_message['time']
        notification_time_seconds = parsed_user_message['time_seconds']

        serializer = self.get_serializer(data={
            'chat_id': chat_id,
            'text': notification_text,
            'time': notification_time,
            'time_seconds': notification_time_seconds
        })

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class NotificationRetrieveView(RetrieveAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationRetrieveViewSerializer
