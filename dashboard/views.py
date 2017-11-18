from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Question, Story, Profile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from taggit.models import Tag
from django.db.models import Count
from django.utils import timezone
import pytz
from datetime import timedelta
from .forms import QuestionForm, AnswerForm, StoryForm,\
     CommentForm, LoginForm, SignupForm, UserEditForm, ProfileEditForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# Create your views here.
def frontboard(request, tag_slug=None):
    object_list=Question.objects.filter(created__gte=timezone.now()-timedelta(days=7))
    object_list = object_list.annotate(
        total_answers=Count('answers')).order_by('-total_answers')
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list=object_list.filter(tags__in=[tag])
    paginator=Paginator(object_list,15)
    page=request.GET.get('page')
    try:
        questions=paginator.page(page)
    except PageNotAnInteger:
        questions=paginator.page(1)
    except EmptyPage:
        questions=paginator.page(paginator.num_pages)
    return render(request,
                  'questions.html',
                  {'page':page,
                   'questions':questions,
                   'tag':tag})
    
def questions_board(request):
    object_list=Question.objects.order_by('-created')
    paginator=Paginator(object_list,15)
    page=request.GET.get('page')
    try:
        questions=paginator.page(page)
    except PageNotAnInteger:
        questions=paginator.page(1)
    except EmptyPage:
        questions=paginator.page(paginator.num_pages)
    return render(request,
                  'questions.html',
                  {'page':page,
                   'questions':questions})

def question_detail(request, year, month, day, question):
    question=get_object_or_404(Question,
                               slug=question,
                               created__year=year,
                               created__month=month,
                               created__day=day)
    answers=question.answers.filter(active=True)
    answer_form=AnswerForm()
    if request.method=='POST':  #an answer is posted
        answer_form=AnswerForm(data=request.POST or None)
        if answer_form.is_valid():
            new_answer=answer_form.save(commit=False)
            new_answer.question=question
            u=request.user
            new_answer.name= u
            new_answer.save()
            
        else:
            answer_form=AnswerForm()
            new_answer=False
    else:
        answer_form=AnswerForm()
        new_answer=False
        
    return render(request,
                  'question_detail.html',
                  {'question':question,
                   'answers':answers,
                   'answer_form':answer_form,
                   'new_answer':new_answer})
    
def stories_board(request, tag_slug=None):
    object_list=Story.objects.order_by('-created')
    tag=None
    if tag_slug:
        tag=get_object_or_404(Tag, slug=tag_slug)
        object_list.filter(tags__in=[tag])
    paginator=Paginator(object_list,15)
    page=request.GET.get('page')
    try:
        stories=paginator.page(page)
    except PageNotAnInteger:
        stories=paginator.page(1)
    except EmptyPage:
        stories=paginator.page(paginator.num_pages)
    return render(request,
                  'stories.html',
                  {'page':page,
                   'stories':stories,
                   'tag':tag})
def story_detail(request, year, month, day, story):
    story=get_object_or_404(Story,
                            slug=story,
                            created__year=year,
                            created__month=month,
                            created__day=day)
    comments=story.comments.filter(active=True)
    comment_form=CommentForm()
    if request.method=='POST': #a comment is posted
        comment_form=CommentForm(data=request.POST or None)
        if comment_form.is_valid():
            new_comment=comment_form.save(commit=False)
            new_comment.story=story
            u=request.user
            new_comment.name=u
            new_comment.save()
        else:
            comment_form=CommentForm()
            new_comment=False
    else:
        comment_form=CommentForm()
        new_comment=False
    return render(request,
                  'story_detail.html',
                  {'story':story,
                   'comments':comments,
                   'comment_form':comment_form,
                   'new_comment':new_comment})
@login_required
def users_board(request):
    users_list=User.objects.all()
    paginator=Paginator(users_list,100)
    page=request.GET.get('page')
    try:
        users=paginator.page(page)
    except PageNotAnInteger:
        users=paginator.page(1)
    except EmptyPage:
        users=paginator.page(paginator.num_pages)
        
    return render(request,
                  'users.html',
                  {'users':users,
                   'page':page})
@login_required    
def new_question(request):
    question_form=QuestionForm()
    if request.method=='POST':
        question_form=QuestionForm(data=request.POST or None)
        if question_form.is_valid():
            new_question=question_form.save(commit=False)
            usr=request.user
            new_question.author=usr
            new_question.save()
            question_form.save_m2m()
            return redirect('/questions/')
        else:
            messages.error(request,'Error Posting Question.')
            question_form=QuestionForm()
    else:
        question_form=QuestionForm()
    return render(request,
                  'new_question.html',
                  {'question_form':question_form})
@login_required
def new_story(request):
    story_form=StoryForm()
    if request.method=='POST':
        story_form=StoryForm(data=request.POST or None)
        if story_form.is_valid():
            new_story=story_form.save(commit=False)
            usr=request.user
            new_story.author=usr
            new_story.save()
            story_form.save_m2m()
            return redirect('/stories/')
        else:
            messages.error(request,'Error Posting Story.')
            story_form=StoryForm()
    else:
        story_form=StoryForm()
    return render(request,
                  'new_story.html',
                  {'story_form':story_form})
def user_login(request):
    form=LoginForm(request.POST)
    if request.method== 'POST':
        form = LoginForm(data=request.POST or None)
        if form.is_valid():
            cd=form.cleaned_data
            user=authenticate(username=cd['username'],
                              password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/')
                else:
                    return HttpResponse('bhag bhosdike')
            else:
                return HttpResponse('bhag bhosdike.')
        else:
            return HttpResponse('bhag bhosdike.')
    else:
        form=LoginForm()
    return render(request,
                  'registration/login.html',
                  {'form': form})
    
def user_logout(request):
    logout(request)
    return redirect('/')
def register(request):
    user_form=SignupForm(request.POST)
    if request.method=='POST':
        user_form=SignupForm(data=request.POST or None)
        if user_form.is_valid():
            new_user=user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            profile=Profile.objects.create(user=new_user)
            shaka=authenticate(username=user_form.cleaned_data['username'],
                               password=user_form.cleaned_data['password'],
                               )
            login(request, shaka)
            return redirect('/')
        else:
            user_form=SignupForm()
    else:
        user_form=SignupForm()
    return render(request,
                  'registration/register.html',
                  {'user_form': user_form})

@login_required
def profile_edit(request):
    if request.method=='POST':
        user_form=UserEditForm(instance=request.user,
                               data=request.POST)
        profile_form=ProfileEditForm(instance=request.user.profile,
                                     data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
        else:
            messages.error(request, 'An error occured while updating profile.')
            user_form=UserEditForm(instance=request.user)
            profile_form=ProfileEditForm(instance=request.user.profile)
    else:
        user_form=UserEditForm(instance=request.user)
        profile_form=ProfileEditForm(instance=request.user.profile)
    return render(request,
                  'profile_edit.html',
                  {'user_form':user_form,
                   'profile_form':profile_form})

@login_required
def profile(request):
    usr=request.user
    profile_usr=request.user.profile
    return render(request,
                  'profile.html',
                  {'usr':usr,
                   'profile_usr':profile_usr})
@login_required
def user_profile(request, username):
    usr=get_object_or_404(User,
                          username=username)
    profile_usr=usr.profile
    return render(request,
                  'profile.html',
                  {'usr':usr,
                   'profile_usr':profile_usr})

