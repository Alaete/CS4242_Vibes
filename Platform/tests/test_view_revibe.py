from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse
from django.utils import timezone
from ..models import Vibe, Revibe
from ..views import revibe


class RevibeTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='12345')
        vibe = Vibe.objects.create(title='Test', body='Set-up for test', pk=1, created_by=self.user, created_at=timezone.now())
        Revibe.objects.create(title='Test', body='Set-up for test', pk=1, created_by=self.user, created_at=timezone.now(), original=vibe)

    def test_revibe_view_success_status_code(self):
        url = reverse('revibe', kwargs={'pk': 1, 'revibe_pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_vibe_view_not_found_status_code(self):
        url = reverse('revibe', kwargs={'pk': 1, 'revibe_pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_revibe_url_resolves_revibe_view(self):
        view = resolve('/vibe/1/revibe/1/')
        self.assertEquals(view.func, revibe)

    def test_revibe_view_contains_navigation_links(self):
        vibe_url = reverse('vibe', kwargs={'pk': 1})
        homepage_url = reverse('home')
        revibe_url = reverse('revibe', kwargs={'pk': 1, 'revibe_pk': 1})

        response = self.client.get(revibe_url)

        self.assertContains(response, 'href="{0}"'.format(homepage_url))
        self.assertContains(response, 'href="{0}"'.format(vibe_url))
