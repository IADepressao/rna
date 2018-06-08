from django.conf.urls import url, include

from . import views
from django.contrib.auth import views as auth_views
from depressao.settings import DEBUG

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^perguntas/$', views.perguntas, name='perguntas'),
    url(r'^resultados/$', views.resultados, name='resultados'),
    url(r'^configuracoes/$', views.configuracoes, name='configuracoes'),
]

if DEBUG:
    import debug_toolbar
    urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls)),]
