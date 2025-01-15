from django.shortcuts import render
from django.core.paginator import Paginator
from django.views.generic.base import TemplateView

class IndexView(TemplateView):

    template_name = 'index.html'
    paginate_by = 4

class SearchView(TemplateView):

    template_name = 'search.html'

class PostView(TemplateView):

    template_name = 'post.html'

class ProfileView(TemplateView):

    template_name = 'profile.html'

class MypostView(TemplateView):

    template_name = 'mypost.html'

class MyplanView(TemplateView):

    template_name = 'myplan.html'

class PayView(TemplateView):

    template_name = 'pay.html'