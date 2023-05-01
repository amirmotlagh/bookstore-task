from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.exceptions import NotFound, NotAcceptable
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from store.models import Book
from store.serializers import BookSerializer


class BookView(APIView):
    serializer_class = BookSerializer

    def get(self, request):
        auther_param = request.GET.get('auther', None)
        title_param = request.GET.get('title', None)
        price_param = request.GET.get('price', None)

        books = Book.objects.all()

        if auther_param is not None:
            books = books.filter(auther__author_pseudonym__icontains=auther_param)
        if title_param is not None:
            books = books.filter(title__icontains=title_param)
        if price_param is not None:
            books = books.filter(price=price_param)

        return Response(self.serializer_class(books, many=True).data)


class BookUpdateView(ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = BookSerializer

    def read(self, request):
        auther = request.user
        books = Book.objects.filter(auther=auther)
        return Response(self.serializer_class(books, many=True).data)

    def create(self, request):
        auther = request.user
        cover_image = request.data.get('cover_image')
        payload_data = request.data

        title = payload_data.get('title', None)
        if title is None:
            raise NotAcceptable(code='no_title', detail='title is mondatory for registering a '
                                                        'new book')
        payload_data.update({'cover_image': cover_image, 'auther': auther})

        serializer = self.serializer_class(data=payload_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def update(self, request):
        auther = request.user
        cover_image = request.data.get('cover_image', None)
        payload_data = request.data
        if cover_image is not None:
            payload_data.update({'cover_image': cover_image})
        title = payload_data.get('title', None)
        instance = Book.objects.filter(auther=auther, title=title)
        if instance is None:
            raise NotFound(code='no_book', detail='The Requested book to update is not Found')

        payload_data.update({'auther': auther})

        serializer = self.serializer_class(instance=instance, data=payload_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request, title):
        auther = request.user
        books = Book.objects.filter(auther=auther, title=title)

        if books is None:
            raise NotFound(code='book_not_found',
                           detail='The Requested book to delete is not Found')

        books.delete()

        return Response(status=status.HTTP_200_OK)
