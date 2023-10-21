from csv import DictReader
from django.core.management import BaseCommand

# Import the model 
from review.models import Review


ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the review data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from dataset/rating_sampled.csv"

    def handle(self, *args, **options):
    
        # Show this if the data already exist in the database
        if Review.objects.exists():
            print('review data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return
            
        # Show this before loading the data into the database
        print("Loading review data")

        #Code to load the data into database
        FILE_PATH = "dataset/rating_sampled.csv"
        for row in DictReader(open(FILE_PATH)):
            review=Review(book_title=row['book_title'], 
                          reviewer_name=row['reviewer_name'], 
                          review_score=row['review_score'],
                          review_summary=row['review_summary'],
                          review_text=row['review_text'],
                          review_date=row['review_date'])  
            review.save()