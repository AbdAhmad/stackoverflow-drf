from django.contrib.auth import models
from rest_framework import serializers
from .models import Question, Answer, Questionvote, Answervote, Profile


class QuestionSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')    

    class Meta:
        model = Question
        fields = ['id', 'title', 'body', 'tags', 'user', 'views', 'votes', 'ans_count', 'created_at', 'slug']



class AnswerSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')    

    class Meta:
        model = Answer
        fields = ['id', 'answer', 'user', 'question_to_ans', 'votes', 'created_at']


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
    user = serializers.ReadOnlyField(source='user.username')    

    class Meta:
        model = Profile
        fields = ['id', 'user', 'full_name', 'email', 'location', 'bio']



# class TagSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Tag
#         fields = '__all__'
