from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Category, Comment, Genre, Review, Title, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'first_name',
            'last_name',
            'username',
            'bio',
            'role',
            'email'
        )
        model = User
        extra_kwargs = {
            'username': {
                'validators': [UniqueValidator(queryset=User.objects.all(), )],
                'required': True},
            'email': {
                'validators': [UniqueValidator(queryset=User.objects.all(), )],
                'required': True},
            'role': {'required': True}

        }


class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        read_only_fields = ('username', 'role', 'email')
        fields = (*read_only_fields, 'first_name', 'bio', 'last_name',)
        model = User


class EmailRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('email', 'conformation_code')
        model = User
        extra_kwargs = {
            'email': {
                'validators': [UniqueValidator(queryset=User.objects.all(), )],
                'required': True},
        }


class NewTokenObtainSerializer(serializers.Serializer):
    email = serializers.EmailField()
    conformation_code = serializers.CharField()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ['id']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ['id']


class TitleReadSerializer(serializers.ModelSerializer):

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


class TitleWriteSerializer(serializers.ModelSerializer):

    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )

    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many='true'
    )

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Review"""
    author = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        required=False
    )

    class Meta:
        model = Review
        exclude = ['title']

    def validate(self, data):
        # Проверка что пользователь не пытается оставить отзыв повторно
        if self.context['request'].method == 'POST' and Review.objects.filter(
                author=self.context['request'].user,
                title=self.context['request'].parser_context['kwargs'].get(
                    'title_id')).exists():
            raise serializers.ValidationError(
                detail="Review exist",
                code=400
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Comment"""
    author = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        required=False
    )

    class Meta:
        model = Comment
        exclude = ['review']
