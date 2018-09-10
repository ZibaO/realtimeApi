
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import  CreateViewGaussian
from .views import CreateViewMultinomial
from .views import CreateViewBernoulli
#from .views import DetailsView

urlpatterns = {
    url(r'^requestsGaussian/$', CreateViewGaussian.as_view(), name="create"),
    url(r'^requestsMultinomial/$', CreateViewMultinomial.as_view(), name="create"),
    url(r'^requestsBernoulli/$', CreateViewBernoulli.as_view(), name="create"),



    #url(r'^requests/(?P<pk>[0-9]+)/$',DetailsView.as_view(), name="details"),
}

urlpatterns = format_suffix_patterns(urlpatterns)