from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.http import Http404, JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView, TemplateView

from apps.blogs.forms import CommentForm
from apps.blogs.models import Category, Comment, Post


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        post_qs = Post.objects.filter(
            is_published=True
        )
        kwargs['new_posts'] = post_qs.exclude(
            category__categorytype=Category.CATEGORY_QUESTIONS
        )[:5]
        kwargs['practic_posts'] = post_qs.filter(
            category__categorytype=Category.CATEGORY_PRACTICS
        )[:5]
        return kwargs


class PostSearchListView(TemplateView):
    template_name = 'post-search.html'

    def get_context_data(self, **kwargs):
        kwargs = super(PostSearchListView, self).get_context_data(**kwargs)
        kwargs['search'] = self.request.GET.get('text', '')
        return kwargs


class PostListView(ListView):
    model = Post
    paginate_by = 10
    template_name = 'post-list.html'

    def get_queryset(self):
        qs = super(PostListView, self).get_queryset()
        return qs.filter(is_published=True).exclude(category__categorytype=Category.CATEGORY_QUESTIONS)


class PostChoicesListView(PostListView):
    template_name = 'post-choices-list.html'
    is_last = False
    is_populate = False
    is_commented = False
    is_viewed = False

    def get_queryset(self):
        qs = super(PostChoicesListView, self).get_queryset()
        if self.is_last:
            return qs
        if self.is_populate:
            return qs.order_by('-rate')
        if self.is_commented:
            return qs.order_by('-num_comments')
        return qs.none()


class PostCategoryListView(PostListView):
    template_name = 'post-category-list.html'

    def get_context_data(self, **kwargs):
        kwargs = super(PostCategoryListView, self).get_context_data(**kwargs)
        category = Category.objects.filter(slug=self.kwargs['category_slug']).first()
        if category is None:
            raise Http404
        kwargs['category'] = category
        return kwargs

    def get_queryset(self):
        return self.model.objects.filter(is_published=True, category__slug=self.kwargs['category_slug'])


class PostCategoryDetailView(DetailView):
    model = Post
    template_name = 'post.html'

    def get_object(self, queryset=None):
        if queryset is None:
            qs = self.model.objects.filter(is_published=True)
        obj = super(PostCategoryDetailView, self).get_object(queryset=qs)
        obj.view_action(self.request.session)
        return obj

    def get_context_data(self, **kwargs):
        kwargs = super(PostCategoryDetailView, self).get_context_data(**kwargs)
        kwargs['similar_posts'] = self.model.objects.filter(
            is_published=True,
            category=self.object.category
        ).exclude(id=self.object.id)[:5]
        kwargs['comments'] = self.object.comments()
        kwargs['comment_form'] = CommentForm(user=self.request.user)
        return kwargs


class CommentUserListView(ListView):
    model = Comment
    paginate_by = 10
    template_name = 'comment-list.html'

    def get_queryset(self):
        qs = super(CommentUserListView, self).get_queryset()
        return qs.filter(
            author=self.request.user,
            is_published=True,
            post__is_published=True
        )

    @method_decorator(login_required(login_url=reverse_lazy('u-login')))
    def dispatch(self, *args, **kwargs):
        return super(CommentUserListView, self).dispatch(*args, **kwargs)


def comment_json(request):
    instance = None
    comment_id = request.POST.get('comment_id', None)
    if comment_id is not None and comment_id.isdigit():
        instance = Comment.objects.filter(id=comment_id).first()
    form = CommentForm(user=request.user, data=request.POST, instance=instance)
    if form.is_valid():
        comment = form.save()
        return JsonResponse({
            'result': 'success',
            'is_created': instance is None,
            'data': model_to_dict(comment),
            'id': comment.id,
            'parent_id': comment.parent.id if comment.parent is not None else None,
            'html_data': render_to_string('comment.html', {'node': comment, 'user': request.user, 'request': request})
        })
    else:
        return JsonResponse({'result': 'error', 'data': form.errors.as_text()})


def comment_like(request):
    pk = request.POST.get('pk', None)
    if pk is not None and pk.isdigit():
        obj = Comment.objects.filter(pk=pk).first()
        if obj is not None:
            obj.like_action(request.session)
            rate = obj.rate
            rate_represent = '%s' % rate
            if rate > 0:
                rate_represent = '+%s' % rate
            return JsonResponse({'rate': rate_represent})
    return JsonResponse({})


def comment_unlike(request):
    pk = request.POST.get('pk', None)
    if pk is not None and pk.isdigit():
        obj = Comment.objects.filter(pk=pk).first()
        if obj is not None:
            obj.unlike_action(request.session)
            rate = obj.rate
            rate_represent = '%s' % rate
            if rate > 0:
                rate_represent = '+%s' % rate
            return JsonResponse({'rate': rate_represent})
    return JsonResponse({})


def post_like(request):
    pk = request.POST.get('pk', None)
    if pk is not None and pk.isdigit():
        obj = Post.objects.filter(pk=pk).first()
        if obj is not None:
            obj.like_action(request.session)
            rate = obj.rate
            rate_represent = '%s' % rate
            if rate > 0:
                rate_represent = '+%s' % rate
            return JsonResponse({'rate': rate_represent})
    return JsonResponse({})


def post_unlike(request):
    pk = request.POST.get('pk', None)
    if pk is not None and pk.isdigit():
        obj = Post.objects.filter(pk=pk).first()
        if obj is not None:
            obj.unlike_action(request.session)
            rate = obj.rate
            rate_represent = '%s' % rate
            if rate > 0:
                rate_represent = '+%s' % rate
            return JsonResponse({'rate': rate_represent})
    return JsonResponse({})
