from django.urls import re_path, reverse_lazy
from django.views.generic import RedirectView

from apps.blogs import views as blogs_views
from apps.cms import views as cms_views
from apps.generic import views as generic_views
from apps.users import views as users_views

urlpatterns = [
    re_path(
        r'^$',
        blogs_views.IndexView.as_view(),
        name='index'),

    re_path(
        r'^poslednie-statyi/$',
        blogs_views.PostChoicesListView.as_view(is_last=True),
        name='posts-last-list'),
    re_path(
        r'^popularnye-statyi/$',
        blogs_views.PostChoicesListView.as_view(is_populate=True),
        name='posts-popular-list'),
    re_path(
        r'^kommentiruemye-statyi/$',
        blogs_views.PostChoicesListView.as_view(is_commented=True),
        name='posts-commented-list'),
    re_path(
        r'^poisk/$',
        blogs_views.PostSearchListView.as_view(),
        name='posts-search'),
    re_path(
        r'^kontakty/$',
        cms_views.FeedbackCreateView.as_view(),
        name='feedback'),
    re_path(
        r'^reklamodatelyam/$',
        cms_views.FlatPageDetailView.as_view(
            template_name='advertisers.html'
        ),
        name='advertisers'),
    re_path(
        r'^pravila-i-avtorskie-prava/$',
        cms_views.FlatPageDetailView.as_view(
            template_name='rules.html'
        ),
        name='rules'),

    re_path(
        r'^posts/$',
        blogs_views.PostListView.as_view(),
        name='posts-list'),
    re_path(
        r'^posts/(?P<slug>[-_\w]+)/$',
        blogs_views.PostCategoryDetailView.as_view(),
        name='posts-category-detail'),
    re_path(
        r'^category/(?P<category_slug>[-_\w]+)/$',
        blogs_views.PostCategoryListView.as_view(),
        name='posts-category-list'),

    re_path(
        r'^u/login/$',
        users_views.LoginView.as_view(),
        name='u-login'),
    re_path(
        r'^u/logout/$',
        users_views.LogoutView.as_view(),
        name='u-logout'),
    re_path(
        r'^u/registration/$',
        users_views.RegistrationView.as_view(),
        name='u-registration'),
    re_path(
        r'^u/registration/(?P<uuid>.*)/$',
        users_views.RegistrationUuidView.as_view(),
        name='u-registration-uuid'),
    re_path(
        r'^u/reset/password/$',
        users_views.PasswordResetView.as_view(),
        name='u-reset-password'),
    re_path(
        r'^u/reset/password/(?P<uuid>.*)/$',
        users_views.PasswordResetUuidView.as_view(),
        name='u-reset-password-uuid'),
    re_path(
        r'^u/profile/(?P<pk>\d+)/$',
        users_views.UserDetailView.as_view(),
        name='u-profile'),
    re_path(
        r'^u/update/(?P<pk>\d+)/$',
        users_views.UserUpdateView.as_view(),
        name='u-update'),
    re_path(
        r'^u/password/$',
        users_views.PasswordChangeView.as_view(),
        name='u-password'),
    re_path(
        r'^u/subscribe/$',
        users_views.SubscribeUser.as_view(),
        name='subscribe-user'),

    re_path(
        r'^u/comments/$',
        blogs_views.CommentUserListView.as_view(), name='u-comments-list'),
    re_path(
        r'^json/comment/$',
        blogs_views.comment_json,
        name='json-comment'),
    re_path(
        r'^json/comment/like/$',
        blogs_views.comment_like,
        name='json-comment-like'),
    re_path(
        r'^json/comment/unlike/$',
        blogs_views.comment_unlike,
        name='json-comment-unlike'),
    re_path(
        r'^json/post/like/$',
        blogs_views.post_like,
        name='json-post-like'),
    re_path(
        r'^json/post/unlike/$',
        blogs_views.post_unlike,
        name='json-post-unlike'),
    re_path(
        r'^json/cms/vote/$',
        cms_views.cms_vote,
        name='json-cms-vote'),

    re_path(
        r'^m/$',
        RedirectView.as_view(url=reverse_lazy('index'))),
    re_path(
        r'^mobile/$',
        RedirectView.as_view(url=reverse_lazy('index'))),
    re_path(
        r'^posts/tag/(?P<tag_slug>[-_\w]+)/$',
        RedirectView.as_view(url=reverse_lazy('index'))),
    re_path(
        r'^karta-sajta\.html$',
        RedirectView.as_view(url=reverse_lazy('sitemap-html'))),
    re_path(
        r'^favicon\.ico$',
        RedirectView.as_view(url='/static/favicon.ico')),

    re_path(
        r'^robots\.txt$',
        generic_views.RobotTemplateView.as_view()),
    re_path(
        r'^sitemap\.xml$',
        generic_views.sitemap_xml),
    re_path(
        r'^sitemap-(?P<section>.+)\.xml$',
        generic_views.sitemap_xml),
    re_path(
        r'^sitemap\.html$',
        generic_views.sitemap_html,
        name='sitemap-html'),
    re_path(
        r'^feed\.rss$',
        generic_views.feed,
        name='feed'),

    re_path(
        r'^u/ckeditor/upload/',
        generic_views.ImageUploadView.as_view(),
        name='ckeditor_upload'),
]
