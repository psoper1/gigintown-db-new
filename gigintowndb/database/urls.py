from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import *

urlpatterns = [
    path('user/create/', UserCreate.as_view(), name="create_user"),
    path('token/obtain/', ObtainTokenPairWithColorView.as_view(), name='token_create'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('hello/', HelloWorldView.as_view(), name='hello_world'),
    path('events/search/', EventSearchView.as_view(), name='event-search'),
    path('events/', EventCreateView.as_view(), name='event-create'),
    path('save-event/<int:event_id>/', save_event, name='save_event'),
    path('user/details/', UserDetailsView.as_view(), name='user-details'),
    path('get-saved-events/', get_saved_events, name='get_saved_events'),
]