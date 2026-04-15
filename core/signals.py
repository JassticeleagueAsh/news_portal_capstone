from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from .models import User


@receiver(post_migrate)
def create_roles_and_permissions(sender, **kwargs):
    reader_group, _ = Group.objects.get_or_create(name='Reader')
    editor_group, _ = Group.objects.get_or_create(name='Editor')
    journalist_group, _ = Group.objects.get_or_create(name='Journalist')

    article_permissions = Permission.objects.filter(
        content_type__app_label='core',
        content_type__model='article'
    )
    newsletter_permissions = Permission.objects.filter(
        content_type__app_label='core',
        content_type__model='newsletter'
    )

    reader_group.permissions.clear()
    editor_group.permissions.clear()
    journalist_group.permissions.clear()

    view_article = article_permissions.filter(codename='view_article')
    view_newsletter = newsletter_permissions.filter(codename='view_newsletter')

    change_article = article_permissions.filter(codename='change_article')
    delete_article = article_permissions.filter(codename='delete_article')
    change_newsletter = newsletter_permissions.filter(codename='change_newsletter')
    delete_newsletter = newsletter_permissions.filter(codename='delete_newsletter')

    add_article = article_permissions.filter(codename='add_article')
    add_newsletter = newsletter_permissions.filter(codename='add_newsletter')

    reader_group.permissions.add(*view_article, *view_newsletter)

    editor_group.permissions.add(
        *view_article, *change_article, *delete_article,
        *view_newsletter, *change_newsletter, *delete_newsletter
    )

    journalist_group.permissions.add(
        *add_article, *view_article, *change_article, *delete_article,
        *add_newsletter, *view_newsletter, *change_newsletter, *delete_newsletter
    )


@receiver(post_save, sender=User)
def assign_user_to_group(sender, instance, created, **kwargs):
    if instance.role:
        instance.groups.clear()

        role_to_group = {
            'reader': 'Reader',
            'editor': 'Editor',
            'journalist': 'Journalist',
        }

        group_name = role_to_group.get(instance.role)
        if group_name:
            group = Group.objects.get(name=group_name)
            instance.groups.add(group)