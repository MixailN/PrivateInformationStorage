from django.test import TestCase
from storage.models import Page
# Create your tests


class PageModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Page.objects.create(password='12345678', visits_count=0)

    def test_image_label(self):
        page = Page.objects.get(id=1)
        image_label = page._meta.get_field('image').verbose_name
        self.assertEqual(image_label, 'image')

    def test_image_upload_to(self):
        page = Page.objects.get(id=1)
        upload_to = page._meta.get_field('image').upload_to
        self.assertEqual(upload_to, 'images/')

    def test_password_label(self):
        page = Page.objects.get(id=1)
        password_label = page._meta.get_field('password').verbose_name
        self.assertEqual(password_label, 'password')

    def test_password_max_length(self):
        page = Page.objects.get(id=1)
        max_length = page._meta.get_field('password').max_length
        self.assertEqual(max_length, 20)


