from email.policy import HTTP
from webbrowser import get
from rest_framework import status, generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView

from accounts.permissions import IsCharityOwner, IsBenefactor
from charities.models import Task
from charities.serializers import (
    TaskSerializer, CharitySerializer, BenefactorSerializer
)


class BenefactorRegistration(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = BenefactorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CharityRegistration(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CharitySerializer

    def get_serializer_context(self):
        context = super(CharityRegistration, self).get_serializer_context()
        context.update({"request": self.request})
        return context


class Tasks(generics.ListCreateAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.all_related_tasks_to_user(self.request.user)

    def post(self, request, *args, **kwargs):
        data = {
            **request.data,
            "charity_id": request.user.charity.id
        }
        serializer = self.serializer_class(data = data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data, status = status.HTTP_201_CREATED)

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            self.permission_classes = [IsAuthenticated, ]
        else:
            self.permission_classes = [IsCharityOwner, ]

        return [permission() for permission in self.permission_classes]

    def filter_queryset(self, queryset):
        filter_lookups = {}
        for name, value in Task.filtering_lookups:
            param = self.request.GET.get(value)
            if param:
                filter_lookups[name] = param
        exclude_lookups = {}
        for name, value in Task.excluding_lookups:
            param = self.request.GET.get(value)
            if param:
                exclude_lookups[name] = param

        return queryset.filter(**filter_lookups).exclude(**exclude_lookups)


class TaskRequest(APIView):
    permission_classes = [IsBenefactor]

    def get(self, request, task_id):
        
        task =  get_object_or_404(Task, id=task_id)
        if task.state != 'P':
            return Response(data={'detail': 'This task is not pending.'},status=status.HTTP_404_NOT_FOUND)
        else:
            user = request.user
            task.state = 'W'
            task.assign_to_benefactor(benefactor = user.benefactor)
            task.save()
            return Response(data={'detail': 'Request sent.'},status=status.HTTP_200_OK)


class TaskResponse(APIView):
    permission_classes = [IsCharityOwner]

    def post(self, request, task_id):

        task = get_object_or_404(Task, id = task_id)
        user_response = request.data.get("response")
        if user_response not in ["A", "R"]:
            return Response(data={'detail': 'Required field ("A" for accepted / "R" for rejected)'}, status=status.HTTP_400_BAD_REQUEST)
        elif task.state != "W":
            return Response(data={'detail': 'This task is not waiting.'}, status=status.HTTP_404_NOT_FOUND)
        elif user_response == "A":
            task._accept_benefactor()
            return Response(data={'detail': 'Response sent.'}, status=status.HTTP_200_OK)
        elif user_response == "R":
            task._reject_benefactor()
            return Response(data={'detail': 'Response sent.'}, status=status.HTTP_200_OK)



class DoneTask(APIView):
    pass