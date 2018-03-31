from django.contrib import admin

from apps.blogs.admin import PostAdmin
from apps.blogs.models import Category
from apps.questions.models import Question


class QuestionAdmin(PostAdmin):

    def get_queryset(self, request):
        qs = super(PostAdmin, self).get_queryset(request)
        return qs.filter(category__categorytype=Category.CATEGORY_QUESTIONS)


admin.site.register(Question, QuestionAdmin)
