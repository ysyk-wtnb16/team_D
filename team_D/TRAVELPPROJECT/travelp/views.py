from django.shortcuts import render

from django.views.generic.base import TemplateView

class IndexView(TemplateView):

    template_name = 'index.html'

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

class S_homeView(TemplateView):

    template_name = 's_home.html'

class S_sinseiView(TemplateView):

    template_name = 's_sinsei.html'

class S_pageView(TemplateView):

    template_name = 's_page.html'

class S_postView(TemplateView):

    template_name = 's_post.html'

class S_historyView(TemplateView):

    template_name = 's_history.html'