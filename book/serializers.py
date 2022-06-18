from rest_framework import serializers
from .models import ReadPoint, Category

from rest_framework import serializers
from book.models import Book, ReadPoint


class ReadPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadPoint
        fields = '__all__'


class ApiBook(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class ApiReadPoint(serializers.ModelSerializer):
    class Meta:
        model = ReadPoint
        fields = '__all__'


class ApiCate(serializers.ModelSerializer):
    books = ApiBook(many=True)

    class Meta:
        model = Category
        fields = ('name_category', 'id', 'books')


class Category_api(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name_category','id')
