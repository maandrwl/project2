from rest_framework import serializers
from .models import Subject, Assignment, Account, Score


class scoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = (
            'id',
            'idSubject',
            'assignment',
            'score',
            'check',
        )

class accountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            'idSubject',
        )

class assignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = (
            'idSubject',
            'assignment',
            'score',
            'format',
        )