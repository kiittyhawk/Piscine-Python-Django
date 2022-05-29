from ast import For, arg
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from typing import Any, Dict
from django.urls import reverse_lazy
from django.views.generic import ListView, RedirectView, CreateView, DetailView, FormView
from requests import request
from ex.forms.favourite import FavouriteForm
from ex.forms.register import RegisterForm
from ex.forms.login import LoginForm
from ex.forms.create import CreateArticle
from ex.models.article import Article, UserFavouriteArticle
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.db import DatabaseError
from django.contrib.auth.forms import AuthenticationForm
from django.forms.forms import BaseForm


class Articles(ListView):
    model = Article
    template_name = 'ex/articles.html'
    queryset = Article.objects.filter().order_by('-created')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context


class Home(RedirectView):
    url = reverse_lazy('articles')


class Login(LoginView):
    template_name = 'ex/login.html'
    form_class = LoginForm

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if self.request.user.is_authenticated:
            messages.error(self.request, 'You already loggined!')
            return redirect('index')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form: LoginForm) -> HttpResponse:
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password)
        if user is None:
            messages.error(self.request, 'Invalid username or password')
            return
        login(self.request, user)
        messages.info(self.request, f'You are now logged in as {username}')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('index')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context


class Register(CreateView):
    form_class = RegisterForm
    template_name = 'ex/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form: RegisterForm):
        user = form.save()
        login(self.request, user)
        return redirect('index')


def logout_Us(request):
    logout(request)
    return redirect('login')


class Detail(DetailView):
    model = Article
    template_name = 'ex/detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        article = context['object']
        context["favouriteForm"] = FavouriteForm(article.id)
        return context


class Favourites(ListView, FormView):
    template_name = "ex/favourites.html"
    form_class = FavouriteForm
    success_url = reverse_lazy('index')
    login_url = reverse_lazy('index')
    model: UserFavouriteArticle = UserFavouriteArticle

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def form_valid(self, form: AuthenticationForm):
        article_id = form.cleaned_data['article']
        try:
            UserFavouriteArticle.objects.get(
                article=article_id, user=self.request.user).delete()
            messages.success(
                self.request, "successful Remove to favourite.")
        except UserFavouriteArticle.DoesNotExist as e:
            try:
                UserFavouriteArticle.objects.create(
                    user=self.request.user,
                    article=Article.objects.get(id=article_id),
                )
                messages.success(
                    self.request, "successful Add to favourite.")
            except DatabaseError as e:
                messages.error(
                    self.request, "Unsuccessful Add to favourite. Database error.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, "Unsuccessful Add to favourite. Invalid information.{}".format(form.data.get('article')))
        return redirect('index')

    def get_form(self, form_class=None) -> BaseForm:
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(None, **self.get_form_kwargs())


class CreateArticle(FormView):
    form_class = CreateArticle
    template_name = 'ex/publish.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form: CreateArticle):
        title = form.cleaned_data['title']
        synopsis = form.cleaned_data['synopsis']
        content = form.cleaned_data['content']
        try:
            Article.objects.create(
                title=title,
                author=self.request.user,
                synopsis=synopsis,
                content=content
            )
        except DatabaseError as e:
            messages.success(
                self.request, "Unsuccessful publish. DatabaseError")
            return redirect('index')
        messages.success(self.request, "Successful publish.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, "Unsuccessful publish. Invalid information.")
        return super().form_invalid(form)
