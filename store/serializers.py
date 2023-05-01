from rest_framework import serializers
from store.models import CustomUser

from store.models import Book


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'author_pseudonym', 'first_name', 'last_name')


class BookSerializer(serializers.ModelSerializer):
    auther = UserSerializer()

    class Meta:
        model = Book
        fields = ['id', 'title', 'auther', 'description', 'price']

