from django.conf.urls import url

from . import views


# name spacing so url ___ ___ in the html templates knows which 'index' to call for example
# (ie. allows for me to use "url 'login:index' ___" in templates)
app_name = 'user_profile'

urlpatterns = [
    url(r'^$', views.index, name='index'),
]