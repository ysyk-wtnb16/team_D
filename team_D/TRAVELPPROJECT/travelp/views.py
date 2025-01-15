from django.shortcuts import render
from django.core.paginator import Paginator
from django.views.generic.base import TemplateView
from .forms import PostForm
from . import models
posts=[]

class IndexView(TemplateView):

    template_name = 'index.html'

    # 一覧表示するデータを取得するメソッド
    def get_queryset(self):
        # 商品売れ筋ランキングTOP10の商品を取得
        # 商品売れ筋ランキング ＝ 商品と購入明細を結合して、数量の合計の降順
        # select 商品.*, sum(購入明細.数量) as sum
        #  from 商品 join 購入明細 on 商品.JANコード=購入明細.JANコード
        #  group by 商品.*
        #  order by sum desc
        products = (
            models.Product.objects
        )
        return products[:10]

    paginate_by = 4

class SearchView(TemplateView):

    template_name = 'search.html'

     # 一覧表示するデータを取得するメソッド
    def get_queryset(self):
        # 入力された検索ワードを含む商品名に商品を取得する
        # GETメソッドで送信されたkeywordの値を取得
        keyword = self.request.GET.get("keyword", "")
        if keyword != "":
            # select * from product where name like '%keyword%'
            products = models.Product.objects.filter(name__contains=keyword)
        else:
            # 検索ワードが入力されていなかったら空オブジェクトにする
            products = models.Product.objects.none
        return products

class PostView(TemplateView):

    template_name = 'post.html'

    def create_post(request):     
        if request.method == 'POST':         
            form = PostForm(request.POST)        
            if form.is_valid():             
                title = form.cleaned_data['title']             
                content = form.cleaned_data['content']             
                image = form.cleaned_data.get('image', None)  # 画像がある場合            
                posts.append({'title': title, 'content': content, 'image': image})             
                return render(request, 'post_list.html', {'posts': posts}) 
            else: form = PostForm() 
            return render(request, 'create_post.html', {'form': form})
        
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