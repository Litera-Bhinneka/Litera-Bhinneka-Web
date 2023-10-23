from csv import DictReader
from django.core.management import BaseCommand

# Import the model 
from catalog.models import Book


ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the book catalog data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from dataset/book_sampled.csv"

    def handle(self, *args, **options):
    
        # Show this if the data already exist in the database
        if Book.objects.exists():
            print('book catalog data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return
            
        # Show this before loading the data into the database
        print("Loading book catalog data")

        #Code to load the data into database
        FILE_PATH = "dataset/book_sampled.csv"
        for row in DictReader(open(FILE_PATH)):
            book = Book(title = row['title'],
                        rating = row['rating'],
                        author = row['author'],
                        category = row['category'],
                        image_link = row['image_link'],
                        info_link = row['info_link'],
                        publisher = row['publisher'],
                        description = row['description'],
                        preview_link = row['preview_link'],
                        year_of_published = row['published_date'])  
            book.save()