from time import time

from django.test import Client, TestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Category, Comment, CustomUser, Genre, Review, Title


class ApiTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = CustomUser.objects.create_user(
            email='user1@yandex.ru',
            confirmation_code=12345,
            role='user',
            username='user'
        )
        cls.moderator = CustomUser.objects.create_user(
            email='moderator1@yandex.ru',
            confirmation_code=12345,
            role='moderator',
            username='moderator'
        )
        cls.admin = CustomUser.objects.create_user(
            email='admin1@yandex.ru',
            confirmation_code=12345,
            role='admin',
            username='admin'
        )
        cls.genres = Genre.objects.create(
            name='genre_name1',
            slug='slugOfGenre1'
        )
        cls.categories = Category.objects.create(
            name='categories',
            slug='categories1'
        )

        cls.title = Title.objects.create(
            name='titleName1',
            year=time(),
            description='desc',
            category=cls.categories,
        )
        cls.review = Review.objects.create(
            text='namereview1',
            pub_date=time,
            author=cls.user,
            title=cls.title,
            score=7,
        )
        cls.review_admin = Review.objects.create(
            text='namereview1',
            pub_date=time,
            author=cls.admin,
            title=cls.title,
            score=7,
        )
        cls.comment1 = Comment.objects.create(
            text='commentTest',
            author=cls.admin,
            review=cls.review
        )
        cls.comment2 = Comment.objects.create(
            text='commentTest',
            author=cls.user,
            review=cls.review
        )

    def setUp(self):
        self.guest_client = Client()
        self.userc = Client()
        self.moderatorc = Client()
        self.adminc = Client()
        self.user2 = CustomUser.objects.create_user(
            email='user2@yandex.ru',
            confirmation_code=12345,
            role='user',
            username='user1'
        )
        self.moderator2 = CustomUser.objects.create_user(
            email='moderator2@yandex.ru',
            confirmation_code=12345,
            role='moderator',
            username='moderator2'
        )
        self.admin2 = CustomUser.objects.create_user(
            email='admin2@yandex.ru',
            confirmation_code=12345,
            role='admin',
            username='admin2',
            is_superuser=True,
        )

    def test_get_categories(self):
        response = self.guest_client.get('/api/v1/genres/')
        self.assertEqual(response.status_code == 200, True)
        self.assertEqual(len(response.json()) == 4, True)
        response = self.userc.get('/api/v1/genres/')
        self.assertEqual(response.status_code == 200, True)
        self.assertEqual(len(response.json()) == 4, True)
        response = self.moderatorc.get('/api/v1/genres/')
        self.assertEqual(response.status_code == 200, True)
        self.assertEqual(len(response.json()) == 4, True)
        response = self.adminc.get('/api/v1/genres/')
        self.assertEqual(response.status_code == 200, True)
        self.assertEqual(len(response.json()) == 4, True)

    def test_post_genres_admin(self):
        client = APIClient()
        refresh = RefreshToken.for_user(self.admin2)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        data = {
            'genre': 1,
            'slug': 'test1',
            'name': 'test2'
        }

        response = self.adminc.post(
            '/api/v1/genres/', data=data,
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )
        self.assertEqual(response.status_code == 201, True)
        self.assertEqual(len(response.json()) == 2, True)

    def test_post_genres_moderator(self):
        client = APIClient()
        refresh = RefreshToken.for_user(self.moderator2)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        data = {
            'genre': 1,
            'slug': 'test1',
            'name': 'test2'
        }

        response = self.moderatorc.post(
            '/api/v1/genres/', data=data,
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )
        self.assertEqual(response.status_code == 403, True)

    def test_post_genres_user(self):
        client = APIClient()
        refresh = RefreshToken.for_user(self.user2)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        data = {
            'genre': 1,
            'slug': 'test1',
            'name': 'test2'
        }

        response = self.userc.post(
            '/api/v1/genres/', data=data,
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )
        self.assertEqual(response.status_code == 403, True)

    def test_post_genres_guest(self):
        data = {
            'genre': 1,
            'slug': 'test1',
            'name': 'test2'
        }
        response = self.guest_client.post('/api/v1/genres/', data=data)
        self.assertEqual(response.status_code == 401, True)

    def test_post_ununique_genres_data(self):
        client = APIClient()
        refresh = RefreshToken.for_user(self.admin2)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        data1 = {
            'genre': 1,
            'slug': 'test1',
            'name': 'test2'
        }
        data2 = {
            'genre': 1,
            'slug': 'test1',
            'name': 'test2'
        }

        response1 = self.adminc.post(
            '/api/v1/genres/', data=data1,
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )
        response2 = self.adminc.post(
            '/api/v1/genres/', data=data2,
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )
        self.assertEqual(response1.status_code == 201, True)
        self.assertEqual(response2.status_code == 400, True)

    def test_delete_genres_admin(self):
        client = APIClient()
        refresh = RefreshToken.for_user(self.admin2)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        response1 = self.adminc.delete(
            '/api/v1/genres/1/',
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )
        self.assertEqual(response1.status_code == 404, True)

    def test_delete_genres_moderator(self):
        client = APIClient()
        refresh = RefreshToken.for_user(self.moderator2)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        response = self.moderatorc.delete(
            '/api/v1/genres/1/',
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )
        self.assertEqual(response.status_code == 403, True)

    def test_delete_genres_user(self):
        client = APIClient()
        refresh = RefreshToken.for_user(self.user)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        response = self.userc.delete(
            '/api/v1/genres/1/',
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )
        self.assertEqual(response.status_code == 403, True)

    def test_post_categories_admin(self):
        client = APIClient()
        refresh = RefreshToken.for_user(self.admin2)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        data = {
            'genre': 1,
            'slug': 'test1',
            'name': 'test2'
        }

        response = self.adminc.post(
            '/api/v1/categories/', data=data,
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )
        self.assertEqual(response.status_code == 201, True)
        self.assertEqual(len(response.json()) == 2, True)

    def test_post_categories_moderator(self):
        client = APIClient()
        refresh = RefreshToken.for_user(self.moderator2)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        data = {
            'genre': 1,
            'slug': 'test1',
            'name': 'test2'
        }

        response = self.moderatorc.post(
            '/api/v1/categories/', data=data,
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )
        self.assertEqual(response.status_code == 403, True)

    def test_post_categories_user(self):
        client = APIClient()
        refresh = RefreshToken.for_user(self.user2)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        data = {
            'genre': 1,
            'slug': 'test1',
            'name': 'test2'
        }

        response = self.userc.post(
            '/api/v1/categories/', data=data,
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )
        self.assertEqual(response.status_code == 403, True)

    def test_post_categories_guest(self):
        data = {
            'genre': 1,
            'slug': 'test1',
            'name': 'test2'
        }
        response = self.guest_client.post('/api/v1/categories/', data=data)
        self.assertEqual(response.status_code == 401, True)

    def test_post_ununique_categories_data(self):
        client = APIClient()
        refresh = RefreshToken.for_user(self.admin2)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        data1 = {
            'genre': 1,
            'slug': 'test1',
            'name': 'test2'
        }
        data2 = {
            'genre': 1,
            'slug': 'test1',
            'name': 'test2'
        }

        response1 = self.adminc.post(
            '/api/v1/genres/', data=data1,
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )
        response2 = self.adminc.post(
            '/api/v1/genres/', data=data2,
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )
        self.assertEqual(response1.status_code == 201, True)
        self.assertEqual(response2.status_code == 400, True)

    def test_delete_categories_admin(self):
        client = APIClient()
        refresh = RefreshToken.for_user(self.admin2)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        response = self.adminc.delete(
            '/api/v1/categories/1/',
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )
        self.assertEqual(response.status_code == 404, True)

    def test_delete_categories_moderator(self):
        client = APIClient()
        refresh = RefreshToken.for_user(self.moderator2)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        response = self.moderatorc.delete(
            '/api/v1/categories/1/',
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )
        self.assertEqual(response.status_code == 403, True)

    def test_delete_categories_user(self):
        client = APIClient()
        refresh = RefreshToken.for_user(self.user2)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        response = self.userc.delete(
            '/api/v1/categories/1/',
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )
        self.assertEqual(response.status_code == 403, True)

    def test_get_titles(self):
        response = self.guest_client.get('/api/v1/titles/')
        self.assertEqual(response.status_code == 200, True)
        self.assertEqual(len(response.json()) == 4, True)

    def test_get_titles_object(self):
        response = self.guest_client.get('/api/v1/titles/1/')
        self.assertEqual(response.status_code == 200, True)
        self.assertEqual(len(response.json()) == 7, True)
        response = self.userc.get('/api/v1/titles/1/')
        self.assertEqual(response.status_code == 200, True)
        self.assertEqual(len(response.json()) == 7, True)
        response = self.moderatorc.get('/api/v1/titles/1/')
        self.assertEqual(response.status_code == 200, True)
        self.assertEqual(len(response.json()) == 7, True)
        response = self.adminc.get('/api/v1/titles/1/')
        self.assertEqual(response.status_code == 200, True)
        self.assertEqual(len(response.json()) == 7, True)

    def test_post_titles_admin(self):
        client = APIClient()
        refresh = RefreshToken.for_user(self.admin2)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        data = {
            'name': 'test1',
            'year': 2021,
            'description': 'testdesc1',
            'category': self.categories.slug
        }

        response = self.adminc.post(
            '/api/v1/titles/', data=data,
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )
        self.assertEqual(response.status_code == 201, True)
        self.assertEqual(len(response.json()) == 6, True)

    def test_post_titles_moderator(self):
        client = APIClient()
        refresh = RefreshToken.for_user(self.moderator2)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        data = {
            'name': 'test1',
            'year': 2021,
            'description': 'testdesc1',
            'category': self.categories.slug
        }

        response = self.moderatorc.post(
            '/api/v1/titles/', data=data,
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )
        self.assertEqual(response.status_code == 403, True)

    def test_post_titles_user(self):
        client = APIClient()
        refresh = RefreshToken.for_user(self.user2)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        data = {
            'name': 'test1',
            'year': 2021,
            'description': 'testdesc1',
            'category': self.categories.slug
        }
        response = self.userc.post(
            '/api/v1/titles/', data=data,
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )
        self.assertEqual(response.status_code == 403, True)

    def test_post_titles_guest(self):
        data = {
            'name': 'test1',
            'year': 2021,
            'description': 'testdesc1',
            'category': self.categories
        }
        response = self.guest_client.post('/api/v1/titles/', data=data)
        self.assertEqual(response.status_code == 401, True)

    def test_post_many_titles_data(self):
        client = APIClient()
        refresh = RefreshToken.for_user(self.admin2)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        data1 = {
            'name': 'test1',
            'year': 2021,
            'description': 'testdesc1',
            'category': self.categories.slug
        }
        data2 = {
            'name': 'test1',
            'year': 2021,
            'description': 'testdesc1',
            'category': self.categories.slug
        }
        response1 = self.adminc.post(
            '/api/v1/titles/', data=data1,
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )
        response2 = self.adminc.post(
            '/api/v1/titles/', data=data2,
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )
        self.assertEqual(response1.status_code == 201, True)
        self.assertEqual(response2.status_code == 201, True)

    def test_post_titles_response(self):
        client = APIClient()
        refresh = RefreshToken.for_user(self.admin2)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        data1 = {
            'name': 'test1',
            'year': 2021,
            'description': 'testdesc1',
            'category': self.categories.slug
        }

        response = self.adminc.post(
            '/api/v1/titles/',
            data=data1, HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )
        self.assertIsInstance(response.json()['id'], int)
        self.assertEqual(response.json()['name'] == 'test1', True)
        self.assertEqual(response.json()['description'] == 'testdesc1', True)
        self.assertEqual(response.json()['category'] == 'categories1', True)
        self.assertEqual(response.status_code == 201, True)

    def test_delete_title_admin(self):
        client = APIClient()
        refresh = RefreshToken.for_user(self.admin2)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        response = self.adminc.delete(
            '/api/v1/titles/1/',
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )
        self.assertEqual(response.status_code == 204, True)

    def test_delete_title_moderator(self):
        client = APIClient()
        refresh = RefreshToken.for_user(self.moderator2)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        response = self.moderatorc.delete(
            '/api/v1/titles/1/',
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )
        self.assertEqual(response.status_code == 403, True)

    def test_delete_title_user(self):
        client = APIClient()
        refresh = RefreshToken.for_user(self.user2)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        response = self.userc.delete(
            '/api/v1/titles/1/',
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )
        self.assertEqual(response.status_code == 403, True)

    def test_get_review(self):
        response = self.guest_client.get('/api/v1/titles/1/reviews/')
        self.assertEqual(response.status_code == 200, True)
        self.assertEqual(len(response.json()) == 4, True)

    def test_get_review_object(self):
        response = self.guest_client.get('/api/v1/titles/1/reviews/1/')
        self.assertEqual(response.status_code == 200, True)
        self.assertEqual(len(response.json()) == 6, True)
        response = self.userc.get('/api/v1/titles/1/reviews/1/')
        self.assertEqual(response.status_code == 200, True)
        self.assertEqual(len(response.json()) == 6, True)
        response = self.moderatorc.get('/api/v1/titles/1/reviews/1/')
        self.assertEqual(response.status_code == 200, True)
        self.assertEqual(len(response.json()) == 6, True)
        response = self.adminc.get('/api/v1/titles/1/reviews/1/')
        self.assertEqual(response.status_code == 200, True)
        self.assertEqual(len(response.json()) == 6, True)

    def test_post_review_admin(self):
        client = APIClient()
        refresh = RefreshToken.for_user(self.admin2)
        client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )
        data = {
            'text': 'textReview',
            'score': 5,
        }
        response = self.adminc.post(
            '/api/v1/titles/1/reviews/', data=data,
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )
        self.assertEqual(response.status_code == 201, True)
        self.assertEqual(len(response.json()) == 3, True)

    def test_post_review_moderator(self):
        client = APIClient()
        refresh = RefreshToken.for_user(self.moderator2)
        client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )
        data = {
            'text': 'textReview',
            'score': 5,
        }
        response = self.moderatorc.post(
            '/api/v1/titles/1/reviews/', data=data,
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )
        self.assertEqual(response.status_code == 201, True)

    def test_post_review_user(self):
        client = APIClient()
        refresh = RefreshToken.for_user(self.user2)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        data = {
            'text': 'textReview',
            'score': 5,
        }
        response = self.userc.post(
            '/api/v1/titles/1/reviews/', data=data,
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )
        self.assertEqual(response.status_code == 201, True)

    def test_post_review_guest(self):
        data = {
            'text': 'textReview',
            'score': 5,
        }
        response = self.guest_client.post(
            '/api/v1/titles/1/reviews/', data=data
        )
        self.assertEqual(response.status_code == 401, True)

    def test_post_many_review_data(self):
        client = APIClient()
        refresh = RefreshToken.for_user(self.admin2)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        data1 = {
            'text': 'textReview',
            'score': 5,
        }
        data2 = {
            'text': 'textReview',
            'score': 5,
        }
        response1 = self.adminc.post(
            '/api/v1/titles/1/reviews/', data=data1,
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )
        response2 = self.adminc.post(
            '/api/v1/titles/1/reviews/', data=data2,
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )
        self.assertEqual(response1.status_code == 201, True)
        self.assertEqual(response2.status_code == 400, True)

    def test_post_review_response(self):
        client = APIClient()
        refresh = RefreshToken.for_user(self.admin2)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        data = {
            'text': 'textReview',
            'score': 5,
        }
        response = self.adminc.post(
            '/api/v1/titles/1/reviews/', data=data,
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        self.assertIsInstance(response.json()['id'], int)
        self.assertEqual(response.json()['text'] == 'textReview', True)
        self.assertEqual(response.json()['score'] == 5, True)
        self.assertEqual(response.status_code == 201, True)

    def test_post_review_response_rating(self):
        client = APIClient()
        refresh = RefreshToken.for_user(self.admin2)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        data1 = {
            'text': 'textReview',
            'score': 6,
        }
        data2 = {
            'text': 'textReview',
            'score': 5,
        }
        self.adminc.post(
            '/api/v1/titles/1/reviews/',
            data=data1, HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )
        refresh = RefreshToken.for_user(self.user2)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        self.adminc.post(
            '/api/v1/titles/1/reviews/',
            data=data2, HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )
        refresh = RefreshToken.for_user(self.admin2)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        response3 = self.adminc.get(
            '/api/v1/titles/1/',
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )
        avg_rating = response3.json()['rating']
        self.assertEqual(avg_rating == 6.25, True)
        self.assertIsInstance(avg_rating, float)

    def test_post_review_delete_permission_admin(self):
        client = APIClient()
        refresh = RefreshToken.for_user(self.admin2)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        response = self.adminc.delete(
            '/api/v1/titles/1/reviews/1/',
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )
        self.assertEqual(response.status_code == 204, True)
        get_count = len(Review.objects.filter(id=1))
        self.assertEqual(get_count == 0, True)

    def test_post_review_delete_permission_moderator(self):
        client = APIClient()
        refresh = RefreshToken.for_user(self.moderator2)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        response = self.moderatorc.delete(
            '/api/v1/titles/1/reviews/1/',
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )
        self.assertEqual(response.status_code == 204, True)
        get_count = len(Review.objects.filter(id=1))
        self.assertEqual(get_count == 0, True)

    def test_post_review_delete_permission_user(self):
        client = APIClient()
        refresh = RefreshToken.for_user(self.moderator2)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        response = self.moderatorc.delete(
            '/api/v1/titles/1/reviews/1/',
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )
        self.assertEqual(response.status_code == 204, True)
        get_count = len(Review.objects.filter(id=1))
        self.assertEqual(get_count == 0, True)

    def test_post_review_delete_permission_not_owner_user(self):
        client = APIClient()
        refresh = RefreshToken.for_user(self.user2)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        response = self.userc.delete(
            '/api/v1/titles/1/reviews/2/',
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )
        self.assertEqual(response.status_code == 403, True)
        get_count = len(Review.objects.filter(id=2))
        self.assertEqual(get_count == 1, True)

    def test_get_comment(self):
        response = self.guest_client.get(
            '/api/v1/titles/1/reviews/1/comments/'
        )
        self.assertEqual(response.status_code == 200, True)
        self.assertEqual(len(response.json()) == 4, True)

    def test_get_comment_object(self):
        response = self.guest_client.get(
            '/api/v1/titles/1/reviews/1/comments/1/'
        )
        self.assertEqual(response.status_code == 200, True)
        self.assertEqual(len(response.json()) == 4, True)
        response = self.userc.get(
            '/api/v1/titles/1/reviews/1/comments/1/'
        )
        self.assertEqual(response.status_code == 200, True)
        self.assertEqual(len(response.json()) == 4, True)
        response = self.moderatorc.get(
            '/api/v1/titles/1/reviews/1/comments/1/')
        self.assertEqual(response.status_code == 200, True)
        self.assertEqual(len(response.json()) == 4, True)
        response = self.adminc.get(
            '/api/v1/titles/1/reviews/1/comments/1/'
        )
        self.assertEqual(response.status_code == 200, True)
        self.assertEqual(len(response.json()) == 4, True)

    def test_post_comment_admin(self):
        client = APIClient()
        refresh = RefreshToken.for_user(self.admin2)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        data = {
            'text': 'textComment'
        }
        response = self.adminc.post(
            '/api/v1/titles/1/reviews/1/comments/', data=data,
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )
        self.assertEqual(response.status_code == 201, True)
        self.assertEqual(len(response.json()) == 2, True)

    def test_post_comment_moderator(self):
        client = APIClient()
        refresh = RefreshToken.for_user(self.moderator2)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        data = {
            'text': 'textComment'
        }
        response = self.moderatorc.post(
            '/api/v1/titles/1/reviews/1/comments/', data=data,
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )
        self.assertEqual(response.status_code == 201, True)
        self.assertEqual(len(response.json()) == 2, True)

    def test_post_comement_user(self):
        client = APIClient()
        refresh = RefreshToken.for_user(self.user2)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        data = {
            'text': 'textComment'
        }
        response = self.userc.post(
            '/api/v1/titles/1/reviews/1/comments/', data=data,
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )
        self.assertEqual(response.status_code == 201, True)

    def test_post_comment_guest(self):
        data = {
            'text': 'textComment'
        }
        response = self.guest_client.post(
            '/api/v1/titles/1/reviews/1/comments/', data=data
        )
        self.assertEqual(response.status_code == 401, True)

    def test_post_comment_response(self):
        client = APIClient()
        refresh = RefreshToken.for_user(self.admin2)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        data = {
            'text': 'textComment'
        }
        response = self.adminc.post(
            '/api/v1/titles/1/reviews/1/comments/', data=data,
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )
        self.assertIsInstance(response.json()['id'], int)
        self.assertEqual(response.json()['text'] == 'textComment', True)
        self.assertEqual(response.status_code == 201, True)

    def test_post_comment_delete_permission_admin(self):
        client = APIClient()
        refresh = RefreshToken.for_user(self.admin2)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        response = self.adminc.delete(
            '/api/v1/titles/1/reviews/1/comments/1/',
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )
        self.assertEqual(response.status_code == 204, True)
        get_count = len(Comment.objects.filter(id=1))
        self.assertEqual(get_count == 0, True)

    def test_post_comment_delete_permission_moderator(self):
        client = APIClient()
        refresh = RefreshToken.for_user(self.moderator2)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        response = self.moderatorc.delete(
            '/api/v1/titles/1/reviews/1/comments/1/',
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )
        self.assertEqual(response.status_code == 204, True)
        get_count = len(Comment.objects.filter(id=1))
        self.assertEqual(get_count == 0, True)

    def test_post_comment_delete_permission_user(self):
        client = APIClient()
        refresh = RefreshToken.for_user(self.user)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        response = self.userc.delete(
            '/api/v1/titles/1/reviews/1/comments/2/',
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )
        self.assertEqual(response.status_code == 204, True)
        get_count = len(Comment.objects.filter(id=2))
        self.assertEqual(get_count == 0, True)

    def test_post_comment_delete_permission_not_owner_user(self):
        client = APIClient()
        refresh = RefreshToken.for_user(self.user2)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        response = self.userc.delete(
            '/api/v1/titles/1/reviews/1/comments/2/',
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )
        self.assertEqual(response.status_code == 403, True)
        get_count = len(Comment.objects.filter(id=2))
        self.assertEqual(get_count == 1, True)

    def test_post_comment_delete_permissions_admin(self):
        client = APIClient()
        refresh = RefreshToken.for_user(self.admin2)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        response = self.adminc.delete(
            '/api/v1/titles/1/reviews/1/comments/2/',
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )
        self.assertEqual(response.status_code == 204, True)
        get_count = len(Comment.objects.filter(id=2))
        self.assertEqual(get_count == 0, True)

    def test_post_comment_delete_permissions_moderator(self):
        client = APIClient()
        refresh = RefreshToken.for_user(self.moderator2)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        response = self.moderatorc.delete(
            '/api/v1/titles/1/reviews/1/comments/2/',
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )
        self.assertEqual(response.status_code == 204, True)
        get_count = len(Comment.objects.filter(id=2))
        self.assertEqual(get_count == 0, True)
