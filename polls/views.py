from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .models import *
import random
from django.contrib.auth.models import User
from django.db.models import Max, Min, Avg
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import messages

# Create your views here.
def index(request):
    return HttpResponse("Hello")


def get_marks(request):
    if request.user.is_authenticated:
        if(request.GET):
            username = request.user.username
            score = int(request.GET.get('score'))
            if 0 <= score <= 5:
                Marks.objects.create(user=username, score=score)
            else:
                msg = "There is some error in marks .So Try again"
                return render(request, 'error.html', {'msg': msg})

        marks = Marks.objects.all()
        data= []
        for mark in marks:
            if request.user.username==mark.user:
                data.append({
                    "username":request.user.username,
                    "mark": mark.score
                })
        if not data:
           return render(request,'score.html')
        marks1 = Marks.objects.filter(user=request.user.username)
        avg = marks1.aggregate(Avg('score'))['score__avg']
        min_score = marks1.aggregate(Min('score'))['score__min']
        max_score = marks1.aggregate(Max('score'))['score__max']
        context = {
            "data": data,
            "avg": avg,
            "min_score": min_score,
            "max_score": max_score,
        }
        return render(request, 'score.html', context)
    else:
        msg = "You must be logged in to view this page."
        return render(request, 'error.html', {'msg': msg})


@login_required
def get_quiz(request):
    try:
        question_objects=list(Question.objects.all())
        data=[]
        random.shuffle(question_objects)
        for question in question_objects:
            data.append(
                {
                    "uid":question.id,
                    "question":question.question_text,
                    "marks":question.marks,
                    "Answer":question.get_answers()
                })
        payload={'status':True,'data':data}
        return JsonResponse(payload)
    except Exception as e:
        print(e)
    return HttpResponse("Something went wrong.")


def quiz(request):
    if request.user.is_authenticated:
        username = request.user.username
        return render(request, 'quiz.html', {'username':username})
    else:
        msg="You must be logged in to view this page."
        return render(request,'error.html',{'msg':msg})

@login_required
def log_out(request):
    logout(request)
    return redirect('/')


def login_user(request):
    if request.user.is_authenticated:
        return redirect('quiz')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request, user)
            messages.success(request,"logged in successfully")
            return redirect('quiz')
        else:
            messages.error(request,"Invalid password or username")
    return render(request, 'login.html')


def signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        lname = request.POST.get('lname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if name=="" or username=="":
            messages.error(request, "You can not leave any field empty")
            return redirect('signup')
        if email=="" or password1=="":
            messages.error(request, "You can not leave any field empty")
            return redirect('signup')
        if password2!=password1:
            messages.error(request,"Password does not match with each other")
            return redirect('signup')
        if User.objects.filter(username=username).exists():
            messages.error(request,"Username is already taken. choose another username")
            return redirect('signup')

        user=User.objects.create_user(username=username, email=email, password=password1, first_name=name,last_name=lname)
        user.save()
        messages.success(request,"Account created successfully.")
        return redirect('login')
    return render(request,'signup.html')
