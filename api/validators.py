from django.contrib.auth import authenticate
from rest_framework import serializers, status
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken

from .exception import CustomApiException
from .models import CustomUser, Review


class CustomSerializerValidator:
    requires_context = True

    def __call__(self, data, serializer):
        user_data = dict(data)
        email = user_data.get('email')
        confirmation_code = user_data.get('confirmation_code')
        if confirmation_code is None:
            raise serializers.ValidationError(
                'An confirmation_code  is required to auth.'
            )
        authenticate(email=email)
        user = get_object_or_404(
            CustomUser,
            email=email,
            confirmation_code=confirmation_code
        )
        refresh = RefreshToken.for_user(user)
        user = CustomUser.objects.filter(email=email)
        user.update(
            email=email,
            confirmation_code=None
        )
        return {
            'token': str(refresh.access_token)
        }


class CustomReviewValidator:
    requires_context = True

    def __call__(self, data, author, is_POST: bool, title, serializer):
        if (
                Review.objects.filter(author=author, title=title).exists()
                and is_POST
        ):
            raise CustomApiException(
                detail='You can send 1 review on title',
                status_code=status.HTTP_400_BAD_REQUEST
            )
        return data
