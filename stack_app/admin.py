from django.contrib import admin
from .models import Question, Answer, Questionvote, Answervote, Profile

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Questionvote)
admin.site.register(Answervote)
admin.site.register(Profile)
