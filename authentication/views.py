from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from authentication.models import CustomUser


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class UserDataDetailView(DetailView):
    model = CustomUser
    template_name = 'user_details.html'

    def get_object(self, queryset=None):
        return self.request.user
