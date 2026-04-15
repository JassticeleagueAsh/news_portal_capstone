from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import Article, Newsletter, Publisher, User


class RegisterForm(UserCreationForm):
    """
    Form used to register a new user.

    The role field comes from the custom User model, so once the
    model includes 'publisher' in ROLE_CHOICES, it will also appear
    in the registration form automatically.
    """

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "role", "password1", "password2"]


class LoginForm(AuthenticationForm):
    """
    Form used to log in an existing user.
    """

    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class ArticleForm(forms.ModelForm):
    """
    Form used by journalists and editors to create or update articles.
    """

    class Meta:
        model = Article
        fields = ["title", "content", "publisher"]


class NewsletterForm(forms.ModelForm):
    """
    Form used by journalists and editors to create or update newsletters.
    """

    class Meta:
        model = Newsletter
        fields = ["title", "description", "articles"]
        widgets = {
            "articles": forms.CheckboxSelectMultiple(),
        }


class PublisherForm(forms.ModelForm):
    """
    Form used by editors to create publisher records.
    """

    class Meta:
        model = Publisher
        fields = ["name", "description"]