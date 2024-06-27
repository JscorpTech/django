from . import common, local, production

urlpatterns = local.urlpatterns + production.urlpatterns + common.urlpatterns
