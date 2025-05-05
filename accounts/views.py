from django.views.generic import CreateView, DetailView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f'Cadastro realizado com sucesso para {form.cleaned_data["email"]}!'
        )
        return response

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    
    def get_success_url(self):
        messages.success(self.request, f'Bem-vindo(a), {self.request.user.username}!')
        return reverse_lazy('home')

class ProfileView(LoginRequiredMixin, DetailView):
    template_name = 'accounts/profile.html'
    context_object_name = 'user_profile'

    def get_object(self):
        return self.request.user

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, "Você foi desconectado com sucesso.")
        return super().dispatch(request, *args, **kwargs)