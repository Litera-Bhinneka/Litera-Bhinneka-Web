from django.test import TestCase
from review.models import Review

class ReviewModelTest(TestCase):
    def setUp(self):
        Review.objects.create(
            book_title="Test Book",
            reviewer_name="Test Reviewer",
            review_score=5,
            review_summary="Test Summary",
            review_text="Test Review Text"
        )

    def test_review_attributes(self):
        review = Review.objects.get(book_title="Test Book")
        self.assertEqual(review.reviewer_name, "Test Reviewer")
        self.assertEqual(review.review_score, 5)
        self.assertEqual(review.review_summary, "Test Summary")
        self.assertEqual(review.review_text, "Test Review Text")
        self.assertIsNotNone(review.review_date)

    def test_review_str_method(self):
        review = Review.objects.get(book_title="Test Book").review_text
        self.assertEqual(str(review), "Test Review Text")
