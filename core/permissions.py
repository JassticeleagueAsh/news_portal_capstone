from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsReaderOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return False


class IsJournalist(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'journalist')


class IsEditorOrJournalist(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role in ['editor', 'journalist']
        )