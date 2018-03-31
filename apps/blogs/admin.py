from django.contrib import admin
from django.utils.translation import ugettext_lazy as _ul

from apps.blogs.models import Category, Comment, Post, Tag
from apps.generic.admin import GenericModelAdmin


@admin.register(Tag)
class TagAdmin(GenericModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(GenericModelAdmin):
    list_display = (
        'name',
        'is_published',
        GenericModelAdmin.site_url,
    )
    list_filter = (
        'is_published',
        'categorytype'
    )
    fieldsets = (
        (None, {
            'fields': (
                'name',
                'description',
                'categorytype',
                'image_class',
            )
        }),
        (_ul(u'Доступ'), {
            'fields': (
                'is_published',
            )
        }),
        (_ul(u'Seo'), {
            'fields': (
                'slug',
                'seo_title',
                'seo_description',
                'seo_keywords',
                'seo_author'
            )
        }),
    )
    search_fields = ('name', 'description',)


@admin.register(Post)
class PostAdmin(GenericModelAdmin):
    list_display = (
        'title',
        'category',
        'author',
        'rate',
        'view_count',
        'num_comments',
        'publication_date',
        'is_published',
        GenericModelAdmin.site_url,
    )
    list_filter = (
        'is_published',
        'category',
    )
    fieldsets = (
        (None, {
            'fields': (
                'author',
                'category',
                'tags',
                'title',
                'picture',
                'announcement',
                'post',
            )
        }),
        (_ul(u'Доступ'), {
            'fields': (
                'is_published',
                'publication_date',
            )
        }),
        (_ul(u'Seo'), {
            'fields': (
                'slug',
                'seo_title',
                'seo_description',
                'seo_keywords',
                'seo_author'
            )
        }),
        (_ul(u'Голосование'), {
            'fields': (
                'rate',
            )
        }),
        (_ul(u'Заметки'), {
            'fields': (
                'notes',
            )
        }),
    )
    filter_horizontal = ('tags',)
    search_fields = ('title', 'announcement',)

    def formfield_for_dbfield(self, db_field, *args, **kwargs):
        formfield = super(PostAdmin, self).formfield_for_dbfield(db_field, *args, **kwargs)
        if db_field.name == 'author':
            formfield.initial = kwargs['request'].user
        if db_field.name == 'seo_author':
            formfield.initial = kwargs['request'].user.get_full_name()
        if db_field.name == 'is_published':
            formfield.initial = False
            formfield.help_text = """
            Перед публикацией разместите статью в
            <br>
            <a href="https://webmaster.yandex.ru/site/service-plugin.xml?host=22600389&service=ORIGINALS&need_auth=false&new_site=false">
            Yandex оригинальные тексты</a>
            """ # noqa
        return formfield

    def get_queryset(self, request):
        qs = super(PostAdmin, self).get_queryset(request)
        return qs.exclude(category__categorytype=Category.CATEGORY_QUESTIONS)

    class Media:
        js = (
            '/static/jquery/jquery.min.js',
            '/static/jquery/jquery.synctranslit.min.js',
            '/static/site/js/admin.js',
        )


@admin.register(Comment)
class CommentAdmin(GenericModelAdmin):
    search_fields = ('comment', 'author_username', 'author__username')
    list_display = (
        'comment',
        'creation_date',
        'author_username',
        'is_published',
        'is_spam',
        GenericModelAdmin.site_url,
    )
    list_filter = (
        'is_spam',
        'is_published',
    )
    list_editable = (
        'is_spam',
        'is_published',
    )
    fieldsets = (
        (None, {
            'fields': (
                'comment',
            )
        }),
        (_ul(u'Доступ'), {
            'fields': (
                'is_published',
                'is_spam'
            )
        }),
        (_ul(u'Голосование'), {
            'fields': (
                'rate',
            )
        }),
        (_ul(u'Связи'), {
            'fields': (
                'parent',
                'post',
            )
        }),
        (_ul(u'Автор'), {
            'fields': (
                'author',
                'author_username',
            )
        }),
    )
    readonly_fields = ('parent', 'post', 'author', 'author_username')
