from django.contrib.auth import login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from accounts.forms import MyUserCreationForm, UserChangeForm, ProfileChangeForm
from accounts.models import Profile
from webapp.models import Photo, Album


class RegisterView(CreateView):
    model = User
    template_name = 'registration.html'
    form_class = MyUserCreationForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        Profile.objects.create(user=user)
        return redirect(self.get_success_url())

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if not next_url:
            next_url = self.request.POST.get('next')
        if not next_url:
            next_url = reverse('webapp:index')
        return next_url


class ProfileView(DetailView):
    model = get_user_model()
    template_name = 'profile_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user == self.object:
            context['photos'] = Photo.objects.filter(author=self.object, )
            context['albums'] = Album.objects.filter(author_album=self.object, )
        else:
            context['photos'] = Photo.objects.filter(author=self.object, private=False)
            context['albums'] = Album.objects.filter(author_album=self.object, private=False)
        return context


class ChangeProfileView(PermissionRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = UserChangeForm
    template_name = 'change_user.html'
    profile_form = ProfileChangeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'profile_form' not in context:
            context['profile_form'] = self.profile_form(instance=self.get_object().profile)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(instance=self.object, data=request.POST)
        profile_form = self.profile_form(instance=self.object.profile, data=request.POST, files=request.FILES)
        if form.is_valid() and profile_form.is_valid():
            return self.form_valid(form, profile_form)
        else:
            return self.form_invalid(form, profile_form)

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form, profile_form):
        form.save()
        profile_form.save()
        return redirect('accounts:profile_view', self.object.pk)

        def form_invalid(self, form, profile_form):
            return self.render_to_response(self.get_context_data(form=form, profile_form=profile_form))

    def has_permission(self):
        return self.request.user == self.get_object()


class ChangePasswordView(PasswordChangeView):
    template_name = 'change_password.html'

    def get_success_url(self):
        return reverse('accounts:profile_view', kwargs={'pk': self.request.user.pk})
