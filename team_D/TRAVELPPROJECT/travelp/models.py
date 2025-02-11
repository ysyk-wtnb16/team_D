from django.db import models
from django.conf import settings
from accounts.models import CustomUser
from django.core.validators import MinValueValidator

# 募金機能
# from django.contrib.auth.models import User

class Fundraising(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    goal_amount = models.DecimalField(max_digits=10, decimal_places=2)
    collected_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def get_remaining_amount(self):
        return max(0, self.goal_amount - self.collected_amount)

    def is_completed(self):
        """目標額に達成しているかを判定"""
        return self.collected_amount >= self.goal_amount
 
class FundraisingProject(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    goal_amount = models.DecimalField(max_digits=10, decimal_places=2)
    collected_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)



class Donation(models.Model):
    # FundraisingProjectと関連付け（募金プロジェクトと紐づけ）
    project = models.ForeignKey(Fundraising, on_delete=models.CASCADE, related_name="donations")

    # ユーザーと紐づけ（募金者）
    donor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # 金額（Decimal型）
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(50)])

    # 応援メッセージ（任意）
    message = models.TextField(blank=True, null=True)

    # 日付（募金日時）
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.donor.username} - ¥{self.amount}"

    class Meta:
        # 日付で並び替え（最新の募金が最初に表示される）
        ordering = ['-date']



# class Post(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)    
#     title = models.CharField(max_length=200)
#     comment = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     caption = models.TextField(verbose_name='場所', blank=True)
#     latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)  # 緯度
#     longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)  # 経度
#     fundraising = models.ForeignKey(Fundraising, null=True, blank=True, on_delete=models.SET_NULL)

#     def __str__(self):
#         return f"{self.user.username} - {self.title}"

#     def like_count(self):
#         return self.likes.count()  # 投稿に対する「いいね」の数を返す

#     def liked_by_user(self, user):
#         """投稿にユーザーがいいねをしているか確認する"""
#         return self.likes.filter(user=user).exists()


class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)    
    title = models.CharField(max_length=200)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    caption = models.TextField(verbose_name='場所', blank=True)
    fundraising = models.BooleanField(default=False)
    latitude = models.DecimalField(max_digits=15, decimal_places=11, null=True, blank=True)  # 緯度
    longitude = models.DecimalField(max_digits=15, decimal_places=11, null=True, blank=True)  # 経度
 
    def __str__(self):
        return f"{self.user.username} - {self.title}"
 
    def like_count(self):
        return self.likes.count()  # 投稿に対する「いいね」の数を返す
 
    def liked_by_user(self, user):
        """投稿にユーザーがいいねをしているか確認する"""
        return self.likes.filter(user=user).exists()

class PostImage(models.Model):
    """投稿に関連する画像を保存するモデル"""
    post = models.ForeignKey(Post, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos')

    def __str__(self):
        return f"Image for {self.post.title}"

class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)  # コメント投稿者
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)  # コメントが付けられた投稿
    text = models.TextField()  # コメント内容
    created_at = models.DateTimeField(auto_now_add=True)  # コメント日時

    def __str__(self):
        return f"{self.user.username}: {self.text[:20]}"  # コメントの最初の20文字


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')  # いいねが付けられた投稿
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)  # いいねをしたユーザー

    class Meta:
        unique_together = ('post', 'user')  # 同じユーザーが同じ投稿に「いいね」を複数回できないように

    def __str__(self):
        return f"{self.user.username} liked {self.post.id}"  # どのユーザーがどの投稿に「いいね」したか
    
class Plan(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    posts = models.ManyToManyField(Post, related_name='plans')  # プランに関連する投稿
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_oldest_post(self):
        """プランの中で最も古い投稿を取得"""
        return self.posts.order_by('created_at').first()  # created_atが一番古い投稿を取得

