from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from subscription import models as sub_models
from twilio.rest import Client
# fill twilio acc details here
client = Client(ACCOUNT_SID, AITH_ID)
twilio_no = 'twilio_number'


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
