from dataclasses import fields
from pyexpat import model
from rest_framework import serializers

from .models import Benefactor
from .models import Charity, Task


class BenefactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Benefactor
        fields = ["experience","free_time_per_week",]

    def create(self, validated_data):
            benefactor = Benefactor(
                experience=validated_data["experience"],
                free_time_per_week=validated_data["free_time_per_week"],
        
            )
            user = self.context['request'].user
            benefactor.user = user
            benefactor.save()
            return benefactor
        


class CharitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Charity
        fields = ['name', 'reg_number',]

    def create(self, validated_data):
            charity = Charity(
                name=validated_data["name"],
                reg_number=validated_data["reg_number"],
        
            )
            user =  self.context['request'].user
            charity.user = user
            charity.save()
            return charity



class TaskSerializer(serializers.ModelSerializer):
    state = serializers.ChoiceField(read_only=True, choices=Task.TaskStatus.choices)
    assigned_benefactor = BenefactorSerializer(required=False)
    charity = CharitySerializer(read_only=True)
    charity_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Charity.objects.all(), source='charity')

    class Meta:
        model = Task
        fields = (
            'id',
            'title',
            'state',
            'charity',
            'charity_id',
            'description',
            'assigned_benefactor',
            'date',
            'age_limit_from',
            'age_limit_to',
            'gender_limit',
        )
