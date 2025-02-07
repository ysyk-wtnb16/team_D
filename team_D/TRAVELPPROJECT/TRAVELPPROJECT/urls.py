from django.contrib import admin
from django.urls import path, include
# settingsを追加
from django.conf import settings
# staticを追加
from django.conf.urls.static import static
 
urlpatterns = [
    path('admin/', admin.site.urls),
 
    path('',include('travelp.urls')),
 
    # accounts.urlsへのURLパターン
    path('', include('accounts.urls')),
 
]
 
 
# urlpatternsにmediaフォルダーのURLパターンを追加
urlpatterns += static(
   # MEDIA_URL = '/media/'
  settings.MEDIA_URL,
  # MEDIA_ROOTにリダイレクト
  document_root=settings.MEDIA_ROOT
  )
 