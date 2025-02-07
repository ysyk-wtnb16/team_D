from django.db import models
# AbstractUserクラスをインポート
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    '''
    Userモデルを継承したカスタムユーザーモデル
    '''
    pass
    nickname = models.CharField(max_length=150, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    profile_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.username