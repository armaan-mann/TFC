from django.urls import path, re_path
from studios.api.views import StudiosByProximityAPIView, ViewStudioAPIView, FilterStudioAPIView
from studios.api.views import SearchStudioAPIView, SearchAmenityAPIView, SearchClassAPIView, SearchCoachAPIView

app_name = 'studios'
urlpatterns = [
    path('search/coach/', SearchCoachAPIView.as_view(), name='search_studios'),
    path('search/class_name/', SearchClassAPIView.as_view(), name='search_studios'),
    path('search/studio_name/', SearchStudioAPIView.as_view(), name='search_studios'),
    path('search/amenity/', SearchAmenityAPIView.as_view(), name='search_studios'),
    path('<int:studio_id>/', ViewStudioAPIView.as_view(), name='list_studios'),
    path('filter/<slug:studio_name>/<slug:types>/<slug:class_names>/<slug:coaches>/', FilterStudioAPIView.as_view(), name='filter_studios'),
    #re_path(r'^(?P<latitude>[0-9.-]+).+?([0-9.-]+)/(?P<longitude>[0-9.-]+).+?([0-9.-]+)/list$', StudiosByProximityAPIView.as_view(), name='list_studios')
    re_path(r'^(?P<latitude>[0-9.-]+).+?([0-9.-]+)/(?P<longitude>[0-9.-]+).+?([0-9.-]+)/(?P<ids>.+)/list$', StudiosByProximityAPIView.as_view(), name='list_studios')
]