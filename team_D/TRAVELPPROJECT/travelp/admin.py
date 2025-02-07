from django.contrib import admin
from .models import Post, Comment, Like
 
# admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)

class PostAdmin(admin.ModelAdmin):
  # レコード一覧にidとtitleを表示
  list_display = ('id', 'title')
  # 表示するカラムにリンクを設定
  list_display_links = ('id', 'title')

    # Django管理サイトにPhotoPost、PhotoPostAdminを登録する
admin.site.register(Post, PostAdmin)