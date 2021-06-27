from django.test import TestCase
from storage.models import Page
from storage.views import create_url
from django.core.files.images import ImageFile


class IndexViewTest(TestCase):

    def test_index_view_url(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_page_creation(self):
        response = self.client.post('', data={'text_information': 'abc'})
        self.assertTrue('url' in response.context)
        self.assertTrue('password' in response.context)

    def test_page_wrong_creation(self):
        response = self.client.post('', data={'text_information': ''})
        self.assertFalse('url' in response.context)
        self.assertFalse('password' in response.context)


class PageViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Page.objects.create(image=ImageFile(file=None), password='12345', visits_count=0)

    def test_page_id_1_view_url(self):
        url = create_url(1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_page_id_1_right_password_validation(self):
        url = create_url(1)
        response = self.client.post(url, data={'password': '12345'})
        self.assertTrue('page' in response.context)
        self.assertTrue('visits' in response.context)
        self.assertFalse('form' in response.context)
        self.assertFalse('message' in response.context)

    def test_page_id_1_wrong_password_validation(self):
        url = create_url(1)
        response = self.client.post(url, data={'password': '54321'})
        self.assertFalse('page' in response.context)
        self.assertFalse('visits' in response.context)
        self.assertTrue('form' in response.context)
        self.assertTrue('message' in response.context)
