from django.test import TestCase, Client

class HomepageTest(TestCase):
    def test_main_url_is_exist(self):
        response = Client().get('/home/')
        self.assertEqual(response.status_code, 200)

    def test_main_using_main_template(self):
        response = Client().get('/home/')
        self.assertTemplateUsed(response, 'homepage.html')