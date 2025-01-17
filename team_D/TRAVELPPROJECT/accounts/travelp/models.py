from django.db import models
 
 
class CustomUser(models.Model):
    user_id = models.CharField(primary_key=True, max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    display_name = models.CharField(max_length=255)
    nickname = models.CharField(max_length=255)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
 
    def __str__(self):
        return self.display_name
 
    class Meta:
        verbose_name = "カスタムユーザー"
        verbose_name_plural = "カスタムユーザー"
 
 
class MemberUser(models.Model):
    custom_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="member_profile")
    plan_id = models.CharField(max_length=255)  # Plan ID (ForeignKey-like placeholder)
    interests = models.TextField()
 
    def __str__(self):
        return f"MemberUser: {self.custom_user.display_name}"
 
    class Meta:
        verbose_name = "会員ユーザー"
        verbose_name_plural = "会員ユーザー"
 
 
class CityOffice(models.Model):
    city_office_id = models.CharField(primary_key=True, max_length=255)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    is_sister_city = models.BooleanField(default=False)
    sister_city_name = models.CharField(max_length=255, null=True, blank=True)
 
    def __str__(self):
        return self.name
 
    class Meta:
        verbose_name = "市役所"
        verbose_name_plural = "市役所"
 
 
class Post(models.Model):
    post_id = models.CharField(primary_key=True, max_length=255)
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='post_images/')
    content = models.TextField()
    member_user = models.ForeignKey(MemberUser, on_delete=models.CASCADE, related_name="posts")
 
    def __str__(self):
        return self.title
 
    class Meta:
        verbose_name = "投稿"
        verbose_name_plural = "投稿"
 
 
class MyPlan(models.Model):
    plan_id = models.CharField(primary_key=True, max_length=255)
    plan_name = models.CharField(max_length=255)
    member_user = models.ForeignKey(MemberUser, on_delete=models.CASCADE, related_name="my_plans")
 
    def __str__(self):
        return self.plan_name
 
    class Meta:
        verbose_name = "マイプラン"
        verbose_name_plural = "マイプラン"
 
 
class Like(models.Model):
    like_id = models.CharField(primary_key=True, max_length=255)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    member_user = models.ForeignKey(MemberUser, on_delete=models.CASCADE, related_name="likes")
    is_deleted = models.BooleanField(default=False)
 
    def __str__(self):
        return f"Like by {self.member_user.custom_user.display_name} on {self.post.title}"
 
    class Meta:
        verbose_name = "いいね"
        verbose_name_plural = "いいね"
 
 
class Comment(models.Model):
    comment_id = models.CharField(primary_key=True, max_length=255)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    member_user = models.ForeignKey(MemberUser, on_delete=models.CASCADE, related_name="comments")
    reply_to = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name="replies")
    content = models.TextField()
 
    def __str__(self):
        return f"Comment by {self.member_user.custom_user.display_name} on {self.post.title}"
 
    class Meta:
        verbose_name = "コメント"
        verbose_name_plural = "コメント"
 
 
class Donation(models.Model):
    donation_id = models.CharField(primary_key=True, max_length=255)
    name = models.CharField(max_length=255)
    description = models.TextField()
    goal_amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
 
    def __str__(self):
        return self.name
 
    class Meta:
        verbose_name = "募金"
        verbose_name_plural = "募金"
 
 
class DonationHistory(models.Model):
    history_id = models.CharField(primary_key=True, max_length=255)
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE, related_name="histories")
    member_user = models.ForeignKey(MemberUser, on_delete=models.CASCADE, related_name="donation_histories")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    donation_date = models.DateField(auto_now_add=True)
 
    def __str__(self):
        return f"DonationHistory of {self.member_user.custom_user.display_name} to {self.donation.name}"
 
    class Meta:
        verbose_name = "募金履歴"
        verbose_name_plural = "募金履歴"