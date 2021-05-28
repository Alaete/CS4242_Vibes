from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse
from django.utils import timezone

from ..models import Vibe, Revibe
from ..views import vibe_revibes


class VibeRevibesTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='12345')
        vibe = Vibe.objects.create(title='Test', body='Set-up for test', pk=1, created_by=self.user, created_at=timezone.now())
        revibe = Revibe.objects.create(title='Test', body='Set-up for test', original=vibe, pk=1, created_by=self.user, created_at=timezone.now())
        url = reverse('vibe_revibes', kwargs={'pk': vibe.pk})
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/vibe/1/revibes/')
        self.assertEquals(view.func, vibe_revibes)
