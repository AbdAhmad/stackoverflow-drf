from rest_framework import generics, permissions, status

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import User

from .models import Question, Answer, Questionvote, Answervote, Profile

from stack_app.permissions import IsOwnerOrReadOnly
from stack_app.serializers import QuestionSerializer, AnswerSerializer, QuestionvoteSerializer, ProfileSerializer, AnswervoteSerializer


################################################################################################################
########################################## Question Views ######################################################
################################################################################################################


class QuestionList(generics.ListCreateAPIView):

    questions = Question.objects.all()
    serializer_class = QuestionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):

        data = request.data
        serializer = QuestionSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"data": serializer.data, "status": status.HTTP_201_CREATED})
        return Response({"status": status.HTTP_400_BAD_REQUEST})


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

        try:
            question = Question.objects.get(slug=kwargs['slug'])
        except Question.DoesNotExist:
            return Response({'status': status.HTTP_404_NOT_FOUND})

        all_ques_vote = Questionvote.objects.filter(question=question)
        ques_upvotes = all_ques_vote.filter(upvote=True).count()
        ques_downvotes = all_ques_vote.filter(downvote=True).count()
        ques_votes_count = ques_upvotes - ques_downvotes
        question.votes = ques_votes_count
        question.views = question.views + 1 
        question.save()

        ques_serializer = QuestionSerializer(question, many=False)

        answers = Answer.objects.filter(question_to_ans=question)

        for answer in answers:
            all_ans_votes = Answervote.objects.filter(answer=answer)
            ans_upvotes = all_ans_votes.filter(upvote=True).count()
            ans_downvotes = all_ans_votes.filter(downvote=True).count()
            ans_votes_count = ans_upvotes - ans_downvotes
            answer.votes = ans_votes_count
            answer.save()

        ans_serializer = AnswerSerializer(answers, many=True)
 
        return Response({'question': ques_serializer.data, 'answers': ans_serializer.data})


    def update(self, request, *args, **kwargs):

        try:
            question = Question.objects.get(slug=kwargs['slug'])
        except Question.DoesNotExist:
            return Response({'status': status.HTTP_404_NOT_FOUND})
        data = request.data

        serializer = QuestionSerializer(instance=question, data=data)

        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data)


class UpvoteQues(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        question = Question.objects.get(id=kwargs['pk'])
        user = request.user
        
        try:
            ques_vote_by_user = Questionvote.objects.filter(user=user)
            print(ques_vote_by_user)
            ques_vote = ques_vote_by_user.get(question=question)
        except Questionvote.DoesNotExist:
            ques_vote = None

        if ques_vote is not None:
            if ques_vote.upvote != True:
                ques_vote.upvote = True
                ques_vote.downvote = False
                ques_vote.save()
                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_208_ALREADY_REPORTED)

        serializer = QuestionvoteSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=user, upvote=True, question=question)
            return Response(status=status.HTTP_201_CREATED)


class DownvoteQues(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        question = Question.objects.get(id=kwargs['pk'])
        user = request.user
        
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
                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_208_ALREADY_REPORTED)
            
        serializer = QuestionvoteSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=user, downvote=True, question=question)
            return Response(status=status.HTTP_201_CREATED)


class SearchedQues(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):

        try:
            questions = Question.objects.filter(title__icontains=kwargs['searched_ques']).order_by('-views')
        except Question.DoesNotExist:
            questions = None

        if questions:
            serializer = QuestionSerializer(questions, many=True)
            return Response(serializer.data)
        else:
            return Response({"status": status.HTTP_404_NOT_FOUND})


######################################################################################################################
############################################# Answer Views ###########################################################
######################################################################################################################


class AnswerCreate(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        user = request.user
        data = request.data
        question = Question.objects.get(id=kwargs['pk'])
        slug = question.slug

        serializer = AnswerSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save(question_to_ans=question, question_slug=slug, user=user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AnswerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsOwnerOrReadOnly]

    def retrieve(self, request, *args, **kwargs):

        answer = Answer.objects.get(pk=kwargs['pk'])
        question = answer.question_to_ans

        ans__serializer = AnswerSerializer(answer, many=False)
        ques_serializer = QuestionSerializer(question, many=False)
 
        return Response({'answer': ans__serializer.data, 'question': ques_serializer.data})


class UpvoteAns(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        answer = Answer.objects.get(id=kwargs['pk'])
        user = request.user

        try:
            ans_vote_by_user = Answervote.objects.filter(user=user)
            ans_vote = ans_vote_by_user.get(answer=answer)
        except Answervote.DoesNotExist:
            ans_vote = None

        if ans_vote is not None:
            if ans_vote.upvote != True: 
                ans_vote.upvote = True
                ans_vote.downvote = False
                ans_vote.save()
                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_208_ALREADY_REPORTED)
            
        serializer = AnswervoteSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=user, upvote=True, answer=answer)
            return Response(status=status.HTTP_201_CREATED)


class DownvoteAns(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        answer = Answer.objects.get(id=kwargs['pk'])
        user = request.user
    
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
                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_208_ALREADY_REPORTED)
            
        serializer = AnswervoteSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=user, downvote=True, answer=answer)
            return Response(status=status.HTTP_201_CREATED)


################################################################################################################
########################################### Profile Views ######################################################
################################################################################################################


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

        try:
            user = User.objects.get(username=kwargs['username'])
        except User.DoesNotExist:
            return Response({'status': status.HTTP_404_NOT_FOUND})           

        else:
            profile = Profile.objects.get(user=user)
            
            questions = Question.objects.filter(user=user)
            answers = Answer.objects.filter(user=user)
        
            profile_serializer = ProfileSerializer(profile)
            questions_serializer = QuestionSerializer(questions, many=True)
            answers_serializer = AnswerSerializer(answers, many=True)

            return Response({
                'profile': profile_serializer.data,
                'questions': questions_serializer.data,
                'answers': answers_serializer.data
                })


    def update(self, request, *args, **kwargs):
        
        data = request.data
        user = User.objects.get(username=kwargs['username'])
        profile = Profile.objects.get(user=user)

        serializer = ProfileSerializer(instance=profile, data=data)

        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data)
