#（追加した）
from django.contrib.auth.models import AbstractUser


from django.db import models


#（追加した）
class CustomUser(AbstractUser):

    # 必要に応じて追加のフィールドを定義します

    nickname = models.CharField(max_length=50, blank=True, null=True) 
