from django.contrib.auth import models
from rest_framework import serializers
from .models import Question, Answer, Questionvote, Answervote, Profile


class QuestionSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')    

    class Meta:
        model = Question
        fields = ['id', 'title', 'body', 'tags', 'user']



class AnswerSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')    

    class Meta:
        model = Answer
        fields = ['id', 'answer', 'user', 'question_to_ans']


class QuestionvoteSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')    

    class Meta:
        model = Questionvote
        fields = ['id', 'user']


class AnswervoteSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')    

    class Meta:
        model = Answervote
        fields = ['id', 'user']


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['id', 'name', 'email', 'location', 'about_me']



# class TagSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Tag
#         fields = '__all__'
