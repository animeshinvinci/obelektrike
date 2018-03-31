from apps.cms.models import Feedback
from apps.generic.forms import BootstrapModelForm


class FeedbackForm(BootstrapModelForm):

    class Meta:
        model = Feedback
        fields = ('name', 'email', 'message')
