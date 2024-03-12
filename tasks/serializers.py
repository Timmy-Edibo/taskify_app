# payments/serializers.py
from rest_framework import serializers
from .models import Project, Task, TaskMembers
from accounts.serializers import UserSerializer


class ProjectSerializer(serializers.ModelSerializer):
    # passenger_name = serializers.CharField(source="passenger.username", read_only=True)
    class Meta:
        model = Project
        fields = "__all__"


class TaskSerializer(serializers.ModelSerializer):
    # passenger_name = serializers.CharField(source="passenger.username", read_only=True)
    image = serializers.ImageField(allow_null=True, required=False)

    class Meta:
        model = Task
        fields = "__all__"


class TaskMemberSerializer(serializers.ModelSerializer):
    member_info = UserSerializer(read_only=True)

    class Meta:
        model = TaskMembers
        fields = "__all__"

    def get_member_info(self, instance):
        return UserSerializer(instance.member).data


class TaskMemberResponseSerializer(serializers.ModelSerializer):
    member = UserSerializer()

    class Meta:
        model = TaskMembers
        fields = "__all__"
        # depth=1

    # def get_member_info(self, instance):
    #     return UserSerializer(instance.member).data
