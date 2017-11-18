from django import forms
from .models import Question, Answer, Story, Comment, Profile
from django.contrib.auth.models import User

#question forms
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('title','body','tags')


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer 
        fields = {'body'}


#news forms

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ('title','source')

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields={'body'}

#login form

class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)
    
class SignupForm(forms.ModelForm):
    password=forms.CharField(label='Password',
                             widget=forms.PasswordInput)
    class Meta:
        model=User
        fields = ('username','email')
        
class UserEditForm(forms.ModelForm):
    class Meta:
        model=User
        fields= ('first_name','last_name','email')
class ProfileEditForm(forms.ModelForm):
    date_of_birth=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'y-m-d'}))
    class Meta:
        model= Profile
        fields = ('date_of_birth','work_or_study')
        

#search form
class SearchForm(forms.Form):
    search_query=forms.CharField(max_length=50)
    
