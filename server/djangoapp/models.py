from django.db import models
from django.utils.timezone import now


# Create your models here.
SEDAN = "Sedan"
SUV = "SUV"
WAGON = "WAGON"
CAR_TYPES = ((SEDAN, "Sedan"), (SUV, "SUV"), (WAGON, "WAGON"))

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(null=False, max_length=40)
    description = models.CharField(max_length=500)
    
    # Create a toString method for object string representation
    def __str__(self):
        return self.name


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(null=False, max_length=40)
    dealer_id = models.IntegerField()
    car_type = models.CharField(choices=CAR_TYPES, max_length=30)
    year = models.DateField()
    
    # Create a toString method for object string representation
    def __str__(self):
        return self.name


# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer():
    id = None
    city = None
    state = None
    st = None
    address = None
    zip = None
    lat = None
    long = None
    short_name = None
    full_name = None
    def __init__(self, address, city, state, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer state
        self.state = state
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip
    def from_json(j):
        self.id = j["id"]
        self.city = j["city"]
        self.state = j["state"]
        self.st = j["st"]
        self.address = j["address"]
        self.zip = j["zip"]
        self.lat = j["lat"]
        self.long = j["long"]
        self.short_name = j["short_name"]
        self.full_name = j["full_name"]
    def __str__(self):
        return "Dealer name: " + self.full_name


# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview():
    car_make = None#
    car_model = None#
    car_year = None#
    dealership = None#
    id = None#
    name = None#
    purchase = None#
    purchase_date = None#
    review = None#
    sentiment = None#
    def __init__(self, car_make, car_model, car_year, dealership, id, name, purchase, 
                purchase_date, review, sentiment=""
                ):
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.dealership = dealership
        self.id = id
        self.name = name
        self.purchase = purchase
        self.purchase_date = purchase_date
        self.review = review
        self.sentiment = sentiment
    def from_json(j):
        self.car_make = j["car_make"]
        self.car_model = j["car_model"]
        self.car_year = j["car_year"]
        self.dealership = j["dealership"]
        self.id = j["id"]
        self.name = j["name"]
        self.purchase = j["purchase"]
        self.purchase_date = j["purchase_date"]
        self.review = j["review"]
    def __str__(self):
        return self.review
