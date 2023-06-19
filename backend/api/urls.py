from django.urls import include, path
from rest_framework import routers

from api.views import IngredientViewSet, RecipeViewSet, TagViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register('ingredients', IngredientViewSet, basename='ingredient')
router.register('tags', TagViewSet, basename='tag')
router.register('recipes', RecipeViewSet, basename='recipe')

urlpatterns = [
    path(r'', include('djoser.urls')),
    path(r'auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]
