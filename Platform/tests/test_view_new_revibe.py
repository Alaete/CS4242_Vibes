from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse
from django.utils import timezone
from ..forms import NewRevibeForm
from ..models import Vibe, Revibe
from ..views import new_revibe


class NewRevibeTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='12345')
        Vibe.objects.create(title='Test', body='Set-up for test', pk=1, created_by=self.user, created_at=timezone.now())
        self.client.login(username='testuser', password='12345')

    def test_new_revibe_view_success_status_code(self):
        url = reverse('new_revibe', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_new_revibe_view_not_found_status_code(self):
        url = reverse('new_revibe', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_new_revibe_url_resolves_new_revibe_view(self):
        view = resolve('/vibe/1/new_revibe/')
        self.assertEquals(view.func, new_revibe)

    def test_new_revibe_view_contains_link_back_to_vibe_view(self):
        new_revibe_url = reverse('new_revibe', kwargs={'pk': 1})
        vibe_url = reverse('vibe', kwargs={'pk': 1})
        response = self.client.get(new_revibe_url)
        self.assertContains(response, 'href="{0}"'.format(vibe_url))

    def test_csrf(self):
        url = reverse('new_revibe', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        url = reverse('new_revibe', kwargs={'pk': 1})
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, NewRevibeForm)

    def test_new_revibe_invalid_post_data(self):
        url = reverse('new_revibe', kwargs={'pk': 1})
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)

    def test_new_topic_valid_post_data(self):
        url = reverse('new_revibe', kwargs={'pk': 1})
        data = {
            'title': 'Test title',
            'body': 'Lorem ipsum dolor sit amet'
        }
        self.client.post(url, data)
        self.assertTrue(Revibe.objects.exists())

    def test_new_topic_invalid_post_data_empty_fields(self):
        url = reverse('new_revibe', kwargs={'pk': 1})
        data = {
            'title': '',
            'body': ''
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Revibe.objects.exists())
