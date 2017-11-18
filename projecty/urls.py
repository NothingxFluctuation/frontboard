"""projecty URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from dashboard import views
urlpatterns = [
    url(r'^$', views.frontboard, name='frontboard'),
    url(r'^tag/(?P<tag_slug>[-\w]+)/$', views.frontboard,
        name='questions_by_tag'),
    url(r'^stories/tag/(?P<tag_slug>[-\w]+)/$', views.stories_board,
        name='stories_by_tag'),
    url(r'^questions/$', views.questions_board, name='questions_board'),
    url(r'^stories/$', views.stories_board, name='stories_board'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<question>[-\w]+)/$',
        views.question_detail,
        name='question_detail'),
    url(r'^story/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<story>[-\w]+)/$',
        views.story_detail,
        name='story_detail'),
    url(r'^users/$',views.users_board,name='users_board'),
    url(r'^new_question/$',views.new_question,name='new_question'),
    url(r'^new_story/$', views.new_story,name='new_story'),
    #url(r'^login/$', views.user_login, name='login'),
    url(r'^login/$', 'django.contrib.auth.views.login',
        name='login'),
    url(r'^logout/$',
        views.user_logout,
        name='logout'),
    url(r'^logout-then-login/$',
        'django.contrib.auth.views.logout_then_login',
        name='logout_then_login'),
    #change password urls
    url(r'^password_change/$',
        'django.contrib.auth.views.password_change',
        name='password_change'),
    url(r'^password_change/done/$',
        'django.contrib.auth.views.password_change_done',
        name='password_change_done'),
    url(r'^signup/$', views.register, name='signup'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile/edit/$', views.profile_edit, name='profile_edit'),
    url(r'^profile/(?P<username>[\w.@+-]+)/$', views.user_profile, name='user_profile'),
    url(r'^admin/', include(admin.site.urls)),
]
