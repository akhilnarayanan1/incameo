from django.views.generic import TemplateView

class IndexView(TemplateView):
    template_name = "index.html"
    extra_context = {'title': 'Home Page'}

class SignupView(TemplateView):
    template_name = "signup.html"
    extra_context = {'title': 'Signup'}

class LoginView(TemplateView):
    template_name = "login.html"
    extra_context = {'title': 'Login'}