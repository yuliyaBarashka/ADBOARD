import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from ads.models import Ad

User = get_user_model()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        email='user@test.ru', password='TestPass123!',
        first_name='Иван', last_name='Иванов', phone='+79990000000',
    )


@pytest.fixture
def ad(db, user):
    return Ad.objects.create(
        title='Ноутбук', price=50000, description='Хороший', author=user,
    )


@pytest.mark.django_db
class TestWebPages:
    def test_index(self, client):
        response = client.get(reverse('web:index'))
        assert response.status_code == 200
        assert 'AdBoard' in response.content.decode()

    def test_ad_list(self, client, ad):
        response = client.get(reverse('web:ad-list'))
        assert response.status_code == 200
        assert 'Ноутбук' in response.content.decode()

    def test_ad_list_search(self, client, ad):
        response = client.get(reverse('web:ad-list') + '?search=Ноут')
        assert response.status_code == 200
        assert 'Ноутбук' in response.content.decode()

    def test_ad_detail(self, client, ad):
        response = client.get(reverse('web:ad-detail', args=[ad.pk]))
        assert response.status_code == 200

    def test_ad_create_requires_login(self, client):
        response = client.get(reverse('web:ad-create'))
        assert response.status_code == 302  # редирект на login

    def test_ad_create_authenticated(self, client, user):
        client.force_login(user)
        response = client.get(reverse('web:ad-create'))
        assert response.status_code == 200

    def test_register(self, client):
        response = client.get(reverse('web:register'))
        assert response.status_code == 200

    def test_login(self, client):
        response = client.get(reverse('web:login'))
        assert response.status_code == 200

    def test_profile_requires_login(self, client):
        response = client.get(reverse('web:profile'))
        assert response.status_code == 302

    def test_profile_authenticated(self, client, user):
        client.force_login(user)
        response = client.get(reverse('web:profile'))
        assert response.status_code == 200
