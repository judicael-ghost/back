"""
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.urls import path
from django.urls.conf import include
from django.contrib import admin
from rest_framework import routers
from kairos.urls import router as client_router
from utilisateur.urls import router as utilisateur_router
from django.conf import settings
from django.conf.urls.static import static


router = routers.DefaultRouter()

router.registry.extend(client_router.registry)
router.registry.extend(utilisateur_router.registry)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('dj_rest_auth.urls')),
    path('', include('kairos.urlsIngredient')),
    path('', include(router.urls)),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)