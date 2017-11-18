from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown
from ..models import Question, Story

register = template.Library()

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))

@register.simple_tag
def total_questions():
    return Question.objects.count()

@register.inclusion_tag('question_tags.html')
def top_question_tags():
    top_q_tags=Question.tags.most_common()[:10]
    return {'top_q_tags':top_q_tags}

@register.inclusion_tag('story_tags.html')
def top_story_tags():
    top_s_tags=Story.tags.most_common()[:10]
    return {'top_s_tags':top_s_tags}
