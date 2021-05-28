from django.forms import ModelForm

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse
from django.utils import timezone

from ..models import Vibe, Revibe
from ..views import RevibeUpdateView


class RevibeUpdateViewTestCase(TestCase):
    def setUp(self):
        self.username = 'john'
        self.password = '123'
        self.user = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password)
        self.vibe = Vibe.objects.create(title='Test', body='Set-up for test', pk=1, created_by=self.user, created_at=timezone.now())
        self.revibe = Revibe.objects.create(title='Test', body='Set-up for test', pk=1, created_by=self.user, created_at=timezone.now(), original=self.vibe)
        self.url = reverse('edit_revibe', kwargs={'pk': self.vibe.pk, 'revibe_pk': self.revibe.pk})


class LoginRequiredRevibeUpdateViewTests(RevibeUpdateViewTestCase):
    def test_redirection(self):
        login_url = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))


class UnauthorizedRevibeUpdateViewTests(RevibeUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        username = 'jane'
        password = '321'
        user = User.objects.create_user(username=username, email='jane@doe.com', password=password)
        self.client.login(username=username, password=password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 404)


class RevibeUpdateViewTests(RevibeUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_class(self):
        view = resolve('/vibe/1/revibe/1/edit/')
        self.assertEquals(view.func.view_class, RevibeUpdateView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, ModelForm)

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 1)
        self.assertContains(self.response, '<textarea', 1)


class SuccessfulRevibeUpdateViewTests(RevibeUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {'body': 'edited body'})

    def test_redirection(self):
        revibe_url = reverse('revibe', kwargs={'pk': self.vibe.pk, 'revibe_pk': self.revibe.pk})
        self.assertRedirects(self.response, revibe_url)

    def test_post_changed(self):
        self.revibe.refresh_from_db()
        self.assertEquals(self.revibe.body, 'edited body')


class InvalidRevibeUpdateViewTests(RevibeUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {})

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)
