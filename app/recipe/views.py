"""
Views for the recipe APIs
"""

from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)

from rest_framework import (
    viewsets,
    mixins,
    status,
)

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import (
    Recipe,
    Tag,
    Ingredient,
)

from recipe import serializers

@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'tags',
                OpenApiTypes.STR,  # the type is str
                description='Comma separated list of tag IDs to filter',
            ),
            OpenApiParameter(
                'ingredients',
                OpenApiTypes.STR,
                description='Comma separated list of ingredient IDs to filter',
            ),
        ]
    )
)

class RecipeViewSet(viewsets.ModelViewSet):   # viewsets.ModelViewSet can handel all the CRUD
    """View for manage recipe APIs."""
    serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def _params_to_ints(self, qs):
        """Convert a list of strings to integers."""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):  # override and will be called auto in GET request
        """Retrieve recipes for authenticated user."""  # filter performed here
        tags = self.request.query_params.get('tags')
        ingredients = self.request.query_params.get('ingredients')
        queryset = self.queryset
        if tags:   # return all recipe if no tags
            tag_ids = self._params_to_ints(tags)  # convert "1,2,3" to [1,2,3]
            queryset = queryset.filter(tags__id__in=tag_ids)  # filter tags by id field in tag_ids
        if ingredients:
            ingredient_ids = self._params_to_ints(ingredients)
            queryset = queryset.filter(ingredients__id__in=ingredient_ids)

        return queryset.filter(
            user=self.request.user
        ).order_by('-id').distinct()  # distinct() prevent duplicates

    def get_serializer_class(self):  # override get_serializer_class and will be called auto
        """Return the serializer class for request."""
        if self.action == 'list':   # url path: recipes/
            return serializers.RecipeSerializer

        elif self.action == 'upload_image':    # custome action
            return serializers.RecipeImageSerializer

        return self.serializer_class

    def perform_create(self, serializer): # override and will be called auto in post
        """Create a new recipe."""         # the serializer is validated
        serializer.save(user=self.request.user)

    # serializer is the outer layer of a model and i can directly save the
    # model or indirectly save the model via the serializer

# 1. The client sends a POST request to the endpoint.

# 2. Django processes the request and determines the appropriate view to handle it,
# based on the URL of the request. In your case, this is the RecipeViewSet.

# 3. Within the RecipeViewSet, the create method is called to handle the POST request.
# This is a built-in method of ModelViewSet.

# 4. The create method calls get_serializer to get an instance of the appropriate serializer.
# The choice of serializer depends on your get_serializer_class method.

# 5. The serializer's is_valid method is called to validate the request data.

# 6. If the data is valid, perform_create is called, passing in the validated serializer.

# 7. The perform_create method calls serializer.save(), passing in any additional arguments if necessary.

# 8. The save method then calls either create or update on the serializer, depending on whether
# a new instance is being created or an existing one is being updated. Since we're handling a POST request,
# which is used to create new instances, create is called. This method creates a new instance of the model
# in the database.

    @action(methods=['POST'], detail=True, url_path='upload-image')   # add custome action
    def upload_image(self, request, pk=None):
        """Upload an image to recipe."""
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)  # the default update() in serializer will be called
        # get_serializer method is a utility method provided by the viewset that retrieves
        # an instance of the serializer based on the serializer class returned by get_serializer_class
        if serializer.is_valid():
            serializer.save()   # perform_create wont be call in this case
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # When you define a custom action using the @action decorator in your viewset,
    # the corresponding URL for that action is automatically generated and included in the router's URLs.


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'assigned_only',
                OpenApiTypes.INT, enum=[0, 1],
                description='Filter by items assigned to recipes.',
            ),
        ]
    )
)

class BaseRecipeAttrViewSet(mixins.DestroyModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    """Base viewset for recipe attributes."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # this make the returned data from GET that only belongs to the user
        """Filter queryset to authenticated user."""
        assigned_only = bool(
            int(self.request.query_params.get('assigned_only', 0))  # 0 is default value
        )
        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(recipe__isnull=False)   # check the recipe field in tags or ingredents

        return queryset.filter(
            user=self.request.user
        ).order_by('-name').distinct()

        # the returned queryset will be passed to serilizer before passing to client as Response object


class TagViewSet(BaseRecipeAttrViewSet):
    """Manage tags in the database."""
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()



class IngredientViewSet(BaseRecipeAttrViewSet):
    """Manage ingredients in the database."""
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()
