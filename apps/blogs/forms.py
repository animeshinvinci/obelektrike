from apps.blogs.models import Comment
from apps.generic.forms import BootstrapModelForm


class CommentForm(BootstrapModelForm):

    def __init__(self, user, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.user = user
        if self.user.is_authenticated:
            self.fields['author_username'].required = False

    def clean_comment(self):
        comment = self.cleaned_data['comment']
        self.clean_on_spam(comment)
        return comment

    def save(self, *args, **kwargs):
        self.instance.is_deleted = False
        self.instance.is_published = True
        if self.user.is_authenticated:
            self.instance.author = self.user
            self.instance.author_username = self.user.get_full_name()
        return super(CommentForm, self).save(*args, **kwargs)

    class Meta:
        model = Comment
        fields = ('parent', 'post', 'author', 'author_username', 'comment')
