from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from subscription import models as sub_models
from subscription.serializers import TopicSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from subscription import models as sub_models
from twilio.rest import Client
import wikipedia
# fill twilio acc details here
client = Client(settings.ACCOUNT_SID, settings.AUTH_ID)
twilio_no = settings.TWILIO_NO


@api_view(['GET'])
def test_view(request):
    return Response("Hosted Successfully", status=status.HTTP_200_OK)


@api_view(['POST'])
def register_student(request):
    data = {
        "type": request.data.get('type'),
        "name": request.data.get('name'),
        "phone": request.data.get('phone')
    }
    if data["type"] == "registration":
        data["class"] = request.data.get('class')
        if data["class"] is None:
            # twilio added
            message = client.messages.create(
                from_='twilio_no', body='Class not provided', to=data["phone"])
            return Response("Class not provided", status=status.HTTP_400_BAD_REQUEST)
        if data["name"] is None:
            # twilio added
            message = client.messages.create(
                from_='twilio_no', body='Name not provided', to=data["phone"])
            return Response("Name not provided", status=status.HTTP_400_BAD_REQUEST)
        if data["phone"] is None:
            # twilio added
            message = client.messages.create(
                from_='twilio_no', body='Phone not provided', to=data["phone"])
            return Response("Phone not provided", status=status.HTTP_400_BAD_REQUEST)
        student = sub_models.Student.objects.get(
            student_name__exact=data["name"],
            student_phone__exact=data["phone"],
            student_class__exact=data["class"]
        )
        if student is not None:
           # twilio added
            message = client.messages.create(
                from_='twilio_no', body='Student exist', to=data["phone"])
            return Response("student exists", status=status.HTTP_409_CONFLICT)
        student = sub_models.Student()
        student.student_class = data["class"]
        student.student_name = data["name"]
        student.student_phone = data["phone"]
        student.save()
    # TODO send sms here
        message = client.messages.create(
            from_='twilio_no', body='Registered', to=data["phone"])
    return Response("successful", status=status.HTTP_201_CREATED)


def next_topic(phone):
    students = sub_models.Student.objects.filter(student_phone__exact=phone)
    for student in students:
        progress = sub_models.Progress.objects.get(student=student)
        if len(progress) != 0:
            if progress.last_topic_index == sub_models.Topic.objects.filter(chapter=progress.last_chapter).count():
                progress.last_topic_index = 1
                progress.last_chapter_index += 1
                progress.last_chapter = sub_models.Chapter.objects.get(index=progress.last_chapter_index)
                progress.last_topic = sub_models.Topic.objects.get(chapter=progress.last_chapter,
                                                                   index=progress.last_topic_index)
                return TopicSerializer(progress.last_topic)
            else:
                progress.last_topic_index += 1
                progress.last_topic = sub_models.Topic.objects.get(chapter=progress.last_chapter,
                                                                   index=progress.last_topic_id)
                return TopicSerializer(progress.last_topic)

@api_view(['POST'])            
def search(request):
    data = {
        "term": request.data.get('term'),
        "phone": request.data.get('phone')
    }
    st = request.data.get(data['term'])
    message = client.messages.create(from_='twilio_no', body=wikipedia.summary(st, sentences=3), to=data["phone"])
    return Response("successful")
            
