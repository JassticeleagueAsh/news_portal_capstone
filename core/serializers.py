from rest_framework import serializers
from .models import User, Publisher, Article, Newsletter


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['id', 'name', 'description']


class NewsletterSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Newsletter
        fields = ['id', 'title', 'description', 'created_at', 'author', 'articles']


class ArticleSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    publisher = PublisherSerializer(read_only=True)

    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'author', 'publisher', 'created_at', 'approved']