from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from .models import Article, Newsletter, Publisher, User


class NewsPortalTests(TestCase):
    """
    Automated tests for the news portal application.

    These tests cover:
    - role-based access
    - article visibility
    - journalist article creation
    - editor approval
    - newsletter creation
    - API endpoints
    - API authentication
    - subscribed article filtering
    """

    def setUp(self):
        """
        Create test users, publisher, and sample articles used across tests.
        """
        self.client_api = APIClient()

        self.reader = User.objects.create_user(
            username="reader_test",
            password="Testpass123",
            email="reader@example.com",
            role="reader",
        )

        self.editor = User.objects.create_user(
            username="editor_test",
            password="Testpass123",
            email="editor@example.com",
            role="editor",
        )

        self.journalist = User.objects.create_user(
            username="journalist_test",
            password="Testpass123",
            email="journalist@example.com",
            role="journalist",
        )

        self.other_journalist = User.objects.create_user(
            username="other_journalist",
            password="Testpass123",
            email="otherjournalist@example.com",
            role="journalist",
        )

        self.publisher = Publisher.objects.create(
            name="Daily Times",
            description="Test publisher",
        )

        self.other_publisher = Publisher.objects.create(
            name="Global News",
            description="Another test publisher",
        )

        self.publisher.editors.add(self.editor)
        self.publisher.journalists.add(self.journalist)

        self.approved_article = Article.objects.create(
            title="Approved Article",
            content="This article is approved.",
            author=self.journalist,
            publisher=self.publisher,
            approved=True,
        )

        self.unapproved_article = Article.objects.create(
            title="Draft Article",
            content="This article is not approved yet.",
            author=self.journalist,
            publisher=self.publisher,
            approved=False,
        )

        self.other_approved_article = Article.objects.create(
            title="Other Approved Article",
            content="Approved from another source.",
            author=self.other_journalist,
            publisher=self.other_publisher,
            approved=True,
        )

        self.reader_token = Token.objects.create(user=self.reader)
        self.editor_token = Token.objects.create(user=self.editor)
        self.journalist_token = Token.objects.create(user=self.journalist)

    def test_reader_can_only_view_approved_articles(self):
        """
        Readers should only see approved articles in the article list.
        """
        self.client.force_login(self.reader)
        response = self.client.get(reverse("article_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Approved Article")
        self.assertNotContains(response, "Draft Article")

    def test_reader_cannot_view_unapproved_article_detail(self):
        """
        Readers should not be able to open the detail page for unapproved articles.
        """
        self.client.force_login(self.reader)
        response = self.client.get(
            reverse("article_detail", args=[self.unapproved_article.id])
        )

        self.assertEqual(response.status_code, 404)

    def test_journalist_can_create_article(self):
        """
        Journalists should be able to create articles.
        New articles must be unapproved by default.
        """
        self.client.force_login(self.journalist)

        response = self.client.post(
            reverse("create_article"),
            {
                "title": "New Journalist Article",
                "content": "Created by journalist.",
                "publisher": self.publisher.id,
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Article.objects.filter(title="New Journalist Article").exists()
        )

        article = Article.objects.get(title="New Journalist Article")
        self.assertEqual(article.author, self.journalist)
        self.assertFalse(article.approved)

    def test_reader_cannot_create_article(self):
        """
        Readers should not be able to create articles.
        """
        self.client.force_login(self.reader)

        response = self.client.post(
            reverse("create_article"),
            {
                "title": "Reader Article",
                "content": "This should not be created.",
                "publisher": self.publisher.id,
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Article.objects.filter(title="Reader Article").exists())

    @patch("core.views.requests.post")
    @patch("core.views.send_mail")
    def test_editor_can_approve_article(self, mock_send_mail, mock_requests_post):
        """
        Editors should be able to approve articles.

        Approval should:
        - set approved to True
        - trigger email logic
        - trigger external POST request logic
        """
        self.reader.subscribed_publishers.add(self.publisher)

        self.client.force_login(self.editor)
        response = self.client.get(
            reverse("approve_article", args=[self.unapproved_article.id])
        )

        self.assertEqual(response.status_code, 302)

        self.unapproved_article.refresh_from_db()
        self.assertTrue(self.unapproved_article.approved)

        mock_send_mail.assert_called_once()
        mock_requests_post.assert_called_once()

    def test_journalist_cannot_access_editor_review_page(self):
        """
        Journalists should not be able to access the editor review page.
        """
        self.client.force_login(self.journalist)
        response = self.client.get(reverse("editor_article_list"))

        self.assertEqual(response.status_code, 302)

    def test_journalist_can_create_newsletter(self):
        """
        Journalists should be able to create newsletters linked to articles.
        """
        self.client.force_login(self.journalist)

        response = self.client.post(
            reverse("create_newsletter"),
            {
                "title": "Weekly Roundup",
                "description": "Top stories of the week.",
                "articles": [self.approved_article.id],
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Newsletter.objects.filter(title="Weekly Roundup").exists())

        newsletter = Newsletter.objects.get(title="Weekly Roundup")
        self.assertEqual(newsletter.author, self.journalist)
        self.assertIn(self.approved_article, newsletter.articles.all())

    def test_dashboard_redirects_by_role(self):
        """
        Users should be redirected to the correct dashboard/page based on role.
        """
        self.client.force_login(self.reader)
        response = self.client.get(reverse("dashboard"))
        self.assertRedirects(response, reverse("article_list"))

        self.client.force_login(self.journalist)
        response = self.client.get(reverse("dashboard"))
        self.assertRedirects(response, reverse("journalist_dashboard"))

        self.client.force_login(self.editor)
        response = self.client.get(reverse("dashboard"))
        self.assertRedirects(response, reverse("editor_article_list"))

    def test_api_returns_only_approved_articles(self):
        """
        The public article list API should return approved articles only.
        """
        response = self.client_api.get("/api/articles/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Approved Article")
        self.assertContains(response, "Other Approved Article")
        self.assertNotContains(response, "Draft Article")

    def test_api_subscribed_requires_authentication(self):
        """
        The subscribed articles API should require token authentication.
        """
        response = self.client_api.get("/api/articles/subscribed/")

        self.assertEqual(response.status_code, 401)

    def test_api_subscribed_returns_only_subscribed_content(self):
        """
        The subscribed articles API should return only articles from the
        reader's subscribed publishers and journalists.
        """
        self.reader.subscribed_publishers.add(self.publisher)
        self.client_api.credentials(
            HTTP_AUTHORIZATION=f"Token {self.reader_token.key}"
        )

        response = self.client_api.get("/api/articles/subscribed/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Approved Article")
        self.assertNotContains(response, "Other Approved Article")
        self.assertNotContains(response, "Draft Article")

    def test_api_journalist_can_create_article(self):
        """
        Journalists should be able to create articles through the API.
        """
        self.client_api.credentials(
            HTTP_AUTHORIZATION=f"Token {self.journalist_token.key}"
        )

        response = self.client_api.post(
            "/api/articles/create/",
            {
                "title": "API Journalist Article",
                "content": "Created through API.",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(Article.objects.filter(title="API Journalist Article").exists())

        article = Article.objects.get(title="API Journalist Article")
        self.assertEqual(article.author, self.journalist)

    def test_api_reader_cannot_create_article(self):
        """
        Readers should not be able to create articles through the API.
        """
        self.client_api.credentials(
            HTTP_AUTHORIZATION=f"Token {self.reader_token.key}"
        )

        response = self.client_api.post(
            "/api/articles/create/",
            {
                "title": "Reader API Article",
                "content": "This should not be allowed.",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 403)
        self.assertFalse(Article.objects.filter(title="Reader API Article").exists())