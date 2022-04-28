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


class ProductCondition(enum.Enum):
    Used = 1,
    New = 2


class VehicleDocument(object):
    def __init__(self):
        self.__issuer: str = ''
        self.__doc_id: str = ''


class CarListing(object):
    def __init__(self, car_status: ProductCondition):
        self.__listing_car: Car = None
        self.__car_condition = car_status
        self.__docs: List[VehicleDocument] = []
        self.__price: float = 0.0


class SparePartListing(object):
    def __init__(self, part: SparePart, part_status: ProductCondition):
        self.__listing_part = part
        self.__condition = part_status
        self.__price: float = 0.0


class PaymentType(enum.Enum):
    Cash = 1,
    Debit = 2,
    Credit = 3


class TransactionType(enum.Enum):
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


class Review(object):
    def __init__(self, text, num_stars, review_writer):
        self.__text: str = text
        self.__start: int = num_stars
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
        self.__car_details: Car = None
        self.__legal_documents: List[VehicleDocument] = []
        self.__transaction_id: int = 0
        self.__dealerships: DealershipStore = None


class InsurancePlan(object):
    def __init__(self, ins_code):
        self.__transaction_code: str = ins_code
        self.__price: float = 0.0
        self.__car_details: Car = None


class CarCompanies(enum.Enum):
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
        self.__car_companies = specific_comp


class DealershipStore(object):
    def __init__(self):
        self.__location: Location = None
        self.__email: str = ''
        self.__telephone: str = ''
        self.__store_name: str = ''
        self.__store_owner: str = ''

class TestDrive(object):
    def __init__(self,lst_code):
        self.__listings_id: str = lst_code
        self.__date: datetime = None
        self.__time: Time = None
        self.__listing_car: Car = None

class Message(object):
    def __init__(self):
        self.__message: str = ''
        self.__sender_name: str = ''

class Transporter(object):
    def __init__(self):
        self.__firstname: str = ''
        self.__lastname: str = ''
        self.__email: str = ''
        self.__location: Location = None

class Transportation_type(enum.Enum):
    express = 1,
    normal = 2
   
class CarTransportation(object):
    def __init__(self,trs_code,trs_method: Transportation_type):
        self.__transaction_code: str = trs_code
        self.__location: Location = None
        self.__transportation_method = trs_method
        self.__transporter_details: Transporter = None
        self.car_details: Car = None
        self.__delivery_point: str = ''
        self.__transportation_time: datetime = None