from rest_framework import generics, permissions
from rest_framework.authentication import TokenAuthentication

from .models import Article
from .permissions import IsEditorOrJournalist, IsJournalist
from .serializers import ArticleSerializer


class ArticleListAPIView(generics.ListAPIView):
    """
    Public API endpoint that returns all approved articles.

    No authentication is required for this endpoint.
    """

    # Only return approved articles and optimise query with select_related
    queryset = Article.objects.filter(approved=True).select_related("author", "publisher")
    serializer_class = ArticleSerializer
    permission_classes = [permissions.AllowAny]


class SubscribedArticleListAPIView(generics.ListAPIView):
    """
    Authenticated API endpoint that returns approved articles from:

    - publishers the user is subscribed to
    - journalists the user is subscribed to

    A valid token is required to access this endpoint.
    """

    serializer_class = ArticleSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Build the queryset for subscribed content.
        """
        user = self.request.user  # Get the currently authenticated user

        # Get articles from publishers the user follows
        publisher_articles = Article.objects.filter(
            approved=True,
            publisher__in=user.subscribed_publishers.all(),
        )

        # Get articles from journalists the user follows
        journalist_articles = Article.objects.filter(
            approved=True,
            author__in=user.subscribed_journalists.all(),
        )

        # Combine both querysets into one result
        return publisher_articles | journalist_articles


class ArticleDetailAPIView(generics.RetrieveAPIView):
    """
    Public API endpoint that returns a single approved article.
    """

    # Only allow retrieval of approved articles
    queryset = Article.objects.filter(approved=True).select_related("author", "publisher")
    serializer_class = ArticleSerializer
    permission_classes = [permissions.AllowAny]


class ArticleCreateAPIView(generics.CreateAPIView):
    """
    Protected API endpoint that allows journalists to create articles.

    A valid token is required.
    """

    serializer_class = ArticleSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsJournalist]

    def perform_create(self, serializer):
        """
        Save the current authenticated journalist as the article author.
        """
        # Automatically assign the logged-in user as the author
        serializer.save(author=self.request.user)


class ArticleUpdateAPIView(generics.UpdateAPIView):
    """
    Protected API endpoint that allows editors and journalists to update articles.
    """

    # Allow updating any article (permissions control access)
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsEditorOrJournalist]


class ArticleDeleteAPIView(generics.DestroyAPIView):
    """
    Protected API endpoint that allows editors and journalists to delete articles.
    """

    # Allow deletion of any article (permissions control access)
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsEditorOrJournalist]