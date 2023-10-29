from django.test import TestCase
from django.urls import reverse
from .models import Recommendation
class ViewTest(TestCase):
    def show_main_view(self):
        response = self.client.get(reverse('recommendation:show_main'))

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'show_main.html')

    def show_recommendation_view(self):
        response = self.client.get(reverse('recommendation:show_recommendation'))
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'show_recommendation.html')

class RecommendationJsonViewTest(TestCase):
    def setUp(self):
        Recommendation.objects.create(
            book_title='Test Book 1',
            another_book_title='Test Book 2',
            book_id=1,
            another_book_id=2,
            recommender_name='Test User',
            recommendation_scale=5,
            description='This is a test recommendation.',
        )

    def test_get_recommendation_json_view(self):
        response = self.client.get(reverse('recommendation:get_recommendation_json'))

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Test Book 1')
        self.assertContains(response, 'Test Book 2')
        self.assertContains(response, 'Test User')
        self.assertContains(response, 'This is a test recommendation.')