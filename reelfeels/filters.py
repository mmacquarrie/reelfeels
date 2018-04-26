from django import template

register = template.Library()
@register.filter
def youtube_thumbnail(obj):
    return obj.get_youtube_thumbnail()

@register.filter
def top_emotion(obj):
    return obj.get_top_emotion()
