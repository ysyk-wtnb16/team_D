# Django standard imports
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from django.db.models import Q
from django.contrib import messages
from django.conf import settings
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, CreateView, FormView, View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .forms import ProfileEditForm, PostCreateForm, CommentForm, DonationForm, FundraisingForm
from .models import Post, PostImage, Comment, Like, CustomUser, Plan, Fundraising, Donation
from . import models

# Stripe API
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


 
class IndexView(ListView):
    template_name = 'index.html'
 
    queryset = Post.objects.order_by('-created_at')
    # 1ページに表示するレコードの件数
    paginate_by = 6
 
def post_list(request):
    posts = Post.objects.all().order_by('-created_at')  # 全投稿を取得（新しい順）
   
    # スタッフの募金投稿のみ取得
    staff_posts = Post.objects.filter(user__is_staff=True, fundraising__isnull=False).order_by('-created_at')
   
    final_posts = []
    staff_index = 0
    staff_count = staff_posts.count()
 
    for i, post in enumerate(posts):
        final_posts.append(post)
        if (i + 1) % 5 == 0 and staff_index < staff_count:
            final_posts.append(staff_posts[staff_index])
            staff_index += 1
 
    return render(request, 'posts_list.html', {'posts': final_posts})
 
# 商品検索ビュー
class SearchView(ListView):
    template_name = "search.html"
    model = Post
 
# 検索ビュー
class SearchResultView(ListView):
    template_name = "search_result.html"
    model = Post
 
    # 一覧表示するデータを取得するメソッド
    def get_queryset(self):
        # 入力された検索ワードを含む商品名に商品を取得する
        # GETメソッドで送信されたkeywordの値を取得
        keyword = self.request.GET.get("keyword", "")
        if keyword != "":
            # select * from product where name like '%keyword%'
            post = models.Post.objects.filter(title__contains=keyword)
        else:
            # 検索ワードが入力されていなかったら空オブジェクトにする
            post = models.Post.objects.none()
        return post
 
 
class ProfileView(TemplateView):
    template_name = 'profile.html'
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
       
        # 投稿者を取得
        post_id = self.kwargs['pk']  # URLから投稿IDを取得（URLで渡す）
        post = get_object_or_404(Post, pk=post_id)
        user = post.user  # 投稿のユーザー情報を取得
 
        context['user'] = user
        context['user_posts'] = Post.objects.filter(user=user)  # ユーザーが投稿した投稿
        context['liked_posts'] = Post.objects.filter(likes__user=user)  # ユーザーがイイネした投稿
        context['commented_posts'] = Post.objects.filter(comments__user=user)  # ユーザーがコメントした投稿
       
        return context
   
class MyProfileView(TemplateView):
    template_name = 'myprofile.html'
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
       
        user = self.request.user  # ログインしているユーザー情報を取得
        context['user'] = user
        context['user_posts'] = Post.objects.filter(user=user)  # ユーザーが投稿した投稿
        context['liked_posts'] = Post.objects.filter(likes__user=user)  # ユーザーがイイネした投稿
        context['commented_posts'] = Post.objects.filter(comments__user=user)  # ユーザーがコメントした投稿
       
        return context
 
 
class EditProfileView(UpdateView):
    model = CustomUser  # 編集するモデルを指定
    form_class = ProfileEditForm  # 使用するフォームクラスを指定
    template_name = 'edit_profile.html'  # 使用するテンプレートを指定
    success_url = reverse_lazy('travelp:myprofile')  # 編集が成功した後にリダイレクトするURL
 
    def get_object(self, queryset=None):
        # 現在ログインしているユーザーのプロフィールを取得
        return self.request.user
 
    def form_valid(self, form):
        # フォームが有効な場合に、変更を保存
        form.save()
        return redirect(self.success_url)
   
    def profile_edit(request, user_id):
        if request.user.pk != user_id:
            # 自分のプロフィールでなければ、アクセス禁止またはリダイレクト
            return redirect('profile_detail', user_id=request.user.pk)
 
class PostCreateView(LoginRequiredMixin, CreateView):
    form_class = PostCreateForm
    template_name = "post.html"
    success_url = reverse_lazy('travelp:post_done')
 
    def get_form_kwargs(self):
        """フォームに現在のユーザー情報を渡す"""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # user を追加
        return kwargs
 
    def form_valid(self, form):
            print("form_validが呼ばれた！")  # ここで確認
            postdata = form.save(commit=False)
            postdata.user = self.request.user
   
            # フォームからの緯度・経度取得
            lat = form.cleaned_data.get('latitude')
            lon = form.cleaned_data.get('longitude')
   
            # 緯度・経度を丸めて保存
            postdata.latitude = round(lat, 8) if lat else None  # 小数点以下6桁に丸める
            postdata.longitude = round(lon, 8) if lon else None  # 小数点以下9桁に丸める
   
            print("保存する緯度:", postdata.latitude)
            print("保存する経度:", postdata.longitude)
   
            postdata.save()
   
            # 画像を保存
            images = self.request.FILES.getlist('images')
            for image in images:
                PostImage.objects.create(post=postdata, image=image)
   
            return super().form_valid(form)
 
   
    def form_invalid(self, form):
        print("form_invalidが呼ばれた！")  
        print("フォームエラー:", form.errors)  
 
        # フォームデータの中身を確認！
        print("受け取った緯度 (latitude):", self.request.POST.get('latitude'))
        print("受け取った経度 (longitude):", self.request.POST.get('longitude'))
 
        return super().form_invalid(form)
 
 
class PostSuccessView(TemplateView):
    template_name = 'post_success.html'
 
# 投稿を削除
class DeletePostView(View):
    @method_decorator(login_required)
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        if post.user == request.user:
            post.delete()
        return redirect('travelp:index')
 
class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
 
        # **この投稿を含むプランを取得**
        context['plans'] = Plan.objects.filter(posts=self.object)
       
        # **デバッグ: プランの数をログに出す**
        print(f"DEBUG: {self.object.title} を含むプラン数 → {context['plans'].count()}")
 
        post = self.object  # 現在表示されている投稿オブジェクトを取得
 
        context['comments'] = Comment.objects.filter(post=post)
       
        # ログインしている場合のみ、いいねの状態をチェック
        if self.request.user.is_authenticated:
            context['liked'] = post.liked_by_user(self.request.user)  # いいねしているか確認
        else:
            context['liked'] = False  # ログインしていない場合はいいねなし
        return context
   
    def post_detail(request, post_id):
        post = get_object_or_404(Post, id=post_id)

        fundraising = get_object_or_404(Fundraising, post=post)  # 投稿に関連する募金プロジェクト
 
        # **イイネ or コメントがない場合はリダイレクト**
        if not (post.likes.filter(id=request.user.id).exists() or post.comments.filter(user=request.user).exists()):
            return redirect('some_other_page')
 
        # **この投稿が含まれる全てのプランを取得（どのユーザーのプランでもOK）**
        plans = Plan.objects.filter(posts=post)
 
        print(f"DEBUG: {post.title} を含むプラン数 → {plans.count()}")
        
        return render(request, 'post_detail.html', {'post': post, 'plans': plans, 'fundraising': fundraising})
        
    def fundraising_detail(request, pk):
        project = get_object_or_404(Fundraising, pk=pk)
        donations = project.donations.all().order_by('-date')  # 新しい順に募金履歴を取得
    
        if request.method == "POST":
            form = DonationForm(request.POST)
            if form.is_valid():
                donation = form.save(commit=False)
                donation.project = project  # どの募金プロジェクトへの募金か設定
                donation.donor = request.user  # 現在のユーザーを募金者として設定
                donation.save()  # 保存
    
                return redirect('travelp:fundraising_detail', pk=project.pk)  # ページを再読み込み
    
        else:
            form = DonationForm()
    
        return render(request, 'fundraising/fundraising_detail.html', {
            'project': project,
            'donations': donations,
            'form': form,  # フォームをテンプレートに渡す
        })
    
 


class PostLikeView(View):
    @method_decorator(login_required)
    def post(self, request, post_pk):
        post = get_object_or_404(Post, pk=post_pk)
 
        # すでに「いいね」がされているか確認
        like, created = Like.objects.get_or_create(post=post, user=request.user)
 
        if not created:
            # いいねがすでに存在する場合、削除
            like.delete()
            liked = False
        else:
            # 新しい「いいね」を追加
            liked = True
 
        # いいね数を取得
        like_count = post.likes.count()
 
        return JsonResponse({'liked': liked, 'like_count': like_count})
 
class AddCommentView(View):
    def post(self, request, post_pk):
        post = get_object_or_404(Post, pk=post_pk)
        comment_text = request.POST.get('comment')
        Comment.objects.create(user=request.user, post=post, text=comment_text)
        return redirect('travelp:post_detail', pk=post_pk)
 
def liked_posts(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    liked_posts = Post.objects.filter(likes=user)  # いいねした投稿を取得
    return render(request, 'travelp/liked_posts.html', {'user': user, 'liked_posts': liked_posts})
 
def commented_posts(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    commented_posts = Post.objects.filter(comments__user=user).distinct()  # コメントした投稿を取得
    return render(request, 'travelp/commented_posts.html', {'user': user, 'commented_posts': commented_posts})
 
   
# コメントを削除
class DeleteCommentView(View):
    @method_decorator(login_required)
    def post(self, request, post_pk, comment_id):
        post = get_object_or_404(Post, pk=post_pk)
        comment = get_object_or_404(Comment, pk=comment_id)
        if comment.user == request.user:
            comment.delete()
        return redirect('travelp:post_detail', pk=post_pk)
 
def user_posts(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)  # ユーザーを取得
    posts = Post.objects.filter(user=user)  # そのユーザーの投稿を取得
    return render(request, 'user_posts.html', {'user': user, 'posts': posts})
 
 
 
@login_required
def mypost(request):
    posts_list = Post.objects.filter(user=request.user).order_by('-created_at')
 
    # 🔹 Paginator を適用（1ページに6件表示）
    paginator = Paginator(posts_list, 6)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)  # 現在のページのオブジェクトを取得
 
    if request.method == 'POST':
        # プラン作成処理
        plan_name = request.POST.get('plan_name')
        selected_posts = request.POST.getlist('selected_posts')
 
        # Planの作成
        plan = Plan.objects.create(user=request.user, name=plan_name)
 
        # 投稿をプランに関連付け
        for post_id in selected_posts:
            post = Post.objects.get(pk=post_id)
            plan.posts.add(post)
 
        return redirect('travelp:myplan')  # 作成したプランページにリダイレクト
 
    return render(request, 'mypost.html', {'posts': posts})
 
@login_required
def myplan(request):
    plans = Plan.objects.filter(user=request.user).order_by('-id')  # 自分の作成したプランを取得（新しい順）
 
    # 🔹 Paginator を適用（1ページに6件表示）
    paginator = Paginator(plans, 6)
    page_number = request.GET.get('page')
    plans = paginator.get_page(page_number)  # 現在のページのオブジェクトを取得
 
    for plan in plans:
        # 各プランの中で一番古い投稿を取得
        plan.thumbnail = plan.posts.order_by('created_at').first()
    return render(request, 'myplan.html', {'plans': plans})
 
@login_required
def plan_detail(request, plan_id):
    plan = get_object_or_404(Plan, id=plan_id)  # どのユーザーのプランでも取得可能に
 
     # 投稿の位置情報を取得
    post_locations = []
    for post in plan.posts.all():
        if post.latitude and post.longitude:  # 位置情報がある場合
            post_locations.append({
                'latitude': post.latitude,
                'longitude': post.longitude,
                'title': post.title,
            })
   
    return render(request, 'plan_detail.html', {
        'plan': plan,
        'post_locations': post_locations
    })
 
 
@login_required
def save_plan(request):
    if request.method == "POST":
        plan_name = request.POST.get('plan_name')
        selected_post_ids = request.POST.getlist('selected_posts')
        selected_posts = Post.objects.filter(id__in=selected_post_ids)
 
        # プランを作成
        plan = Plan.objects.create(name=plan_name, user=request.user)
        plan.posts.add(*selected_posts)  # 選択した投稿をプランに追加
 
        return redirect('travelp:myplan', plan.pk)
 
    return redirect('travelp:mypost')
 
def create_plan(request):
    if request.method == 'POST':
        # 選択された投稿を取得
        selected_posts = request.POST.getlist('selected_posts')  # 複数の投稿IDを取得
       
        # Planの作成
        plan = Plan.objects.create(user=request.user)
       
        # 投稿をプランに関連付ける
        for post_id in selected_posts:
            post = Post.objects.get(pk=post_id)
            plan.posts.add(post)  # `posts` は Plan モデルで定義された ManyToMany フィールド
       
        return redirect('travelp:myplan', plan_id=plan.id)  # 作成したプランページにリダイレクト
   
    return redirect('travelp:mypost')  # GETリクエストの場合は自分の投稿ページにリダイレクト
 
 
 
def user_plans(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)  # ユーザーを取得
    plans = Plan.objects.filter(user=user)  # そのユーザーのプランを取得
    return render(request, 'user_plans.html', {'user': user, 'plans': plans})
 
@login_required
def delete_plan(request, plan_id):
    """プランを削除"""
    plan = get_object_or_404(Plan, id=plan_id, user=request.user)
    plan.delete()
    return redirect('travelp:myplan')  # 削除後にプラン一覧へリダイレクト
 

 
def fundraising_list(request):
    fundraising_projects = Fundraising.objects.all()
    return render(request, 'fundraising/fundraising_list.html', {'fundraising_projects': fundraising_projects})
 
 
def fundraising_detail(request, pk):
    project = get_object_or_404(Fundraising, pk=pk)
    donations = project.donations.all().order_by('-date')  # 新しい順に募金履歴を取得
 
    if request.method == "POST":
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.project = project  # どの募金プロジェクトへの募金か設定
            donation.donor = request.user  # 現在のユーザーを募金者として設定
            donation.save()  # 保存
 
            return redirect('travelp:fundraising_detail', pk=project.pk)  # ページを再読み込み
 
    else:
        form = DonationForm()
 
    return render(request, 'fundraising/fundraising_detail.html', {
        'project': project,
        'donations': donations,
        'form': form,  # フォームをテンプレートに渡す
    })
 
 
 
def donate(request, pk):
    project = get_object_or_404(Fundraising, pk=pk)
   
    if request.method == "POST":
        form = DonationForm(request.POST)
        if form.is_valid():
            # フォームから情報を取得
            card_number = request.POST.get("card_number", None)
            expiry_date = request.POST.get("expiry_date", None)
            cvv = request.POST.get("cvv", None)
            amount = form.cleaned_data['amount']
           
            # セキュリティチェックや支払いゲートウェイの処理を追加
            # 仮の支払い成功処理
            # 実際の支払い処理では、カード情報を扱う際にAPIや支払いゲートウェイを使用します。
            if amount <= 0:
                messages.error(request, "募金額は1円以上にしてください。")
                return redirect('fundraising:fundraising_detail', pk=project.pk)
           
            # 実際の支払い処理はここに実装されます
            # 例: 支払いゲートウェイでカード情報を送信して決済を実行
           
            # 募金情報を保存
            donation = Donation(
                project=project,
                donor=request.user,
                amount=amount
            )
            donation.save()
           
            # 目標金額を更新
            project.raised_amount += amount
            project.save()
           
            messages.success(request, f"¥{amount}の募金が成功しました！")
            return redirect('fundraising:fundraising_detail', pk=project.pk)
        else:
            messages.error(request, "フォームに誤りがあります。再度ご確認ください。")
    else:
        form = DonationForm()
 
    return render(request, 'fundraising/donate.html', {'form': form, 'project': project})
 
def donation_history(request):
    donations = Donation.objects.filter(donor=request.user)  # 現在ログインしているユーザーの募金履歴を取得
    return render(request, 'fundraising/donation_history.html', {'donations': donations})
 
def donation_detail(request, pk):
    donation = get_object_or_404(Donation, pk=pk)
    return render(request, 'fundraising/donation_detail.html', {'donation': donation})
 

 
@login_required
def create_fundraising(request):
    if request.user.is_staff:  # 管理者（市役所）かどうかチェック
        if request.method == "POST":
            form = FundraisingForm(request.POST)
            if form.is_valid():
                fundraising = form.save(commit=False)
                fundraising.created_by = request.user  # ログインしてる管理者を設定
                fundraising.save()
                return redirect('travelp:fundraising_list')  # 募金一覧へリダイレクト
        else:
            form = FundraisingForm()
        return render(request, 'fundraising/create_fundraising.html', {'form': form})
    else:
        return redirect('travelp:index')  # 一般ユーザーならホームへリダイレクト
 
@login_required
def fundraising_delete(request, pk):
    project = get_object_or_404(Fundraising, pk=pk)
 
    # 市役所ユーザー（管理者）のみ削除可能
    if request.user.is_staff:
        project.delete()
        return redirect('travelp:fundraising_list')
   
    return redirect('travelp:fundraising_detail', pk=pk)
 
 
@csrf_exempt
def create_checkout_session(request, pk):
    project = get_object_or_404(Fundraising, id=pk)
 
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'jpy',
                'product_data': {
                    'name': project.title,
                },
                # 'unit_amount': "amount",  # 募金額を動的に取得する場合は後で変更
                'unit_amount': 1000,  # 募金額を動的に取得する場合は後で変更
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('travelp:fundraising_detail', args=[project.id])) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse('travelp:fundraising_detail', args=[project.id])),
    )
 
    return redirect(session.url, code=303)

 
def donate(request, pk):
    project = get_object_or_404(Fundraising, pk=pk)
 
    if request.method == "POST":
        form = DonationForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            payment_method = request.POST.get("payment")
 
            if amount <= 0:
                messages.error(request, "募金額は1円以上にしてください。")
                return redirect('travelp:fundraising_detail', pk=project.pk)
 
            if payment_method == "pbank":
                # 銀行振込の場合のみ処理
                donation = Donation(
                    project=project,
                    donor=request.user,
                    amount=amount
                )
                donation.save()
                project.raised_amount += amount
                project.save()
 
                messages.success(request, f"¥{amount}の募金が成功しました！")
                return redirect('travelp:fundraising_detail', pk=project.pk)