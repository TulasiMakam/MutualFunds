from django.conf.urls import url
from ISINapp import views
# SET THE NAMESPACE!
app_name = 'ISINapp'
# Be careful setting the name to just /login use userlogin instead!
urlpatterns=[
    url(r'^mutual-fund/$', views.mutualfund, name='mutualfund'),
    url(r'^addisin/$', views.addisin, name='addisin'),
]