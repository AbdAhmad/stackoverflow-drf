from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from .slug import unique_slug_generator
from django.utils import timezone


# class Tag(models.Model): 
#     tag = models.CharField(max_length=50, unique=True)

#     def __str__(self):
#         return self.tag


class Question(models.Model):
    title = models.CharField(max_length=200, unique=True)
    body = models.TextField()
    user = models.ForeignKey(User, related_name='questions', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=250, null=True, blank=True)
    answers = models.ManyToManyField('stack_app.Answer', blank=True)
    # tags = models.ManyToManyField(Tag, blank=True)
    tags = models.CharField(max_length=200)
    views = models.IntegerField(default=0)
    votes = models.IntegerField(default=0)
    ans_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title[:50]

def pre_save_receiver(instance, **kwargs):
   if not instance.slug:
       instance.slug = unique_slug_generator(instance)

pre_save.connect(pre_save_receiver, sender=Question)


class Answer(models.Model):
    answer = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question_to_ans = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True)
    votes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.answer[:20]


class Questionvote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    upvote = models.BooleanField(default=False)
    downvote = models.BooleanField(default=False)

    def __str__(self):
        return str(self.question) + ' votes'


class Answervote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    upvote = models.BooleanField(default=False)
    downvote = models.BooleanField(default=False)

    def __str__(self):
        return str(self.answer) + ' votes'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    ques_asked = models.ManyToManyField('stack_app.Question', blank = True)
    ans_given = models.ManyToManyField('stack_app.Answer', blank = True)
    date_joined = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return self.user.username