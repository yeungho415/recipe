"""
Tests for the Django admin modifications.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


class AdminSiteTests(TestCase):
    """Tests for Django admin."""

    def setUp(self):
        """Create user and client."""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='testpass123',
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='testpass123',
            name='Test User'
        )

    def test_users_lists(self):
        """Test that users are listed on page."""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        """Test the edit user page works."""
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test the create user page works."""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

# whats self.client = Client() and url = reverse('admin:core_user_changelist') doing?

# !!!
# self.client = Client() is initializing a Django test client object.
# The test client is a Python class that acts as a dummy web browser,
# allowing you to test your views and interact with your Django-powered
# application programmatically. You can simulate GET and POST requests,
# observe the response, and so on. This is used to test your views and
# interactions between them in isolation, without the need for an actual web server.

# The "changelist" view, which displays a list of all instances of the model.

# reverse is a Django utility function to create URLs by using the named URL
# patterns defined in your Django application's urls.py