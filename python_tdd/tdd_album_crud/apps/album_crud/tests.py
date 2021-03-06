from django.test import TestCase, Client
from .models import *

class AlbumTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Album.objects.create(title = 'The Battle of Los Angeles', artist = 'Rage Against the Machine', year = 1999)

    # urls test
    def test_urls(self):
        c = Client()
        res = c.get('/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(c.get('/create').status_code, 302)
        self.assertEqual(c.get('/read').status_code, 200)

    def test_model_creation(self):
        a = Album.objects.create(title = 'License to Ill', artist = 'Beastie Boys', year = 1986)
        self.assertEqual(a.title, 'License to Ill')
        self.assertEqual(a.artist, 'Beastie Boys')
        self.assertEqual(a.year, 1986)

    def test_model_get(self):
        # album = Album.objects.get(id = 1)
        albums = Album.objects.all()
        for elem in albums:
            self.assertEqual(elem.artist, 'Rage Against the Machine')

    def test_model_edit(self):
        a = Album.objects.first()
        a.title = 'Enter the Wu-Tang'
        a.artist = 'Wu-Tang Clan'
        a.year = 1993
        a.save()
        edited_a = Album.objects.first()
        # print(a.artist)
        self.assertEqual(edited_a.title, 'Enter the Wu-Tang')
        self.assertEqual(edited_a.artist, 'Wu-Tang Clan')
        self.assertEqual(edited_a.year, 1993)
    
    def test_model_delete(self):
        # Note: Delete will return a tuple that holds the number of entities deleted in the 0 index
        num_deleted = Album.objects.get(id = 1).delete()[0]
        self.assertEqual(num_deleted, 1)

    def test_view_create(self):
        # First, we make a POST request to the server. We can send a dictionary of POST data
        c = Client()
        post_data = {
            'title': '8',
            'artist' : 'Incubus',
            'year': 2017
        }
        response = c.post('/create', post_data)
        # We also want to test to make sure that the view function did actually redirect as we wanted
        self.assertEqual(response.status_code, 302)
        new_album = Album.objects.last()
        # print(new_album.artist)
        self.assertEqual(new_album.title, post_data['title'])
        self.assertEqual(new_album.artist, post_data['artist'])
        self.assertEqual(new_album.year, post_data['year'])

    def test_view_read(self):
        c = Client()
        response = c.get('/read')
        self.assertEqual(response.status_code, 200)

    def test_view_update(self):
        ## For this one, we have given you a good jumping off point, but it's still
        ## up to you to create the url and the view function to make this test pass
        c = Client()
        post_data = {
            "title": "A Test Edit",
            "artist" : "Test Artist Edit",
            "year": 3099
        }
        # This should edit the single album that is created by our setUp method
        response = c.post('/update/1', post_data)
        # Let's make sure the view function eventually redirects
        self.assertEqual(response.status_code, 302)
        # Let's test to make sure the edit worked
        edited = Album.objects.get(id = 1)
        self.assertEqual(edited.title, post_data['title'])
        self.assertEqual(edited.artist, post_data['artist'])
        self.assertEqual(edited.year, post_data['year'])

    def test_view_delete(self):
        c = Client()
        res = c.post('/delete/1')
        self.assertEqual(res.status_code, 302)