"""
URL mappings for the recipe app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from recipe import views


router = DefaultRouter()
router.register('recipes', views.RecipeViewSet)
router.register('tags', views.TagViewSet)
router.register('ingredients', views.IngredientViewSet)

# DefaultRouter will create the endpoints recipes/ and recipes/<id>/
# as long as your RecipeViewSet includes the appropriate methods.

# recipes/ for listing all recipes or creating a new recipe
# (corresponding to the .list() and .create() methods in RecipeViewSet)

# recipes/<id>/ for retrieving, updating, or deleting a specific
# recipe (corresponding to the .retrieve(), .update(), .partial_update(),
# and .destroy() methods in RecipeViewSet)

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls)),
]

# the line path('', include(router.urls)) in your urlpatterns list is used to
# include the URLs (recipes/ and recipes/<id>/) that are automatically generated
# by the DefaultRouter instance. They are both linked to the views.RecipeViewSet