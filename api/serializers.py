from django.core.validators import EmailValidator
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt import serializers

from .models import Category, Comment, CustomUser, Genre, Review, Title
from .validators import CustomReviewValidator, CustomSerializerValidator


class CustomSerializer(serializers.TokenObtainPairSerializer, ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['confirmation_code']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['password']

    def validate(self, data):
        return CustomSerializerValidator().__call__(data, CustomSerializer)


class UserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'username', 'first_name', 'last_name',
            'email', 'role', 'bio', 'password'
        ]


class EmailSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email']
        extra_kwargs = {
            'email': {'validators': [EmailValidator]},
        }


class ReviewSerializerPost(ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'text', 'score']

    def validate(self, data):
        author = self.context['request'].user
        title = self.context['view'].kwargs.get('title_id')
        method = self.context['request'].method
        is_POST: bool = method == 'POST'
        return (
            CustomReviewValidator().__call__(
                data, author, is_POST, title, ReviewSerializerPost
            )
        )


class ReviewSerializerGet(ModelSerializer):
    author = serializers.serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = ['id', 'text', 'author', 'pub_date', 'score', 'title']


class CommentSerializerGet(ModelSerializer):
    author = serializers.serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ['id', 'text', 'author', 'pub_date']


class CommentSerializerPost(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'text']


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        exclude = ['id']


class GenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        exclude = ['id']


class TitleSerializerGet(ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer(many=False)
    rating = serializers.serializers.FloatField()

    class Meta:
        model = Title
        fields = [
            'id', 'name', 'description',
            'year', 'genre', 'category', 'rating'
        ]


class TitleSerializerPost(ModelSerializer):
    genre = serializers.serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )
    category = serializers.serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        fields = ['id', 'name', 'description', 'year', 'genre', 'category']
        model = Title
