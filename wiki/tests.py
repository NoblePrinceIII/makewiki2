import unittest
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from wiki.models import Page


class wikiTestCase(TestCase):
    def test_true_is_true(self):
        """Tests that True equals True"""
        self.assertEqual(True, True)

    def test_page_slugify_on_save(self):
        """Test the slug generated when saving a Page."""
        #Create a user to properly test code
        user = User()
        user.save()
        
        page = Page(title="My Test Page", content="test", author=user)
        page.save()
        
        self.assertEqual(page.slug, 'my-test-page')
    
class PageListView_Test(TestCase):
    """Tests that the homepage works."""
    def test_multiple_pages(self):
        user = User.objects.create()

        Page.objects.create(title="My Test Page", content="test", author=user)
        Page.objects.create(title="My Test Page 2", content="test", author=user)

        response = self.client.get('/')
    
        self.assertEqual(response.status_code, 200)

        responses = response.context['pages']
        self.assertEqual(len(responses), 2)

        self.assertQuerysetEqual(
            responses,
            ['<Page: My Test Page>', '<Page: My Test Page 2>'],
            ordered=False
        )
    
class PageDetailView_Test(TestCase):
    """Tests that the Detail Page works."""
    def test_detail_page(self):
        #Create a user for this test 
        user = User.objects.create()

        #Create a page to the database 
        Page.objects.create(title="My Test Page", content="test", author=user)
        

        #Make a GET request, and test route returns 200
        reponse = self.client.get("/my-test-page/")

        self.assertEqual(reponse.status_code, 200)