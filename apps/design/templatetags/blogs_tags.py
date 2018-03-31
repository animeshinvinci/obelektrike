from django import template

register = template.Library()


@register.filter
def xrange(value):
    return range(1, value + 1)


@register.filter
def post_like(obj, request):
    if obj is None:
        return True
    return not obj.has_session_key(request.session, 'post_like')


@register.filter
def comment_like(obj, request):
    if obj is None:
        return True
    return not obj.has_session_key(request.session, 'comment_like')


@register.filter
def pollitem_vote(obj, request):
    if obj is None:
        return True
    return not obj.has_session_key(request.session, 'pollitem_vote')
