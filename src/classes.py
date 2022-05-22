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
        self.category: str = ''
        self.__release_year: int = 0
        self.__mileage: int = 0
        self.__engine: int = 0
        self.__power: int = 0
        self.__transmission = transmission_type
        self.__fuel_type = fuel_type
        self.__city_consumption: int = 0
        self.__motorway_consumption: int = 0
        self.__color: str = ''
        self._interior_color: str = ''
        self.__num_doors: int = 0
        self.__registration_plate: str = ''


class SparePart(object):
    def __init__(self):
        self.__brand: str = ''
        self.__type: str = ''
        self.__category: str = ''
        self.__number: str = ''


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


class ProductCondition(enum.Enum):   # product condition enum
    Used = 1,
    New = 2


class VehicleDocument(object):            
    def __init__(self):
        self.__issuer: str = ''
        self.__doc_id: str = ''


class CarListing(Listing):
    def __init__(self, car_status: ProductCondition):
        self.__vehicle: Car = None
        self.__car_condition = car_status
        self.__docs: List[VehicleDocument] = []
        self.__price: float = 0.0

class CarListingStatisticsLog(object):
    def __init__(self):
        self.__search_log: List[CarSearch] = []
        self.__comparison_log: List[CarComparison] = []
        self.__popular_listings: List[CarListing] = []


class SparePartListing(Listing):
    def __init__(self, part: SparePart, part_status: ProductCondition):
        self.__listing_part = part
        self.__condition = part_status
        self.__price: float = 0.0


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

class Review(object):
    def __init__(self, text, num_stars, review_writer):
        self.__text: str = text
        self.__stars: int = num_stars
        self.__writer: User = review_writer


class Location(object):
    def __init__(self, location_coordinates: Tuple[float, float]):
        self.__coordinates: Tuple[float, float] = location_coordinates


class Photograph(object):
    def __init__(self, photo_file_name, photo_size):
        self.__file_name: str = photo_file_name
        self.__size: int = photo_size


class CarExchange(object):
    def __init__(self):
        self.__vehiicle: Car = None
        self.__car_owner: User = None
        self.__exchange_reward: float = 0.0
        self.__legal_documents: List[VehicleDocument] = []
        self.__transaction: Transaction = None
        self.__dealerships: DealershipStore = None
        self.__chosen_store: DealershipStore = None


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

class TestDrive(object):
    def __init__(self,lst_code):
        self.__listings_id: str = lst_code
        self.__date: datetime = None
   #     self.__time: Time = None
        self.__user: User = None

class Message(object):
    def __init__(self):
        self.__message: str = ''
        self.__sender_name: str = ''

class Transporter(object):
    def __init__(self):
        self.__transporter_id: int = 0
        #self.__firstname: str = ''
        #self.__lastname: str = ''
        #self.__email: str = ''
        self.__location: Location = None
        self.__trasportations_list: List[CarTransportation] = []

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

