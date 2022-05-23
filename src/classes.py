import enum  # for enumerations
import datetime  # for dates
from typing import List, Tuple


class User(object):
    def __init__(self):
        self.__first_name: str = ''
        self.__last_name: str = ''
        self.__username: str = ''
        self.__user_id: int = 0
        self.__email: str = ''
        self.__telephone: str = ''
        self.__reg_date: datetime.date = datetime.date.today()

    def set_first_name(self, new_first_name):
        self.__first_name = new_first_name

    def get_first_name(self):
        return self.__first_name

    def set_last_name(self, new_last_name):
        self.__last_name = new_last_name

    def get_last_name(self):
        return self.__last_name

    def set_username(self, new_username):
        self.__username = new_username

    def get_first_name(self):
        return self.__username

    def set_email(self, new_email):
        self.__email = new_email

    def get_email(self):
        return self.__email

    def set_telephone(self, new_telephone):
        self.__telephone = new_telephone

    def get_telephone(self):
        return self.__telephone


class CarTransmission(enum.Enum):  # transmission type enum
    Manual = 1,
    Automatic = 2


class CarFuel(enum.Enum):  # fuel type enum
    Diesel = 1,
    Gas = 2,
    Petrol = 3,
    Electric = 4,
    Hybrid = 5


class Car(object):
    def __init__(self, transmission_type: CarTransmission, fuel_type: CarFuel):
        self.__company: str = ''
        self.__model: str = ''
        self.__category: str = ''
        self.__release_year: int = 0
        self.__mileage: int = 0
        self.__engine: int = 0
        self.__power: int = 0
        self.__transmission = transmission_type
        self.__fuel_type = fuel_type
        self.__city_consumption: int = 0
        self.__motorway_consumption: int = 0
        self.__color: str = ''
        self.__interior_color: str = ''
        self.__num_doors: int = 0
        self.__registration_plate: str = ''

    def set_car_info(self,new_company,new_model,new_category,new_release_year,new_mileage,new_engine,new_power,new_transmission,new_fuel_type,new_city_consumption,new_motorway_consumption,new_color,new_interior_color,new_num_doors,new_registration_plate):
        self.__company = new_company
        self.__model = new_model
        self.__category = new_category
        self.__release_year = new_release_year
        self.__mileage = new_mileage
        self.__engine = new_engine
        self.__power = new_power
        self.__transmission = new_transmission
        self.__fuel_type = new_fuel_type
        self.__city_consumption = new_city_consumption
        self.__motorway_consumption = new_motorway_consumption
        self.__color = new_color
        self.__interior_color = new_interior_color
        self.__num_doors = new_num_doors
        self.__registration_plate = new_registration_plate

    def get_spare_part_info(self):
        return self.__company
        return self.__model
        return self.__category
        return self.__release_year
        return self.__mileage
        return self.__engine
        return self.__power
        return self.__transmission
        return self.__fuel_type
        return self.__city_consumption
        return self.__motorway_consumption
        return self.__color
        return self.__interior_color
        return self.__num_doors
        return self.__registration_plate
    

class SparePart(object):
    def __init__(self):
        self.__brand: str = ''
        self.__type: str = ''
        self.__category: str = ''
        self.__number: str = ''

    def set_spare_part_info(self,new_brand,new_type,new_number):
        self.__brand = new_brand
        self.__type = new_type
        self.__number = new_number

    def get_spare_part_info(self):
        return self.__brand
        return self.__type
        return self.__number

    def set_spare_part_category(self, new_category):
        self.__category = new_category

    def get_spare_part_category(self):
        return self.__category


class Listing(object):
    def __init__(self):
        self.__id: int = 0
        self.__title: str = ''
        self.__description: str = ''
        self.__publish_date: datetime = None
        self.__creator: User = None
        self.__location: Location = None
        self.__photos: List[Photograph] = []

    def set_listing_title(self, new_title):
        self.__title = new_title

    def get_listing_title(self):
        return self.__title

    def set_photos(self, new_photos):
        self.__photos = new_photos

    def get_photos(self):
        return self.__photos

    def set_description(self, new_description):
        self.__description = new_description

    def get_description(self):
        return self.__description


class ProductCondition(enum.Enum):   # product condition enum
    Used = 1,
    New = 2


class CarDocument(object):            
    def __init__(self):
        self.__issuer: str = ''
        self.__doc_id: str = ''      #setters/getters?


class CarListing(Listing):
    def __init__(self, car_status: ProductCondition):
        self.__vehicle: Car = None
        self.__car_condition = car_status
        self.__docs: List[VehicleDocument] = []
        self.__price: float = 0.0

    def set_car(self, new_car):
        self.__vehicle = new_car

class CarListingsStatisticsLog(object):
    def __init__(self):
        self.__search_log: List[CarSearch] = []
        self.__comparison_log: List[CarComparison] = []
        self.__popular_listings: List[CarListing] = []

    def get_popular_cars(self,CarListing):         #needs corrections
        return self.CarListing.__popular_listings


class SparePartListing(Listing):
    def __init__(self, part: SparePart, part_status: ProductCondition):
        self.__listing_part = part
        self.__condition = part_status
        self.__price: float = 0.0

    def set_spare_part(self, new_spare_part):
        self.__spare_part = new_spare_part


class PaymentType(enum.Enum):    #payment type enum
    Cash = 1,
    Debit = 2,
    Credit = 3


class TransactionType(enum.Enum):       #transaction type enum
    Payment = 1,
    Exchange = 2,
    Transfer = 3


class Transaction(object):
    def __init__(self, payment_type: PaymentType, transaction_purpose: TransactionType):
        self.__id: str = ''
        self.__timestamp: datetime = None
        self.__payment_method = payment_type
        self.__amount: float = 0.0
        self.__type = transaction_purpose
        self.__customer: User = None
        self.__merchant: User = None
        self.__product_id: int = 0

    def get_transaction_info(self):
        return self.__id
        return self.__timestamp
        return self.__payment_method
        return self.__type
        return self.__customer
        return self.__merchant
        return self.__product_id

class TransactionLog(object):
    def __init__(self):
        self.__name: str = ''
        self.__ttransaction_list: List[Transaction] = [] 

class Invoice(object):
    def __init__(self):
        self.transaction: Transaction = None
        self.__invoice_code: int = 0
        self.__text: str = ''
        self._recipient_email: str = ''

    def get_invoice(self,Transaction):
        return self.Transaction.__transaction
        return self.__invoice_code
        return self.__text
        return self.__recipient_email

class Review(object):
    def __init__(self, text, num_stars, review_writer):
        self.__text: str = text
        self.__stars: int = num_stars
        self.__writer: User = review_writer

    def set_review_info(self, new_text,new_stars,new_writer,new_creation_date):
        self.__text = new_text
        self.__stars = new_stars
        self.__writer = new_writer
        self.__creation_date = new_creation_date

    def get_review(self,User,Date):
        return self.__text
        return self.__stars
        return self.User.__writer
        return self.Date.__creation_date


class Location(object):
    def __init__(self, location_coordinates: Tuple[float, float]):
        self.__coordinates: Tuple[float, float] = location_coordinates

    def set_location(self,new_coordinates):
        self.__coordinates = new_coordinates

    def get_location(self):
        return self.__coordinates

class Photograph(object):
    def __init__(self, photo_file_name, photo_size):
        self.__file_name: str = photo_file_name
        self.__size: int = photo_size


class CarExchange(object):
    def __init__(self):
        self.__vehicle: Car = None
        self.__car_owner: User = None
        self.__exchange_reward: float = 0.0
        self.__legal_documents: List[VehicleDocument] = []
        self.__transaction: Transaction = None
        self.__dealerships: DealershipStore = None
        self.__chosen_store: DealershipStore = None

    def get_dealerships(self,DealershipStore):
        return self.DealershipStore.__dealerships

    def set_car_info(self,new_vehicle):
        self.__vehicle = new_vehicle

    def set_docs(self,new_docs):
        self.__legal_documents = new_docs

class InsurancePlan(object):
    def __init__(self, ins_code):
        self.__transaction_code: str = ins_code
        self.__price: float = 0.0
        self.__car_details: Car = None


class CarCompanies(enum.Enum):      #companies enum
    Alfa_Romeo = 1,
    Audi = 2,
    BMW = 3,
    Chevrolet = 4,
    Citroen = 5,
    Dodge = 6,
    Ferrari = 7,
    Ford = 8,
    Hyundai = 9,
    Jaguar = 10,
    Mazda = 11,
    Mercedes_Benz = 12,
    Mitsubishi = 13,
    Nissan = 14,
    Opel = 15,
    Peugeot = 16,
    Porsche = 17,
    Subaru = 18,
    Toyota = 19,
    Volkswagen = 20,
    Volvo = 21,


class Dealership(object):
    def __init__(self, specific_comp: CarCompanies):
        self.__dealership_name: str = ''
        self.__tax_ID: int = 0
        self.__stores: List[DealershipStore] = []
        self.__car_companies = specific_comp


class DealershipStore(object):
    def __init__(self):
        self.__location: Location = None
        self.__email: str = ''
        self.__telephone: str = ''
        self.__store_name: str = ''
        self.__store_owner: str = ''
        self.__cars_list: List[Car] = []

    def get_store(self):
        return self.Location.__location
        return self.__store_name

    def set_store_info(self,new_location,new_email,new_telephone,new_store_name,new_store_owner):
        self.__location = new_location
        self.__email = new_email
        self.__telephne = new_telephone
        self.__store_name = new_store_name
        self.__store_owner = new_store_owner

class TestDrive(object):
    def __init__(self,lst_code):
        self.__listings_id: str = lst_code
        self.__date: datetime = None
   #     self.__time: Time = None
        self.__user: User = None

    def set_test_drive_info(self,new_listing,new_date,new_user):
        self.__listing = new_listing
        self.__date = new_date
        self.__user = new_user

class Message(object):
    def __init__(self):
        self.__message: str = ''
        self.__sender_name: str = ''

    def set_message_info(self,new_sender,new_recipient,new_text,new_timestamp):
        self.__sender = new_sender
        self.__recipient = new_recipient
        self.__text = new_text
        self.__creation_timestamp = new_timestamp

    def get_message(self,User):
        return self.User.__sender
        return self.User.__recipient
        return self.__text

class Transporter(object):
    def __init__(self):
        self.__transporter_id: int = 0
        #self.__firstname: str = ''
        #self.__lastname: str = ''
        #self.__email: str = ''
        self.__location: Location = None
        self.__trasportations_list: List[CarTransportation] = []

    def get_message(self,CarTransportation):
        return self.__transporter_id
        return self.__location
        return self.CarTransportation.__transportations_list

class Transportation_type(enum.Enum):       #transportation type enum
    express = 1,
    standard = 2

class Transportation_status(enum.Enum):     #transportation status enum
    Pending = 1,
    Ongoing = 2,
    Completed = 3
   
class CarTransportation(object):
    def __init__(self,trs_status: Transportation_status,trs_method: Transportation_type):
        self.__transaction: Transaction = None
        self.__delivery_location: Location = None
        self.__transportation_status = trs_status
        self.__transportation_method = trs_method
        self.__transporter: Transporter = None
        self.__vehicle: Car = None
        self.__transportation_time: datetime = None

    def set_transportation_info(self,new_delivery_location,new_status,new_package,new_transporter,new_vehicle,new_transportation_time):
        self.__delivery_location = new_delivery_location
        self.__status = new_status
        self.__package = new_package
        self.__transporter = new_transporter
        self.__vehicle= new_vehicle
        self.__transportation_time = new_transportation_time


class CarComparison(object):
    def __init__(self):
        self.__car_listings: List[CarListing] = []
        self.__criteria: List[str]= []
        self.__price_range: float = (0.0,0.0) # have not checked for this
        self.__comp_results: List[Car] = []
        self.__recommended_car: Car = None

class CarSearch(object):
    def __init__(self,srch_rad):
        self.__search_results: List[CarListing] = []
        self.__criteria: List[str]= []
        self.__location: Location = None
        self.__search_radius: int = srch_rad
        self.__price_range: float = (0.0,0.0) # have not checked for this

class MonthlyInstallment(object):
    def __init__(self):
        self.__transaction: Transaction = None
        self.__price: float = 0.0
        self.__due_date: datetime = None

    def set_installment_price(self,new_price):
        self.__price = new_price

    def get_installment_info(self,Transaction,Date):
        return self.Transaction.__transaction
        return self.__price
        return self.Date.__due_date


class PushNotification(object):
    def __init__(self):
        self.__creator: User = None
        self.__text: str = ''
        self.__issue_time: datetime = None
        self.__recipients: List[User] = []

class ListingDeletionForm(object):
    def __init__(self):
        self.__listing_report: ListingReport = None
        self.__text: str = ''
        self.__creation_date: datetime.date = datetime.date.today()

