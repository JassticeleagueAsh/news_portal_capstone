"""
Views for the News Portal application.

Handles user authentication, dashboards, article management,
newsletter management, and subscription features.
"""
import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    ArticleForm,
    LoginForm,
    NewsletterForm,
    PublisherForm,
    RegisterForm,
)
from .models import Article, Newsletter, Publisher, User


def home_view(request):
    """
    Show the landing page for users who are not logged in.

    If a user is already authenticated, redirect them to the dashboard
    so the system can route them according to their role.
    """
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect("/admin/")
        return redirect("dashboard")

    return render(request, "index.html")


def register_view(request):
    """
    Register a new user and log them in immediately after successful signup.
    """
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("dashboard")
    else:
        form = RegisterForm()

    return render(request, "registration/register.html", {"form": form})


def login_view(request):
    """
    Log in a user with valid credentials.
    """
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect("dashboard")
    else:
        form = LoginForm()

    return render(request, "registration/login.html", {"form": form})


@login_required
def logout_view(request):
    """
    Log out the current user and redirect to the login page.
    """
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("login")


@login_required
def dashboard_view(request):
    """
    Redirect users to the correct page based on their role.

    - editor -> editor review page
    - journalist -> journalist dashboard
    - reader -> article list page
    - publisher -> newsletter list page
    """
    if request.user.is_superuser:
        return redirect("/admin/")

    if request.user.role == "editor":
        return redirect("editor_article_list")

    if request.user.role == "journalist":
        return redirect("journalist_dashboard")

    if request.user.role == "reader":
        return redirect("article_list")

    if request.user.role == "publisher":
        return redirect("newsletter_list")

    return redirect("home")


@login_required
def journalist_dashboard_view(request):
    """
    Show the journalist dashboard with the journalist's own articles
    and newsletters.
    """
    if request.user.role != "journalist":
        messages.error(request, "Only journalists can access that page.")
        return redirect("dashboard")

    articles = Article.objects.filter(author=request.user).select_related(
        "author",
        "publisher",
    )
    newsletters = Newsletter.objects.filter(author=request.user).prefetch_related(
        "articles"
    )

    context = {
        "articles": articles,
        "newsletters": newsletters,
    }
    return render(request, "core/journalist_dashboard.html", context)


@login_required
def article_list_view(request):
    """
    Show articles and newsletters for the current user.

    - Readers can see approved articles and all newsletters.
    - Publishers can also see approved articles and newsletters.
    - Editors and journalists can see all articles and all newsletters.
    - Readers can subscribe to publishers and journalists from this page.
    """
    if request.user.role in ["reader", "publisher"]:
        articles = Article.objects.filter(approved=True).select_related(
            "author",
            "publisher",
        )
    else:
        articles = Article.objects.select_related("author", "publisher").all()

    newsletters = Newsletter.objects.select_related("author").prefetch_related(
        "articles"
    )
    publishers = Publisher.objects.all()
    journalists = User.objects.filter(role="journalist")

    subscribed_publisher_ids = []
    subscribed_journalist_ids = []

    if request.user.role == "reader":
        subscribed_publisher_ids = list(
            request.user.subscribed_publishers.values_list("id", flat=True)
        )
        subscribed_journalist_ids = list(
            request.user.subscribed_journalists.values_list("id", flat=True)
        )

    context = {
        "articles": articles,
        "newsletters": newsletters,
        "publishers": publishers,
        "journalists": journalists,
        "subscribed_publisher_ids": subscribed_publisher_ids,
        "subscribed_journalist_ids": subscribed_journalist_ids,
    }
    return render(request, "core/article_list.html", context)


@login_required
def article_detail_view(request, article_id):
    """
    Show the details of a single article.

    Readers and publishers can only open approved articles.
    Editors and journalists can open any article.
    """
    if request.user.role in ["reader", "publisher"]:
        article = get_object_or_404(
            Article.objects.select_related("author", "publisher"),
            id=article_id,
            approved=True,
        )
    else:
        article = get_object_or_404(
            Article.objects.select_related("author", "publisher"),
            id=article_id,
        )

    return render(request, "core/article_detail.html", {"article": article})


@login_required
def newsletter_list_view(request):
    """
    Show the newsletter feed.

    This allows readers and publishers to access newsletters created by journalists.
    """
    newsletters = Newsletter.objects.select_related("author").prefetch_related(
        "articles"
    )

    return render(
        request,
        "core/newsletter_list.html",
        {"newsletters": newsletters},
    )


@login_required
def newsletter_detail_view(request, newsletter_id):
    """
    Show the details of a single newsletter and its linked articles.
    """
    newsletter = get_object_or_404(
        Newsletter.objects.select_related("author").prefetch_related("articles"),
        id=newsletter_id,
    )

    return render(
        request,
        "core/newsletter_detail.html",
        {"newsletter": newsletter},
    )


@login_required
def editor_article_list_view(request):
    """
    Show all articles and newsletters for editors.

    Editors can review, approve, update, and delete content here.
    """
    if request.user.role != "editor":
        messages.error(request, "Only editors can access that page.")
        return redirect("dashboard")

    articles = Article.objects.select_related("author", "publisher").all()
    newsletters = Newsletter.objects.select_related("author").prefetch_related(
        "articles"
    )

    context = {
        "articles": articles,
        "newsletters": newsletters,
    }
    return render(request, "core/editor_article_list.html", context)


@login_required
def approve_article_view(request, article_id):
    """
    Allow an editor to approve an article.

    Once approved:
    - the article becomes visible to readers
    - subscriber email logic is triggered
    - a simple external API call is triggered
    """
    if request.user.role != "editor":
        messages.error(request, "Only editors can approve articles.")
        return redirect("dashboard")

    article = get_object_or_404(Article, id=article_id)

    if not article.approved:
        article.approved = True
        article.save()

        recipients = set()

        if article.publisher:
            for subscriber in article.publisher.subscribers.all():
                if subscriber.email:
                    recipients.add(subscriber.email)

        for subscriber in article.author.journalist_subscribers.all():
            if subscriber.email:
                recipients.add(subscriber.email)

        if recipients:
            send_mail(
                subject=f"New Approved Article: {article.title}",
                message=f"{article.title}\n\n{article.content}",
                from_email=getattr(
                    settings,
                    "DEFAULT_FROM_EMAIL",
                    "admin@example.com",
                ),
                recipient_list=list(recipients),
                fail_silently=True,
            )

        try:
            requests.post(
                "https://httpbin.org/post",
                json={
                    "title": article.title,
                    "author": article.author.username,
                    "publisher": article.publisher.name if article.publisher else None,
                    "approved": article.approved,
                },
                timeout=5,
            )
        except requests.RequestException:
            pass

        messages.success(request, "Article approved successfully.")
    else:
        messages.info(request, "Article was already approved.")

    return redirect("editor_article_list")


@login_required
def create_article_view(request):
    """
    Allow a journalist to create a new article.

    New articles are unapproved by default and must be reviewed by an editor.
    """
    if request.user.role != "journalist":
        messages.error(request, "Only journalists can create articles.")
        return redirect("dashboard")

    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.approved = False
            article.save()
            messages.success(request, "Article created successfully.")
            return redirect("journalist_dashboard")
    else:
        form = ArticleForm()

    return render(request, "core/article_form.html", {"form": form})


@login_required
def update_article_view(request, article_id):
    """
    Allow journalists to update their own articles.
    Editors may update any article.
    """
    article = get_object_or_404(Article, id=article_id)

    if request.user.role == "journalist" and article.author != request.user:
        messages.error(request, "You can only edit your own articles.")
        return redirect("journalist_dashboard")

    if request.user.role not in ["journalist", "editor"]:
        messages.error(request, "You are not allowed to edit articles.")
        return redirect("dashboard")

    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            updated_article = form.save(commit=False)

            if request.user.role == "journalist":
                updated_article.approved = False

            updated_article.save()
            messages.success(request, "Article updated successfully.")

            if request.user.role == "editor":
                return redirect("editor_article_list")
            return redirect("journalist_dashboard")
    else:
        form = ArticleForm(instance=article)

    return render(request, "core/article_form.html", {"form": form})


@login_required
def delete_article_view(request, article_id):
    """
    Allow journalists to delete their own articles.
    Editors may delete any article.
    """
    article = get_object_or_404(Article, id=article_id)

    if request.user.role == "journalist" and article.author != request.user:
        messages.error(request, "You can only delete your own articles.")
        return redirect("journalist_dashboard")

    if request.user.role not in ["journalist", "editor"]:
        messages.error(request, "You are not allowed to delete articles.")
        return redirect("dashboard")

    if request.method == "POST":
        article.delete()
        messages.success(request, "Article deleted successfully.")

        if request.user.role == "editor":
            return redirect("editor_article_list")
        return redirect("journalist_dashboard")

    return render(
        request,
        "core/delete_confirm.html",
        {"object": article, "type": "article"},
    )


@login_required
def create_newsletter_view(request):
    """
    Allow journalists to create newsletters.
    """
    if request.user.role != "journalist":
        messages.error(request, "Only journalists can create newsletters.")
        return redirect("dashboard")

    if request.method == "POST":
        form = NewsletterForm(request.POST)
        if form.is_valid():
            newsletter = form.save(commit=False)
            newsletter.author = request.user
            newsletter.save()
            form.save_m2m()
            messages.success(request, "Newsletter created successfully.")
            return redirect("journalist_dashboard")
    else:
        form = NewsletterForm()

    return render(request, "core/newsletter_form.html", {"form": form})


@login_required
def update_newsletter_view(request, newsletter_id):
    """
    Allow journalists to update their own newsletters.
    Editors may also update any newsletter.
    """
    newsletter = get_object_or_404(Newsletter, id=newsletter_id)

    if request.user.role == "journalist" and newsletter.author != request.user:
        messages.error(request, "You can only edit your own newsletters.")
        return redirect("journalist_dashboard")

    if request.user.role not in ["journalist", "editor"]:
        messages.error(request, "You are not allowed to edit newsletters.")
        return redirect("dashboard")

    if request.method == "POST":
        form = NewsletterForm(request.POST, instance=newsletter)
        if form.is_valid():
            form.save()
            messages.success(request, "Newsletter updated successfully.")

            if request.user.role == "editor":
                return redirect("editor_article_list")
            return redirect("journalist_dashboard")
    else:
        form = NewsletterForm(instance=newsletter)

    return render(request, "core/newsletter_form.html", {"form": form})


@login_required
def delete_newsletter_view(request, newsletter_id):
    """
    Allow journalists to delete their own newsletters.
    Editors may delete any newsletter.
    """
    newsletter = get_object_or_404(Newsletter, id=newsletter_id)

    if request.user.role == "journalist" and newsletter.author != request.user:
        messages.error(request, "You can only delete your own newsletters.")
        return redirect("journalist_dashboard")

    if request.user.role not in ["journalist", "editor"]:
        messages.error(request, "You are not allowed to delete newsletters.")
        return redirect("dashboard")

    if request.method == "POST":
        newsletter.delete()
        messages.success(request, "Newsletter deleted successfully.")

        if request.user.role == "editor":
            return redirect("editor_article_list")
        return redirect("journalist_dashboard")

    return render(
        request,
        "core/delete_confirm.html",
        {"object": newsletter, "type": "newsletter"},
    )


@login_required
def create_publisher_view(request):
    """
    Allow editors to create publisher records.

    This is separate from user registration.
    """
    if request.user.role != "editor":
        messages.error(request, "Only editors can create publishers.")
        return redirect("dashboard")

    if request.method == "POST":
        form = PublisherForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Publisher created successfully.")
            return redirect("editor_article_list")
    else:
        form = PublisherForm()

    return render(request, "core/publisher_form.html", {"form": form})


@login_required
def subscribe_publisher_view(request, publisher_id):
    """
    Allow readers to subscribe to publishers.
    """
    if request.user.role != "reader":
        messages.error(request, "Only readers can subscribe to publishers.")
        return redirect("dashboard")

    if request.method != "POST":
        return redirect("article_list")

    publisher = get_object_or_404(Publisher, id=publisher_id)

    if publisher in request.user.subscribed_publishers.all():
        messages.info(request, f"You are already subscribed to {publisher.name}.")
    else:
        request.user.subscribed_publishers.add(publisher)
        messages.success(request, f"You subscribed to {publisher.name}.")

    return redirect("article_list")


@login_required
def unsubscribe_publisher_view(request, publisher_id):
    """
    Allow readers to unsubscribe from publishers.
    """
    if request.user.role != "reader":
        messages.error(request, "Only readers can unsubscribe from publishers.")
        return redirect("dashboard")

    if request.method != "POST":
        return redirect("article_list")

    publisher = get_object_or_404(Publisher, id=publisher_id)

    if publisher in request.user.subscribed_publishers.all():
        request.user.subscribed_publishers.remove(publisher)
        messages.success(request, f"You unsubscribed from {publisher.name}.")
    else:
        messages.info(request, f"You are not subscribed to {publisher.name}.")

    return redirect("article_list")


@login_required
def subscribe_journalist_view(request, journalist_id):
    """
    Allow readers to subscribe to journalists.
    """
    if request.user.role != "reader":
        messages.error(request, "Only readers can subscribe to journalists.")
        return redirect("dashboard")

    if request.method != "POST":
        return redirect("article_list")

    journalist = get_object_or_404(User, id=journalist_id, role="journalist")

    if journalist in request.user.subscribed_journalists.all():
        messages.info(
            request,
            f"You are already subscribed to {journalist.username}.",
        )
    else:
        request.user.subscribed_journalists.add(journalist)
        messages.success(request, f"You subscribed to {journalist.username}.")

    return redirect("article_list")


@login_required
def unsubscribe_journalist_view(request, journalist_id):
    """
    Allow readers to unsubscribe from journalists.
    """
    if request.user.role != "reader":
        messages.error(request, "Only readers can unsubscribe from journalists.")
        return redirect("dashboard")

    if request.method != "POST":
        return redirect("article_list")

    journalist = get_object_or_404(User, id=journalist_id, role="journalist")

    if journalist in request.user.subscribed_journalists.all():
        request.user.subscribed_journalists.remove(journalist)
        messages.success(request, f"You unsubscribed from {journalist.username}.")
    else:
        messages.info(request, f"You are not subscribed to {journalist.username}.")

    return redirect("article_list")