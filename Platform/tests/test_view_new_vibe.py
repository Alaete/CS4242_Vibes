from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse
from django.utils import timezone
from ..forms import NewVibeForm
from ..models import Vibe
from ..views import new_vibe


class NewVibeTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_new_vibe_view_success_status_code(self):
        url = reverse('new_vibe')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_new_vibe_url_resolves_new_vibe_view(self):
        view = resolve('/new_vibe/')
        self.assertEquals(view.func, new_vibe)

    def test_new_vibe_view_contains_link_back_to_home_view(self):
        new_vibe_url = reverse('new_vibe')
        home_url = reverse('home')
        response = self.client.get(new_vibe_url)
        self.assertContains(response, 'href="{0}"'.format(home_url))

    def test_csrf(self):
        url = reverse('new_vibe')
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        url = reverse('new_vibe')
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, NewVibeForm)

    def test_new_vibe_invalid_post_data(self):
        url = reverse('new_vibe')
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)

    def test_new_topic_valid_post_data(self):
        url = reverse('new_vibe')
        data = {
            'title': 'Test title',
            'body': 'Lorem ipsum dolor sit amet'
        }
        self.client.post(url, data)
        self.assertTrue(Vibe.objects.exists())

    def test_new_topic_invalid_post_data_empty_fields(self):
        url = reverse('new_vibe')
        data = {
            'title': '',
            'body': ''
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Vibe.objects.exists())
