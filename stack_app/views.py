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


class QuestionList(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request):
        if request.method == 'POST':
                searched_ques = request.POST['search']
                questions = Question.objects.filter(title__icontains=searched_ques)
                marked = ''
        else:
            if request.GET and ('q' in request.GET) and request.GET['q'] == 'latest':
                questions = Question.objects.all().order_by('-created_at')
                marked = 'latest'
            else:
                questions = Question.objects.all().order_by('-views')
                marked = 'mostviewed'
        # questions_dict = {}
        # for question in questions:
        #     ans_n_votes = []
        #     ans_count = Answer.objects.filter(question_to_ans=question).count()
        #     all_votes = Questionvote.objects.filter(question=question)
        #     upvotes = all_votes.filter(upvote=True).count()
        #     downvotes = all_votes.filter(downvote=True).count()
        #     votes_count = upvotes - downvotes
        #     ans_n_votes.append(ans_count)
        #     ans_n_votes.append(votes_count)
        #     questions_dict[str(question)] = ans_n_votes

        questions_list = []
        for question in questions:
            ques_ans_votes_views_tags = []
            ques_ans_votes_views_tags.append(str(question))
            ans_count = Answer.objects.filter(question_to_ans=question).count()
            all_votes = Questionvote.objects.filter(question=question)
            upvotes = all_votes.filter(upvote=True).count()
            downvotes = all_votes.filter(downvote=True).count()
            votes_count = upvotes - downvotes
            ques_ans_votes_views_tags.append(ans_count)
            ques_ans_votes_views_tags.append(votes_count)
            ques_ans_votes_views_tags.append(question.views)
            ques_ans_votes_views_tags.append(question.tags)
            questions_list.append(ques_ans_votes_views_tags)

        context = {
            'questions_list': questions_list,
            'marked': marked
        }

        return Response(context)


class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsOwnerOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        question = Question.objects.get(slug=kwargs['slug'])
        user = request.user
        author = question.user
        authenticated = False
        if str(user) == str(author):
            authenticated = True
        all_ques_votes = Questionvote.objects.filter(question=question)
        upvotes = all_ques_votes.filter(upvote=True).count()
        downvotes = all_ques_votes.filter(downvote=True).count()
        ques_votes = upvotes - downvotes
        question.views = question.views + 1 
        question.save()
 
        context = {
            'question': str(question),
            'ques_votes': ques_votes,
            'authenticated': authenticated 
            }
        return Response(context)


class AnswerList(generics.ListCreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AnswerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsOwnerOrReadOnly]


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


class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsOwnerOrReadOnly]
