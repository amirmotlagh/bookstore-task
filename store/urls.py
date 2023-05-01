from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from store.views import BookView, BookUpdateView

app_name = 'store'

urlpatterns = [
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('books', BookView.as_view(), name='book-view'),
    path('book/', BookUpdateView.as_view({
        'get': 'read',
        'post': 'create',
        'put': 'update',
    }), name='book-update-view'),
    path('book/<str:title>/delete/', BookUpdateView.as_view({
        'delete': 'delete'
    }), name='delete-book')
]
