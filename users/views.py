from django.contrib.auth.views import LoginView, FormView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from .forms import SignUpForm
from .permission_mixins import SignUpPermissionMixin
from django.contrib.auth.views import LogoutView

UserModel = get_user_model()
# Create your views here.


class SignInView(LoginView):
    # authentication_form = SignInForm
    template_name = 'users/sign-in.html'
    next_page = reverse_lazy('main:main')
    redirect_authenticated_user = True


class SignUpView(SignUpPermissionMixin, FormView):
    form_class = SignUpForm
    template_name = 'users/sign-up.html'
    success_url = reverse_lazy('users:sign-in')

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if form.is_valid():
            form.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class LogOutView(LogoutView):
    next_page = reverse_lazy('users:sign-in')
