from django.conf.urls import url

from . import views


# name spacing so url ___ ___ in the html templates knows which 'index' to call for example
# (ie. allows for me to use "url 'login:index' ___" in templates)
app_name = 'login'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^new_account$', views.new_account, name='new_account'),
    url(r'^created_account$', views.created_account, name='created_account'),
    url(r'^verify$', views.verify, name='verify'),
    url(r'^home$', views.home, name='home'),
    url(r'^researcher$', views.researcher, name='researcher'),
    url(ur'^edit_study/(?P<studyName>.*)', views.edit_study, name='edit_study'),
    url(r'^participant$', views.participant, name='participant'),
    url(r'^make_study$', views.make_study, name='make_study'),
    url(r'^study_confirm$', views.study_confirm, name='study_confirm'),
    url(r'^logout$', views.logout_, name="logout")

]
