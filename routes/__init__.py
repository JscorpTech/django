from . import local, production, common

urlpatterns = local.urlpatterns + production.urlpatterns + common.urlpatterns
