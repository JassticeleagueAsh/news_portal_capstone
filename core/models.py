from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model that supports role-based access control.

    Roles:
    - reader: can view approved articles and newsletters
    - editor: can review and approve articles
    - journalist: can create articles and newsletters
    """

    ROLE_CHOICES = [
        ("reader", "Reader"),
        ("editor", "Editor"),
        ("journalist", "Journalist"),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    subscribed_publishers = models.ManyToManyField(
        "Publisher",
        blank=True,
        related_name="subscribers",
    )
    subscribed_journalists = models.ManyToManyField(
        "self",
        blank=True,
        symmetrical=False,
        related_name="journalist_subscribers",
        limit_choices_to={"role": "journalist"},
    )

    def save(self, *args, **kwargs):
        """
        Clear reader-only subscription fields when the user is a journalist.

        This helps separate reader subscription behaviour from journalist data.
        """
        super().save(*args, **kwargs)

        if self.role == "journalist":
            self.subscribed_publishers.clear()
            self.subscribed_journalists.clear()

    def __str__(self):
        """
        Return a readable string representation of the user.
        """
        return f"{self.username} ({self.role})"


class Publisher(models.Model):
    """
    Represents a news publisher.

    A publisher can have multiple editors and journalists.
    """

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    editors = models.ManyToManyField(
        User,
        blank=True,
        related_name="publisher_editor_roles",
        limit_choices_to={"role": "editor"},
    )
    journalists = models.ManyToManyField(
        User,
        blank=True,
        related_name="publisher_journalist_roles",
        limit_choices_to={"role": "journalist"},
    )

    def __str__(self):
        """
        Return the publisher name.
        """
        return self.name


class Article(models.Model):
    """
    Represents a news article written by a journalist.

    Articles must be approved by an editor before readers can view them.
    """

    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="articles",
        limit_choices_to={"role": "journalist"},
    )
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="articles",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        """
        Return the article title.
        """
        return self.title


class Newsletter(models.Model):
    """
    Represents a curated collection of articles created by a journalist.

    Readers can view newsletters, while journalists create them.
    """

    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="newsletters",
        limit_choices_to={"role": "journalist"},
    )
    articles = models.ManyToManyField(
        Article,
        blank=True,
        related_name="newsletters",
    )

    def __str__(self):
        """
        Return the newsletter title.
        """
        return self.title