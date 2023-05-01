from django.urls import reverse
from rest_framework.permissions import AllowAny
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from store.models import CustomUser
from store.views import BookView


class TestBookView(APITestCase):
    fixtures = ['book/base.yaml', 'user/base.yaml']

    def setUp(self):
        super().setUp()
        user = CustomUser.objects.first()
        token = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token.access_token}')

    def _get_permission_classes(self):
        return [AllowAny]

    def _make_url(self, kwargs=None):
        return reverse('store:book-view', kwargs=kwargs)

    def _get_view_class(self):
        return BookView

    def test_permission_classes(self):
        xor = set(self._get_permission_classes()) ^ set(self._get_view_class().permission_classes)
        if not xor:
            return
        self.fail('Expected permission classes: {expected} But found: {actual}'.format(
                    expected=self._get_permission_classes(),
                    actual=self._get_view_class().permission_classes))

    def test_without_any_params(self):
        result = self.client.get(self._make_url(), )

        expected_response = [
            {
                'id': 1,
                'title': 'novel',
                'auther': {
                    'id': 1,
                    'author_pseudonym': 'auther1',
                    'first_name': 'amir',
                    'last_name': 'motlagh',
                },
                'description': 'this is a novel by auther1',
                'price': 10000
            },
            {
                'id': 2,
                'title': 'poem',
                'auther': {
                    'id': 1,
                    'author_pseudonym': 'auther1',
                    'first_name': 'amir',
                    'last_name': 'motlagh',
                },
                'description': 'this is a poem by auther1',
                'price': 20000
            },
            {
                'id': 3,
                'title': 'documentary',
                'auther': {
                    'id': 2,
                    'author_pseudonym': 'auther2',
                    'first_name': 'eli',
                    'last_name': 'soufi',
                },
                'description': 'this is a documentary by auther2',
                'price': 30000
            },
        ]

        self.assertEqual(expected_response, result.data)

    def test_with_query_param(self):
        result = self.client.get(self._make_url(), data={'auther': 'auther2'})

        expected_response = [
            {
                'id': 3,
                'title': 'documentary',
                'auther': {
                    'id': 2,
                    'author_pseudonym': 'auther2',
                    'first_name': 'eli',
                    'last_name': 'soufi',
                },
                'description': 'this is a documentary by auther2',
                'price': 30000
            },
        ]

        self.assertEqual(expected_response, result.data)
