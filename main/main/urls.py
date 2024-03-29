from notice import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('<int:major>/notice', views.NoticeList.as_view()),
    path('notice/', include('notice.urls')),
    path('schedule',views.scheduleList.as_view()),
    path('menu',views.menuList.as_view())
]
