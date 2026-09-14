import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.core import mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

User = get_user_model()

@pytest.fixture
def user(db):
    return User.objects.create_user(
        email='user@test.ru',
        password='TestPass123!',
        first_name='Иван',
        last_name='Иванов',
        phone='+79990000000',
    )

@pytest.fixture(autouse=True)
def email_backend(settings):
    settings.EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
class TestAuth:
    def test_register(self, api_client):
        url = reverse('register')
        data = {
            'email': 'new@test.ru',
            'first_name': 'Пётр',
            'last_name': 'Петров',
            'phone': '+79991112233',
            'password': 'StrongPass123!',
            'password_confirm': 'StrongPass123!',
        }
        response = api_client.post(url, data)
        assert response.status_code == 201
        assert User.objects.filter(email='new@test.ru').exists()

    def test_login(self, api_client, user):
        url = reverse('token_obtain_pair')
        response = api_client.post(url, {
            'email': user.email,
            'password': 'TestPass123!',
        })
        assert response.status_code == 200
        assert 'access' in response.data
        assert 'refresh' in response.data

    def test_profile_requires_auth(self, api_client):
        url = reverse('profile')
        response = api_client.get(url)
        assert response.status_code == 401

    def test_profile_authenticated(self, api_client, user):
        api_client.force_authenticate(user=user)
        url = reverse('profile')
        response = api_client.get(url)
        assert response.status_code == 200
        assert response.data['email'] == user.email


@pytest.mark.django_db
class TestPasswordReset:
    def test_reset_password_request(self, api_client, user):
        url = reverse('password_reset')
        response = api_client.post(url, {'email': user.email})
        assert response.status_code == 200
        assert len(mail.outbox) == 1
        assert user.email in mail.outbox[0].to

    def test_reset_password_request_unknown_email(self, api_client):
        url = reverse('password_reset')
        response = api_client.post(url, {'email': 'unknown@test.ru'})
        assert response.status_code == 200

    def test_reset_password_request_no_email(self, api_client):
        url = reverse('password_reset')
        response = api_client.post(url, {})
        assert response.status_code == 400

    def test_reset_password_confirm(self, api_client, user):
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        url = reverse('password_reset_confirm')
        response = api_client.post(url, {
            'uid': uid,
            'token': token,
            'new_password': 'NewStrongPass123!',
        })
        assert response.status_code == 200
        user.refresh_from_db()
        assert user.check_password('NewStrongPass123!')

    def test_reset_password_confirm_invalid_uid(self, api_client):
        url = reverse('password_reset_confirm')
        response = api_client.post(url, {
            'uid': 'invalid',
            'token': 'invalid',
            'new_password': 'NewStrongPass123!',
        })
        assert response.status_code == 400

    def test_reset_password_confirm_invalid_token(self, api_client, user):
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        url = reverse('password_reset_confirm')
        response = api_client.post(url, {
            'uid': uid,
            'token': 'invalid-token',
            'new_password': 'NewStrongPass123!',
        })
        assert response.status_code == 400

    def test_reset_password_confirm_missing_fields(self, api_client):
        url = reverse('password_reset_confirm')
        response = api_client.post(url, {})
        assert response.status_code == 400


@pytest.mark.django_db
def test_create_user_without_email():
    with pytest.raises(ValueError):
        User.objects.create_user(email='', password='pass')


@pytest.mark.django_db
def test_user_str(user):
    assert 'Иван Иванов' in str(user)


@pytest.mark.django_db
def test_register_password_mismatch(api_client):
    url = reverse('register')
    response = api_client.post(url, {
        'email': 'x@test.ru',
        'first_name': 'X',
        'last_name': 'Y',
        'phone': '+7',
        'password': 'Pass123!',
        'password_confirm': 'Other123!',
    })
    assert response.status_code == 400
