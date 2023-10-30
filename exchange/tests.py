import datetime
import json
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from exchange.forms import MeetForm
from exchange.models import Offer, Meet
from manage_user.models import Inventory
from catalog.models import Book

class OfferModelTest(TestCase):
    def setUp(self):
        user1 = User.objects.create(username="user1")
        user2 = User.objects.create(username="user2")
        book = Book.objects.create(
            title="Sample Book",
            rating=4,
            author="Sample Author",
            category="Sample Category",
            image_link="http://sample.com/image.jpg",
            publisher="Sample Publisher",
            description="Sample Description",
            year_of_published=2023,
        )
        inventory1 = Inventory.objects.create(user=user1, book=book, amount=10)
        inventory2 = Inventory.objects.create(user=user2, book=book, amount=5)

    def test_create_offer(self):
        user1 = User.objects.get(username="user1")
        user2 = User.objects.get(username="user2")
        book = Book.objects.get(title="Sample Book")
        offer = Offer.objects.create(
            Username1=user1.username,
            Username2=user2.username,
            Inventory1=[{'book_id': book.id, 'quantity': 3, 'book_title': book.title}],
            Inventory2=[{'book_id': book.id, 'quantity': 2, 'book_title': book.title}],
        )
        self.assertEqual(offer.pk, 1)  # Check if the offer was created successfully

class MeetModelTest(TestCase):
    def setUp(self):
        user1 = User.objects.create(username="user1")
        user2 = User.objects.create(username="user2")
        book = Book.objects.create(
            title="Sample Book",
            rating=4,
            author="Sample Author",
            category="Sample Category",
            image_link="http://sample.com/image.jpg",
            publisher="Sample Publisher",
            description="Sample Description",
            year_of_published=2023,
        )
        inventory1 = Inventory.objects.create(user=user1, book=book, amount=10)
        inventory2 = Inventory.objects.create(user=user2, book=book, amount=5)
        offer = Offer.objects.create(
            Username1=user1.username,
            Username2=user2.username,
            Inventory1=[{'book_id': book.id, 'quantity': 3, 'book_title': book.title}],
            Inventory2=[{'book_id': book.id, 'quantity': 2, 'book_title': book.title}],
        )

    def test_create_meet(self):
        user1 = User.objects.get(username="user1")
        user2 = User.objects.get(username="user2")
        offer = Offer.objects.get(Username1=user1.username, Username2=user2.username)
        meet = Meet.objects.create(
            sender=user1,
            receiver=user2,
            offer=offer,
            date="2023-10-29",
            location="Sample Location",
            message="Sample Message"
        )
        self.assertEqual(meet.pk, 1)  # Check if the meet was created successfully

class OfferUserViewTest(TestCase):
    def test_offer_user_view(self):
        # Create users and inventories for testing
        user1 = User.objects.create_user(username="user1", password="password1")
        user2 = User.objects.create_user(username="user2", password="password2")
        book = Book.objects.create(
            title="Sample Book",
            rating=4,
            author="Sample Author",
            category="Sample Category",
            image_link="http://sample.com/image.jpg",
            publisher="Sample Publisher",
            description="Sample Description",
            year_of_published=2023,
        )
        inventory1 = Inventory.objects.create(user=user1, book=book, amount=10)
        inventory2 = Inventory.objects.create(user=user2, book=book, amount=5)

        # Log in the user1 for testing
        self.client.login(username="user1", password="password1")

        # Test the view with 'user2' as the target username
        response = self.client.get(reverse("offer_user", args=["user2"]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sample Book")

class ShowBooksViewTest(TestCase):
    def setUp(self):
        # Create some sample books
        self.book1 = Book.objects.create(
                        title="Sample Book 1",
                        rating=5,
                        author="New Sample Author",
                        category="New Sample Category",
                        image_link="http://newsample.com/image.jpg",
                        publisher="New Sample Publisher",
                        description="New Sample Description",
                        year_of_published=2024,
                    )
        self.book2 = Book.objects.create(
                        title="Sample Book 2",
                        rating=5,
                        author="New Sample Author",
                        category="New Sample Category",
                        image_link="http://newsample.com/image.jpg",
                        publisher="New Sample Publisher",
                        description="New Sample Description",
                        year_of_published=2024,
                    )
        self.book3 = Book.objects.create(
                        title="Another Book",
                        rating=5,  # Updated rating
                        author="New Sample Author",
                        category="New Sample Category",
                        image_link="http://newsample.com/image.jpg",
                        publisher="New Sample Publisher",
                        description="New Sample Description",
                        year_of_published=2024,
                    )

    def test_show_books_with_query(self):
        # Test the view with a search query
        response = self.client.get(reverse("exchange:show_books") + "?q=Sample")
        self.assertEqual(response.status_code, 200)

        # Check if the expected books are in the response context
        expected_titles = ["Sample Book 1", "Sample Book 2"]
        for book in response.context['books']:
            self.assertIn(book['title'], expected_titles)

    def test_show_books_without_query(self):
        # Test the view without a search query
        response = self.client.get(reverse("exchange:show_books"))
        self.assertEqual(response.status_code, 200)

        # Check if all books are in the response context
        expected_titles = ["Sample Book 1", "Sample Book 2", "Another Book"]
        for book in response.context['books']:
            self.assertIn(book['title'], expected_titles)

class OfferUserViewTest(TestCase):
    def test_offer_user_view(self):
        # Create users and inventories for testing
        user1 = User.objects.create_user(username="user1", password="password1")
        user2 = User.objects.create_user(username="user2", password="password2")
        book = Book.objects.create(
            title="Sample Book",
            rating=4,
            author="Sample Author",
            category="Sample Category",
            image_link="http://sample.com/image.jpg",
            publisher="Sample Publisher",
            description="Sample Description",
            year_of_published=2023,
        )
        inventory1 = Inventory.objects.create(user=user1, book=book, amount=10)
        inventory2 = Inventory.objects.create(user=user2, book=book, amount=5)

        # Log in the user1 for testing
        self.client.login(username="user1", password="password1")

        # Test the view with 'user2' as the target username
        response = self.client.get(reverse("exchange:offer_user", kwargs={"username": "user2"}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sample Book")

class ScheduleMeetViewTest(TestCase):
    def setUp(self):
        # Create users and an offer for testing
        self.user1 = User.objects.create_user(username="user1", password="password1")
        self.user2 = User.objects.create_user(username="user2", password="password2")

        self.offer = Offer.objects.create(
            Username1=self.user1.username,
            Username2=self.user2.username,
            Inventory1="[]",
            Inventory2="[]",
        )

    def test_schedule_meet_view_GET(self):
        # Log in as user1
        self.client.login(username="user1", password="password1")

        # Make a GET request to the schedule_meet view for the offer
        response = self.client.get(reverse('exchange:schedule_meet', args=[self.offer.id]))

        # Check if the response status code is 200, indicating success
        self.assertEqual(response.status_code, 200)

        # Check if the form in the context is an instance of MeetForm
        self.assertIsInstance(response.context['form'], MeetForm)

    def test_schedule_meet_view_POST_valid_form(self):
        # Log in as user1
        self.client.login(username="user1", password="password1")

        # Prepare valid form data
        form_data = {
            'date': '2023-10-29',
            'location': 'Sample Location',
            'message': 'test',
        }

        # Make a POST request to the schedule_meet view with valid form data
        response = self.client.post(reverse('exchange:schedule_meet', args=[self.offer.id]), data=form_data)

        # Check if the response status code is 201, indicating success
        self.assertEqual(response.status_code, 201)

        # Check if the response contains the success message
        self.assertEqual(response.json()['message'], "Successfully Scheduled an Offline Meeting")

    def test_schedule_meet_view_POST_invalid_form(self):
        # Log in as user1
        self.client.login(username="user1", password="password1")

        # Prepare invalid form data (empty data)
        form_data = {}

        # Make a POST request to the schedule_meet view with invalid form data
        response = self.client.post(reverse('exchange:schedule_meet', args=[self.offer.id]), data=form_data)

        # Check if the response status code is 400, indicating a bad request
        self.assertEqual(response.status_code, 400)

        # Check if the response contains the error message
        self.assertEqual(response.json()['message'], "Form is not valid!")

    def test_schedule_meet_view_GET_unauthenticated(self):
        # Make a GET request to the schedule_meet view without authentication
        response = self.client.get(reverse('exchange:schedule_meet', args=[self.offer.id]))

        # Check if the response status code is 302, indicating a redirect to the login page
        self.assertEqual(response.status_code, 302)

    def test_schedule_meet_view_POST_unauthenticated(self):
        # Prepare valid form data
        form_data = {
            'date': '2023-10-29',
            'location': 'Sample Location',
        }

        # Make a POST request to the schedule_meet view with valid form data without authentication
        response = self.client.post(reverse('exchange:schedule_meet', args=[self.offer.id]), data=form_data)

        # Check if the response status code is 302, indicating a redirect to the login page
        self.assertEqual(response.status_code, 302)