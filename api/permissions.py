from rest_framework import permissions, status

from api.exception import CustomApiException


class RoleUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            raise CustomApiException(
                detail='UNAUTHORIZED',
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        if (
                request.user.is_superuser
                or view.action in ['partial_update', 'retrieve']
        ):
            return True

    def has_permission(self, request, view, **kwargs):
        if request.user.is_anonymous:
            raise CustomApiException(
                detail='UNAUTHORIZED',
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        if request.user.is_admin or request.user.is_superuser:
            return True

        if request.resolver_match.kwargs.get('username') == 'me':
            if request.method in ['GET', 'PATCH']:
                return True
            else:
                raise CustomApiException(
                    detail='Only GET, PATCH allowed methods',
                    status_code=status.HTTP_405_METHOD_NOT_ALLOWED
                )


class RoleCategory(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            if request.method in permissions.SAFE_METHODS:
                return True
            else:
                raise CustomApiException(
                    detail='UNAUTHORIZED',
                    status_code=status.HTTP_401_UNAUTHORIZED
                )
        if request.user.is_admin or request.user.is_superuser:
            return True
        if request.user.is_user or request.user.is_moder:
            return False


class RoleGenreOrTitle(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            if request.method in permissions.SAFE_METHODS:
                return True
            else:
                raise CustomApiException(
                    detail='UNAUTHORIZED',
                    status_code=status.HTTP_401_UNAUTHORIZED
                )
        if request.user.is_admin or request.user.is_superuser:
            return True


class RoleReviewOrComment(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if (
                request.user == obj.author
                or request.user.is_admin or request.user.is_moder
                and request.method in ['GET', 'PATCH', 'PUT', 'DELETE']
        ):
            return True

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            if request.method in permissions.SAFE_METHODS:
                return True
            else:
                raise CustomApiException(
                    detail='UNAUTHORIZED',
                    status_code=status.HTTP_401_UNAUTHORIZED
                )
        if request.user.is_authenticated:
            return True
