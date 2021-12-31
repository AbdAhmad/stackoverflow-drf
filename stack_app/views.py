from django.views.generic.base import View
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from stack_app.serializers import QuestionSerializer, AnswerSerializer, QuestionvoteSerializer, ProfileSerializer, AnswervoteSerializer
from .models import Question, Answer, Questionvote, Answervote, Profile
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics, serializers
from rest_framework import permissions
from stack_app.permissions import IsOwnerOrReadOnly
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import User
from rest_framework import status


class QuestionList(generics.ListCreateAPIView):
    questions = Question.objects.all()
    serializer_class = QuestionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request):

        if 'q' in request.GET and request.GET['q'] == 'latest':
            questions = Question.objects.all().order_by('-created_at')
            question_order = 'latest'

        else:
            questions = Question.objects.all().order_by('-views')
            question_order = 'mostviewed'

        for question in questions:

            ans_count = Answer.objects.filter(question_to_ans=question).count()

            all_votes = Questionvote.objects.filter(question=question)
            upvotes = all_votes.filter(upvote=True).count()
            downvotes = all_votes.filter(downvote=True).count()
            votes_count = upvotes - downvotes

            question.ans_count = ans_count

            question.votes = votes_count

            question.save()

        questions_serializer = QuestionSerializer(questions, many=True)

        return Response({'questions': questions_serializer.data, 'question_order': question_order})



class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsOwnerOrReadOnly]

    lookup_field = "slug"

    def retrieve(self, request, *args, **kwargs):
        question = Question.objects.get(slug=kwargs['slug'])

        ques_serializer = QuestionSerializer(question, many=False)

        answers = Answer.objects.filter(question_to_ans=question)

        for answer in answers:

            all_votes = Answervote.objects.filter(answer=answer)
            upvotes = all_votes.filter(upvote=True).count()
            downvotes = all_votes.filter(downvote=True).count()
            votes_count = upvotes - downvotes

            answer.votes = votes_count
            answer.save()

        ans_serializer = AnswerSerializer(answers, many=True)

        question.views = question.views + 1 
        question.save()
 
        return Response({'question': ques_serializer.data, 'answers': ans_serializer.data})


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def searched_ques(request, searched_ques):
    
    questions = Question.objects.filter(title__icontains=searched_ques).order_by('-views')
   
    if(len(questions) > 0):
        print('inside if')
        serializer = QuestionSerializer(questions, many=True)
        question_order = 'mostviewed'
        return Response({'questions': serializer.data, 'question_order': question_order})
    else:
        print('inside else')
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def answer_create(request, pk):
        data = request.data

        question = Question.objects.get(id=pk)

        serializer = AnswerSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save(question_to_ans=question, user=request.user)

        return Response(serializer.data)


class AnswerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsOwnerOrReadOnly]

    def retrieve(self, request, *args, **kwargs):

        question = Question.objects.get(pk=kwargs['pk'])

        answers = Answer.objects.filter(question_to_ans=question)

        serializer = AnswerSerializer(answers, many=True)
 
        return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def upvote_ques(request, pk):
    
    question = Question.objects.get(id=pk)
    user = request.user
    # slug = question.slug
    try:
        ques_vote_by_user = Questionvote.objects.filter(user=user)
        ques_vote = ques_vote_by_user.get(question=question)
    except Questionvote.DoesNotExist:
        ques_vote = None

    if ques_vote is not None:
        if ques_vote.upvote != True:
            ques_vote.upvote = True
            ques_vote.downvote = False
            ques_vote.save()
            return Response({'status': 200, 'message': 'You have upvoted this question'})
        else:
          return Response({'status': 403, 'message': 'You have already upvoted this question'})

    serializer = QuestionvoteSerializer(data=request.data)

    if not serializer.is_valid():
        return Response({'status': 403, 'errors': serializer.errors, 'message': 'Something went wrong'})

    serializer.save(user=user, upvote=True, question=question)

    return Response({'status': 200, 'message': 'Success'})


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def downvote_ques(request, pk):
    
    question = Question.objects.get(id=pk)
    user = request.user
    # slug = question.slug
    try:
        ques_vote_by_user = Questionvote.objects.filter(user=user)
        ques_vote = ques_vote_by_user.get(question=question)
    except Questionvote.DoesNotExist:
        ques_vote = None

    if ques_vote is not None:
        if ques_vote.downvote != True:
            ques_vote.downvote = True
            ques_vote.upvote = False
            ques_vote.save()
            return Response({'status': 200, 'message': 'You have downvoted this question'})
        else:
          return Response({'status': 403, 'message': 'You have already downvoted this question'})
        
    serializer = QuestionvoteSerializer(data=request.data)

    if not serializer.is_valid():
        return Response({'status': 403, 'errors': serializer.errors, 'message': 'Something went wrong'})

    serializer.save(user=user, downvote=True, question=question)

    return Response({'status': 200, 'message': 'Success'})

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def upvote_ans(request, pk):
    
    answer = Answer.objects.get(id=pk)
    user = request.user
    # slug = question.slug
    try:
        ans_vote_by_user = Answervote.objects.filter(user=user)
        ans_vote = ans_vote_by_user.get(answer=answer)
    except Answervote.DoesNotExist:
        ans_vote = None

    if ans_vote is not None:
        if ans_vote.user == user:
            if ans_vote.upvote != True: 
                ans_vote.upvote = True
                ans_vote.downvote = False
                ans_vote.save()
            return Response({'status': 200, 'message': 'You have downvoted this answer'})
        else:
          return Response({'status': 403, 'message': 'You have already downvoted this answer'})
        
    serializer = AnswervoteSerializer(data=request.data)

    if not serializer.is_valid():
        return Response({'status': 403, 'errors': serializer.errors, 'message': 'Something went wrong'})

    serializer.save(user=user, upvote=True, answer=answer)

    return Response({'status': 200, 'message': 'Success'})


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def downvote_ans(request, pk):
    
    answer = Answer.objects.get(id=pk)
    user = request.user
    # slug = question.slug
    try:
        ans_vote_by_user = Answervote.objects.filter(user=user)
        ans_vote = ans_vote_by_user.get(answer=answer)
    except Answervote.DoesNotExist:
        ans_vote = None

    if ans_vote is not None:
        if ans_vote.downvote != True:
            ans_vote.downvote = True
            ans_vote.upvote = False
            ans_vote.save()
            return Response({'status': 200, 'message': 'You have downvoted this answer'})
        else:
          return Response({'status': 403, 'message': 'You have already downvoted this answer'})
        
    serializer = AnswervoteSerializer(data=request.data)

    if not serializer.is_valid():
        return Response({'status': 403, 'errors': serializer.errors, 'message': 'Something went wrong'})

    serializer.save(user=user, downvote=True, answer=answer)

    return Response({'status': 200, 'message': 'Success'})


class ProfileList(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsOwnerOrReadOnly]


    def retrieve(self, request, *args, **kwargs):
        user = User.objects.get(username=kwargs['username'])

        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            profile = None

        questions = Question.objects.filter(user=user)
        questions_serializer = QuestionSerializer(questions, many=True)

        answers = Answer.objects.filter(user=user)
        answers_serializer = AnswerSerializer(answers, many=True)

        profile_serializer = ProfileSerializer(profile)

        return Response({
            'profile': profile_serializer.data,
            'questions': questions_serializer.data,
            'answers': answers_serializer.data
            })


    def update(self, request, *args, **kwargs):
        data = request.data
        print(data)

        user = User.objects.get(username=kwargs['username'])

        profile = Profile.objects.get(user=user)

        serializer = ProfileSerializer(instance=profile, data=data)

        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data)
