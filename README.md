# StackOverflow Clone API

The aim of this project was to create an API which has all the core functionalities of [Stackoverflow](https://stackoverflow.com/). This
API is consumed by a frontend which was created using ReactJs. Checkout its repository [here](https://github.com/AbdAhmad/stackoverflow-react). See live project [here](https://stack-over-flow.netlify.app/)

### About Stackoverflow
Stackoverflow is an open community for anyone who codes. You can ask questions related to programming and even help others by answering their questions. Stackoverflow is used worldwide by millions of developers.

## Endpoints

#### Endpoints for User registration and JWT Authentication 

* api/token/ - POST - Endpoint to get access and refresh tokens.
* api/token/refresh/ - POST - Endpoint to get new tokens.
* register/ - POST - Endpoint to register a user.
* check_credentials/ - POST - Endpoint to check validity of users credentials while login.

#### Endpoints for Questions

* question/ - GET, POST - Endpoint to create or retrieve a list of all questions.
* question/<str:slug>/ - GET, PUT and DELETE - Endpoint to read, update or delete a particular question with different HTTP methods.
* upvote_ques/<int:pk>/ - POST - Endpoint to upvote a question.
* downvote_ques/<int:pk>/ - POST - Endpoint to downvote a question.
* searched_ques/<str:searched_ques> - POST - Endpoint to get a search question.

#### Endpoints for Answers

* answer_create/<int:pk>/ - POST - Endpoint to add an answer for a question.
* answer/<int:pk>/ - GET, PUT and DELETE - Endpoint to read, update or delete a particular answer.
* upvote_ans/<int:pk>/ - POST - Endpoint to upvote an answer.
* downvote_ans/<int:pk>/ - POST - Endpoint to downvote an answer.

#### Endpoints for User Profile

* profile/ - POST - Endpoint to create users profile.
* profile/<str:username>/ - GET, PUT - Endpoint to retrieve or update profile.



## Installation Guide
A step by step series of examples that tell you how to get a development env running

In your cmd or terminal:

```bash
git clone https://github.com/AbdAhmad/stackoverflow-drf.git
```

Then,
* cd stackoverflow-drf
* pip install -r requirements.txt
* python manage.py makemigrations
* python manage.py migrate
* python manage.py runserver

You are done with the setup now!

## Acknowledgements & References
* [Python](https://docs.python.org/3/)
* [Django](https://docs.djangoproject.com/en/3.2/)
* [Django Rest Framework](https://www.django-rest-framework.org/)
* [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)
* [AutoSlug](https://pypi.org/project/django-autoslug/)
* [Stackoverflow](https://stackoverflow.com/)
* [PythonAnywhere](https://www.pythonanywhere.com/)

## Developed by [Abdulla Ahmad](https://github.com/AbdAhmad)
