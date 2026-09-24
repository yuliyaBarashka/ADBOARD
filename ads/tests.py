import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from .models import Ad, Review

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        email='user@test.ru', password='TestPass123!',
        first_name='Иван', last_name='Иванов', phone='+79990000000',
    )


@pytest.fixture
def admin(db):
    return User.objects.create_superuser(
        email='admin@test.ru', password='AdminPass123!',
        first_name='Админ', last_name='Админов', phone='+79991111111',
    )


@pytest.fixture
def ad(db, user):
    return Ad.objects.create(
        title='Ноутбук', price=50000, description='Хороший', author=user,
    )


@pytest.mark.django_db
class TestAd:
    def test_list_anonymous(self, api_client, ad):
        url = reverse('ad-list')
        response = api_client.get(url)
        assert response.status_code == 200
        assert response.data['count'] == 1

    def test_create_requires_auth(self, api_client):
        url = reverse('ad-list')
        response = api_client.post(url, {
            'title': 'X', 'price': 1, 'description': 'Y',
        })
        assert response.status_code == 401

    def test_create_authenticated(self, api_client, user):
        api_client.force_authenticate(user=user)
        url = reverse('ad-list')
        response = api_client.post(url, {
            'title': 'X', 'price': 1, 'description': 'Y',
        })
        assert response.status_code == 201
        assert Ad.objects.count() == 1

    def test_update_own(self, api_client, user, ad):
        api_client.force_authenticate(user=user)
        url = reverse('ad-detail', args=[ad.id])
        response = api_client.patch(url, {'title': 'Обновлено'})
        assert response.status_code == 200

    def test_update_foreign_forbidden(self, api_client, ad):
        other = User.objects.create_user(
            email='other@test.ru', password='Pass123!',
            first_name='Другой', last_name='Юзер', phone='+79992222222',
        )
        api_client.force_authenticate(user=other)
        url = reverse('ad-detail', args=[ad.id])
        response = api_client.patch(url, {'title': 'Хак'})
        assert response.status_code == 403

    def test_admin_can_delete_any(self, api_client, admin, ad):
        api_client.force_authenticate(user=admin)
        url = reverse('ad-detail', args=[ad.id])
        response = api_client.delete(url)
        assert response.status_code == 204

    def test_search_by_title(self, api_client, ad):
        url = reverse('ad-list') + '?search=Ноут'
        response = api_client.get(url)
        assert response.status_code == 200
        assert response.data['count'] == 1

    def test_pagination(self, api_client, user):
        for i in range(6):
            Ad.objects.create(
                title=f'Ad {i}', price=100, description='X', author=user,
            )
        url = reverse('ad-list')
        response = api_client.get(url)
        assert response.data['count'] == 6
        assert len(response.data['results']) == 4


@pytest.mark.django_db
class TestReview:
    def test_create_review(self, api_client, user, ad):
        api_client.force_authenticate(user=user)
        url = reverse('review-list')
        response = api_client.post(url, {'text': 'Отлично', 'ad': ad.id})
        assert response.status_code == 201
        assert Review.objects.count() == 1

    def test_filter_reviews_by_ad(self, api_client, user, ad):
        Review.objects.create(text='A', author=user, ad=ad)
        url = reverse('review-list') + f'?ad={ad.id}'
        response = api_client.get(url)
        assert response.status_code == 200


@pytest.mark.django_db
def test_ad_str(ad):
    assert str(ad) == '[Товар] Ноутбук'


@pytest.mark.django_db
def test_review_str(user, ad):
    review = Review.objects.create(text='OK', author=user, ad=ad)
    assert str(review)  # не пустая


@pytest.mark.django_db
def test_admin_can_update_any(api_client, admin, ad):
    api_client.force_authenticate(user=admin)
    url = reverse('ad-detail', args=[ad.id])
    response = api_client.patch(url, {'title': 'Админ изменил'})
    assert response.status_code == 200


@pytest.mark.django_db
def test_filter_by_type(api_client, user):
    Ad.objects.create(title='Товар', price=100, description='X', type='item', author=user)
    Ad.objects.create(title='Вакансия', price=200, description='Y', type='vacancy', author=user)

    url = reverse('ad-list') + '?type=vacancy'
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data['count'] == 1
    assert response.data['results'][0]['title'] == 'Вакансия'