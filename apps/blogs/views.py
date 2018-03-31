from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.http import Http404, JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _u
from django.utils.translation import ugettext_lazy as _ul
from django.views.generic import DetailView, ListView, TemplateView

from apps.blogs.forms import CommentForm
from apps.blogs.models import Category, Comment, Post


class IndexView(TemplateView):
    template_name = 'index.html'


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

    def get_context_data(self, **kwargs):
        kwargs = super(PostListView, self).get_context_data(**kwargs)
        page_obj = kwargs.get('page_obj', None)
        prev_page = None
        next_page = None
        baseurl = self.request.build_absolute_uri(location='')
        if page_obj is not None:
            prev_page = page_obj.previous_page_number() if page_obj.has_previous() else None
            next_page = page_obj.next_page_number() if page_obj.has_next() else None
        if prev_page:
            kwargs['meta_prev'] = baseurl + '?page=%s' % prev_page
        if next_page:
            kwargs['meta_next'] = baseurl + '?page=%s' % next_page
        return kwargs


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

    def get_context_data(self, **kwargs):
        kwargs = super(PostChoicesListView, self).get_context_data(**kwargs)
        if self.is_last:
            kwargs['title'] = _ul(u'Последние статьи')
        if self.is_populate:
            kwargs['title'] = _ul(u'Популярные статьи')
        if self.is_commented:
            kwargs['title'] = _ul(u'Комментируемые статьи')
        return kwargs


class PostCategoryListView(PostListView):
    template_name = 'post-category-list.html'

    def get_context_data(self, **kwargs):
        kwargs = super(PostCategoryListView, self).get_context_data(**kwargs)
        category = Category.objects.filter(slug=self.kwargs['category_slug']).first()
        if category is None:
            raise Http404
        kwargs['category'] = category
        kwargs['meta_title'] = '%s | %s' % (category.seo_title, _u(u'страница %s') % self.request.GET.get('page', 1))
        kwargs['meta_keywords'] = category.seo_keywords
        kwargs['meta_description'] = category.seo_description
        kwargs['meta_author'] = category.seo_author
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
        kwargs['meta_title'] = self.object.seo_title
        kwargs['meta_keywords'] = self.object.seo_keywords
        kwargs['meta_description'] = self.object.seo_description
        kwargs['meta_author'] = self.object.seo_author
        kwargs['meta_image'] = self.object.picture.url if self.object.picture else None
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
