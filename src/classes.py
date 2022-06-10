import enum  # for enumerations
import datetime  # for dates
from dateutil.relativedelta import relativedelta
from typing import List, Tuple
import random
import string
import re

#################### "database" ###########################################

# The following lists model the behavior of the equivalent database tables, therefore they are used
# as the application's backend
system_posted_listings = []  # contains all the posted listings

system_registered_listing_reports = []  # contains all the ListingReports

system_scheduled_test_drives = []  # contains all the scheduled TestDrive appointments
system_scheduled_car_inspections = []  # contains all the scheduled CarInspection appointments
system_scheduled_car_transportations = []  # contains all the scheduled CarTransportations

system_registered_stores = []  # contains all the registered dealership stores
system_registered_dealerships = []  # contains all the registered Dealerships (type of User)
system_registered_users = []  # contains all the system's registered Users

system_registered_cars = []  # contains all the cars


###########################################################################

##################### USER types ##########################################
class User(object):
    def __init__(self):
        self.__first_name: str = ''
        self.__last_name: str = ''
        self.__username: str = ''
        self.__user_id: int = random.randint(0, 1000)  # assume that user IDs are within this range
        self.__email: str = ''
        self.__telephone: str = ''
        self.__reg_date: datetime.date = datetime.date.today()
        self.__listings: List["Listing"] = []
        self.__car_purchases: List["Car"] = []
        self.__points: int = 0
        self.__reviews: List["Review"] = []

    def set_name(self, first_name, last_name):
        self.__first_name = first_name
        self.__last_name = last_name

    def get_name(self):
        return self.__first_name + ' ' + self.__last_name

    def set_username(self, new_username):
        self.__username = new_username

    def get_username(self):
        return self.__username

    def set_email(self, new_email):
        self.__email = new_email

    def get_email(self):
        return self.__email

    def set_telephone(self, new_telephone):
        if len(new_telephone) == 10:
            self.__telephone = new_telephone
        else:
            raise Exception('Phone number must be 10 digits')

    def get_telephone(self):
        return self.__telephone

    def get_user_listings(self) -> List["Listing"]:
        return self.__listings

    def add_user_review(self, new_review):
        if new_review not in self.__reviews:
            self.__reviews.append(new_review)

    def get_reviews_list(self) -> List["Review"]:
        return self.__reviews

    def add_listing(self, new_lst) -> bool:
        if new_lst not in self.__listings:  # check if listing does not exist in the user's list
            self.__listings.append(new_lst)
            return True
        else:
            return False

    def delete_listing(self, del_lst) -> bool:
        if del_lst in self.__listings:  # check if listing exists in the user's list
            self.__listings.remove(del_lst)
            return True
        else:
            return False

    def get_car_purchase_history(self) -> List["Car"]:
        return self.__car_purchases

    def get_points(self):
        return self.__points

    def set_points(self, new_amount):
        self.__points = new_amount

    def redeem_points(self, amount) -> bool:
        if self.__points >= amount:  # check if the user has at least as many points as the amount to redeem
            self.__points -= amount  # redeem the user's points
            return True
        else:
            return False

    def get_user_info(self):
        user_info = [self.__first_name, self.__last_name, self.__username,
                     self.__user_id, self.__email, self.__telephone,
                     str(self.__reg_date), self.__listings, self.__car_purchases,
                     self.__points]
        return user_info

    def add_purchased_car(self, new_car):
        if new_car not in self.__car_purchases:  # if car is not already in the user's purchase history
            self.__car_purchases.append(new_car)


class Transporter(User):
    def __init__(self, location):
        super(Transporter, self).__init__()
        self.__transporter_id: int = random.randint(2000, 4000)  # assume transporter IDs are within this range
        self.__location: Location = location
        self.__pending_transportations: List["CarTransportation"] = []
        self.__completed_transportations: List["CarTransportation"] = []

    def get_transporter_info(self) -> List:
        transporter_info = self.get_user_info()
        transporter_info.append(self.__transporter_id)
        transporter_info.append(self.__location.get_location())
        transporter_info.append(self.__pending_transportations)
        transporter_info.append(self.__completed_transportations)
        return transporter_info

    def get_transporter_location(self) -> "Location":
        return self.__location

    def add_transportation(self, new_transportation) -> bool:
        # add the transportation only if it's not already in the list and
        # if the transporter has less than 10 transportations (assuming that each transporter can have at most
        # 10 pending transportations)
        if new_transportation not in self.__pending_transportations and len(self.__pending_transportations) < 10:
            self.__pending_transportations.append(new_transportation)
            new_transportation.start_car_transportation()  # set status to 'Ongoing'
            return True

        return False

    def complete_transportation(self, completed_transportation):
        if completed_transportation not in self.__completed_transportations:
            self.__completed_transportations.append(completed_transportation)
            completed_transportation.finish_car_transportation()  # set status to 'Completed'


class Inspector(User):
    def __init__(self, location):
        super(Inspector, self).__init__()
        self.__inspector_id: int = random.randint(6000, 8000)  # assume inspector IDs are within this range
        self.__location = location
        self.__pending_inspections: List["CarInspection"] = []
        self.__completed_inspections: List["CarInspection"] = []

    def get_inspector_info(self) -> List:
        inspector_info = self.get_user_info()
        inspector_info.append(self.__inspector_id)
        inspector_info.append(self.__location.get_location())
        inspector_info.append(self.__pending_inspections)
        inspector_info.append(self.__completed_inspections)
        return inspector_info

    def get_inspector_location(self) -> "Location":
        return self.__location

    def add_inspection(self, new_inspection) -> bool:
        # add the inspection only if it's not already in the list and
        # if the Inspector has less than 10 inspections (assuming that each inspector can have at most
        # 10 pending car inspections)
        if new_inspection not in self.__pending_inspections and len(self.__pending_inspections) < 10:
            self.__pending_inspections.append(new_inspection)
            new_inspection.start_car_inspection()  # set status to 'Ongoing'
            return True

        return False

    def complete_inspection(self, completed_inspection):
        if completed_inspection not in self.__completed_inspections:
            self.__completed_inspections.append(completed_inspection)
            completed_inspection.finish_car_inspection()  # set status to 'Completed'


class InsuranceCompanyEmployee(User):
    def __init__(self):
        super(InsuranceCompanyEmployee, self).__init__()
        self.__employee_id: int = random.randint(60000, 65000)  # assume employee IDs are within this range
        self.__job_title: str = ''
        self.__company_position: str = ''

    def set_job_info(self, title, position):
        self.__job_title = title
        self.__company_position = position

    def get_ins_company_employee_info(self) -> List:
        employee_info = super().get_user_info()
        employee_info.append(self.__employee_id)
        employee_info.append(self.__job_title)
        employee_info.append(self.__company_position)
        return employee_info


class Dealership(User):
    def __init__(self, name):
        super(Dealership, self).__init__()
        self.__dealership_name: str = name
        self.__tax_ID: int = random.randint(8001, 10000)  # assume Dealership IDs are within this range
        self.__stores: List["DealershipStore"] = []
        self.__car_companies: CarCompanies

    def add_store(self, new_store):
        if new_store not in self.__stores:  # if store is not already added
            self.__stores.append(new_store)

    def register_company(self) -> bool:
        if self not in system_registered_dealerships:  # if not already registered
            system_registered_dealerships.append(self)
            return True  # registration success

        return False

    def is_company_registered(self) -> bool:
        if self in system_registered_dealerships:
            return True  # company is already registered

        return False


##################### END USER types ##########################################

class DealershipStore(object):
    def __init__(self):
        self.__location: Location = None
        self.__email: str = ''
        self.__telephone: str = ''
        self.__store_name: str = ''
        self.__store_owner: str = ''
        self.__cars_list: List["Car"] = []

    def get_store_info(self) -> List:
        store_details = [self.__location, self.__email, self.__telephone,
                         self.__store_name, self.__store_owner, self.__cars_list]
        return store_details

    def get_store(self):
        return self

    def set_store_info(self, new_location, new_email, new_telephone, new_store_owner):
        self.__location = new_location
        self.__email = new_email
        self.__telephone = new_telephone
        self.__store_owner = new_store_owner

    def set_store_name(self, title):
        self.__store_name = title

    def set_store_cars_list(self, cars_list):
        self.__cars_list = cars_list

    def get_cars_list(self):
        return self.__cars_list

    def register_store(self) -> bool:
        if self not in system_registered_stores:  # if store is not already in the "DB"
            system_registered_stores.append(self)
            return True  # registration success

        return False

    def is_store_registered(self) -> bool:
        if self in system_registered_stores:
            return True

        return False


class Wishlist(object):
    def __init__(self, owner):
        self.__owner: User = owner
        self.__car_list: List["Car"] = []

    def add_car(self, new_car):
        if new_car not in self.__car_list:
            self.__car_list.append(new_car)

    def get_car_list(self):
        return self.__car_list


class CarTransmissionType(enum.Enum):  # transmission type enum
    Manual = 1,
    Automatic = 2


class CarFuelType(enum.Enum):  # fuel type enum
    Diesel = 1,
    Gas = 2,
    Petrol = 3,
    Electric = 4,
    Hybrid = 5


class Car(object):
    def __init__(self):
        self.__category: str = ''
        self.__company: str = ''
        self.__model: str = ''
        self.__release_year: int = 0
        self.__mileage: int = 0
        self.__engine: int = 0
        self.__power: int = 0
        self.__transmission: CarTransmissionType
        self.__fuel_type: CarFuelType
        self.__city_consumption: int = 0
        self.__motorway_consumption: int = 0
        self.__color: str = ''
        self.__interior_color: str = ''
        self.__num_doors: int = 0
        self.__registration_plate: str = ''
        self.__estimated_price: float = 0.0

    # Override the default __eq__ dunder method, to provide the comparison criteria for two cars.
    # Specifically, check if they belong in the same category, if they are manufactured by the same company,
    # if they are of the same model, and if they were both released on the same year. If **all** of the above
    # are True, then the two cars are the same. (We ignore car-specific details, like color, mileage, etc)
    def __eq__(self, other):
        if self.__category == other.__category and self.__company == other.__company and self.__model == other.__model \
                and self.__release_year == other.__release_year:
            return True

    def set_car_info(self, new_category, new_company, new_model, new_release_year, new_mileage, new_engine, new_power,
                     new_transmission_type, new_fuel_type, new_city_consumption, new_motorway_consumption, new_color,
                     new_interior_color, new_num_doors, new_registration_plate):
        self.__category = new_category
        self.__company = new_company
        self.__model = new_model
        self.__release_year = new_release_year
        self.__mileage = new_mileage
        self.__engine = new_engine
        self.__power = new_power
        self.__transmission = new_transmission_type
        self.__fuel_type = new_fuel_type
        self.__city_consumption = new_city_consumption
        self.__motorway_consumption = new_motorway_consumption
        self.__color = new_color
        self.__interior_color = new_interior_color
        self.__num_doors = new_num_doors
        self.__registration_plate = new_registration_plate

    def get_car_info(self) -> List:
        car_info = [self.__category, self.__company, self.__model, self.__release_year,
                    self.__mileage, self.__engine, self.__power, self.__transmission,
                    self.__fuel_type, self.__city_consumption, self.__motorway_consumption,
                    self.__color, self.__interior_color, self.__num_doors, self.__registration_plate]
        return car_info

    def calculate_car_price(self) -> float:
        # mileage coefficient, used for calculating the amount that will be removed from the car's price
        mileage_coefficient = 0.25

        # if car release year is between 1990 and 2000, price range is 500 € to 2K €
        if 1990 <= self.__release_year <= 2000:
            self.__estimated_price = round(random.uniform(500, 2000), 2)
            return self.__estimated_price  # return the estimated price, without taking into consideration the car's mileage

        # if car was released between 2001 and 2010, the price range is from 6K to 12K
        elif 2001 <= self.__release_year <= 2010:
            low_price = 6000
            high_price = 12000
        # the car was released after 2010, so the price range is from 12K to 50K
        else:
            low_price = 12000
            high_price = 50000

        # calculate the car's price (random value for simplicity)
        self.__estimated_price = round(random.uniform(low_price, high_price), 2)
        # if the car is new, i.e. has a zero mileage, just return the price, no need to subtract anything from the price
        if self.__mileage == 0:
            return self.__estimated_price
        # the car is not new, subtract an amount from the car's price, due its non-zero mileage.
        # The amount to be subtracted is calculated by multiplying the car's mileage with the mileage coefficient
        else:
            return round(self.__estimated_price - (mileage_coefficient * self.__mileage), 2)  # round to 2 decimals

    def compare_price(self, comp_price) -> bool:
        if abs(comp_price - self.__estimated_price) > 2000:
            return False  # user price is 2K above, i.e.  too high -> car is over/underpriced
        else:
            return True  # user entered price has an acceptable deviation from the system's recommended one

    def is_car_valid(self) -> bool:
        if self in system_registered_cars:  # check if car exists in the "DB"
            return True

        return False

    def calculate_circulation_tax(self) -> float:
        if 300 <= self.__engine <= 1200:  # assume that for cars with engine of 300 to 1200 cc the tax is 135 €
            return 135
        elif 1200 <= self.__engine <= 1700:  # assume that for cars with engine of 1200 to 1700 cc the tax is 280 €
            return 280
        elif 1700 <= self.__engine <= 2500:  # assume that for cars with engine of 1700 to 2500 cc the taxis 690 €
            return 690
        elif self.__engine >= 2500:  # assume that for cars with engine of more than 2500 cc the tax is 1500 €
            return 1500


class SparePart(object):
    def __init__(self):
        self.__brand: str = ''
        self.__type: str = ''
        self.__category: str = ''
        self.__code: str = ''

    def set_spare_part_info(self, new_brand, new_type, new_code):
        self.__brand = new_brand
        self.__type = new_type
        self.__code = new_code

    def get_spare_part_info(self) -> List:
        return [self.__brand, self.__type, self.__category, self.__code]

    def is_spare_part_code_valid(self) -> bool:
        match = re.search(r"PA[1-4]", self.__code)
        if match:
            return True  # spare part number is valid as it is either PA1 or PA2 or PA3 or PA4
        else:
            return False  # spare part number is not valid

    # Assume that the Spare Part code has a prefix which consists of the first 3 characters.
    # Also, assume that the Spare Parts for the car's engine, have the prefix 'PA1',
    # the prefix 'PA2' for the car's braking system and the prefix 'PA3' for the fuel gauge.
    # A prefix of 'PA4' corresponds to a general spare part
    def add_spare_part_to_category(self):
        part_code_prefix = self.__code[:2]

        if part_code_prefix == 'PA1':
            self.__category = 'Engine'
        elif part_code_prefix == 'PA2':
            self.__category = 'Braking System'
        elif part_code_prefix == 'PA3':
            self.__category = 'Fuel Gauge'
        elif part_code_prefix == 'PA4':
            self.__category = 'General'


##################### Listing types ##########################################
class Listing(object):
    def __init__(self, listing_id=random.randint(1, 990)):  # assume that Listing IDs are from 1 to 990
        self.__id: int = listing_id  # if a specific ID was given, use that one
        self.__title: str = ''
        self.__description: str = ''
        self.__publish_date: datetime = datetime.date.today()
        self.__creator: User = None
        self.__location: Location = None
        self.__photos = []

    def get_listing_id(self) -> int:
        return self.__id

    def set_listing_info(self, title, creator, location):
        self.__title = title
        self.__creator = creator
        self.__location = location

    def get_listing_location(self) -> "Location":
        return self.__location

    def set_photos(self, photos_list):
        self.__photos = photos_list

    def get_photos(self) -> List:
        return self.__photos

    def set_description(self, new_description):
        self.__description = new_description

    def get_listing(self) -> "Listing":
        return self

    def post_listing(self) -> bool:
        if self not in system_posted_listings:  # check if listing is already posted
            system_posted_listings.append(self)
            self.__creator.add_listing(self)  # add listing to user's list of listings
            return True  # listing post success

        return False  # listing post failure, i.e. it is already posted

    def delete_listing(self) -> bool:
        if self in system_posted_listings:  # check if listing is actually posted, before deletion
            system_posted_listings.remove(self)
            self.__creator.delete_listing(self)  # remove listing from user's list of listings
            return True

        return False  # listing was not found, therefore the deletion cannot take place

    @staticmethod
    def is_listing_id_valid(search_id) -> bool:
        for listing in system_posted_listings:
            if listing.__id == search_id:
                return True  # listing found in the "DB"

        return False


class ProductCondition(enum.Enum):  # product condition enum
    Used = 1,
    New = 2


class CarListing(Listing):
    def __init__(self, car_status: ProductCondition, id=random.randint(1, 990)):
        super(CarListing, self).__init__(id)
        self.__vehicle: Car = None
        self.__car_condition = car_status
        self.__docs: List["CarDocument"] = []
        self.__price: float = 0.0

    def set_car(self, new_car):
        self.__vehicle = new_car
        self.__price = self.__vehicle.calculate_car_price()  # default price is the system recommended one

    def get_car(self) -> Car:
        return self.__vehicle

    def set_docs(self, doc_list: List["CarDocument"]):
        self.__docs = doc_list

    # user entered a valid price, so change the car's price from the recommended to the new_price argument
    def set_car_price(self, new_price):
        self.__price = new_price

    def get_car_price(self) -> float:
        return self.__price

    # Normally, with this method, based on the car's uploaded pictures, a 3D model would be created. However, this has
    # not been implemented, due to its complexity that surpasses the scope of this project.
    def create_3D_model(self):
        pass

    def get_car_condition(self):
        return self.__car_condition


class SparePartListing(Listing):
    def __init__(self, id=random.randint(1, 990)):
        super(SparePartListing, self).__init__(id)
        self.__listing_part: SparePart = None
        self.__condition: ProductCondition
        self.__price: float = 0.0

    def set_spare_part_listing_info(self, spare_part, part_condition, part_price):
        self.__listing_part = spare_part
        self.__condition = part_condition
        self.__price = part_price


##################### END Listing types ##########################################

class CarDocument(object):
    def __init__(self):
        self.__issuer: str = ''
        self.__doc_id: str = ''

    # assume that this method is called inside the 'Upload File' use case, for each file uploaded
    def set_doc_info(self, issue_authority, new_id):
        self.__issuer = issue_authority
        self.__doc_id = new_id

    def get_doc_info(self) -> List:
        return [self.__issuer, self.__doc_id]


class PaymentType(enum.Enum):  # payment type enum
    Cash = 1,
    Debit = 2,
    Credit = 3


class TransactionType(enum.Enum):  # transaction type enum
    Payment = 1,
    Exchange = 2,


class Transaction(object):
    def __init__(self):
        self.__id: str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))  # 10 character rand IDs
        self.__timestamp: datetime = datetime.date.today()
        self.__payment_method: PaymentType
        self.__amount: float = 0.0
        self.__type: TransactionType
        self.__customer: User = None
        self.__merchant: User = None
        self.__product_id: int

    def get_transaction_id(self):
        return self.__id

    def get_transaction_product_id(self) -> int:
        return self.__product_id

    def set_transaction_info(self, t_method, t_amount, t_type, t_cust,
                             t_merch, t_prod_id):
        self.__payment_method = t_method
        self.__amount = t_amount
        self.__type = t_type
        self.__customer = t_cust
        self.__merchant = t_merch
        self.__product_id = t_prod_id

    def get_transaction_info(self) -> List:
        transaction_info = [self.__id, self.__timestamp, self.__payment_method, self.__amount,
                            self.__type, self.__customer, self.__merchant, self.__product_id]
        return transaction_info


# This class is used to model the behavior of some DB tables, that would contain transaction records.
# The class won't ever be instantiated, as we assume it is a Database and thus, that it is already initialized.
# Since the class won't be instantiated, all of its methods have the **@staticmethod** decorator, so that they can
# be called from other classes, without requiring access to an instance of the TransactionLog class.
# Also, the class has some **class** attributes, and no **instance** attributes, since an __init__ method won't ever
# be called
class TransactionLog(object):
    name: str = 'System-wide Transaction Log'
    transaction_list: List[Transaction] = []

    @staticmethod
    def register_transaction(new_transaction) -> bool:
        if new_transaction not in TransactionLog.transaction_list:  # check if transaction is not registered
            TransactionLog.transaction_list.append(new_transaction)
            return True  # transaction doesn't exist, return register success

        return False  # transaction already exists, return failure

    @staticmethod
    def is_transaction_id_valid(check_id) -> bool:
        for transaction in TransactionLog.transaction_list:
            if transaction.get_transaction_id() == check_id:
                return True  # transaction found in transaction log, thus the given ID is valid

        return False  # a transaction with the given ID, was not found in the Transaction Log, i.e.

    @staticmethod
    def find_transaction(transaction_id) -> Transaction:
        for transaction in TransactionLog.transaction_list:
            if transaction.get_transaction_id() == transaction_id:
                return transaction


class MonthlyInstallment(object):
    def __init__(self):
        self.__transaction: Transaction = None
        self.__price: float = 0.0
        self.__product_price: float = 0.0
        self.__due_date: datetime = datetime.date.today() + relativedelta(months=+1)  # set due date to 1 month from now

    def set_product_price(self, new_price):
        self.__product_price = new_price

    def set_transaction(self, inst_trans):
        self.__transaction = inst_trans

    def get_installment_info(self) -> List:
        return [self.__transaction, self.__price, self.__product_price, self.__due_date]

    def calculate_installment_price(self, user_salary) -> float:
        # if the 20% of the user's salary is greater than the product's price, then we cannot use that percentage
        # of the user's salary, as an upper bound for the randint function, as in the following "else" clause.
        # Therefore, set the upper bound equal to the product's price divided by 5
        if 0.2 * user_salary > self.__product_price:
            self.__price = random.randint(0, int(self.__product_price / 5))
        else:
            self.__price = random.randint(0, 0.2 * user_salary)
            # assume that the installment's price can be at most equal to 20% of the user's salary

        return self.__price


class Invoice(object):
    def __init__(self):
        self.__transaction: Transaction = None
        self.__invoice_code: int = random.randint(15000, 20000)  # assume Invoice codes are within this range
        self.__text: str = ''
        self.__recipient_email: str = ''

    def set_invoice_info(self, inv_trans, inv_text, inv_recp_email):
        self.__transaction = inv_trans
        self.__text = inv_text
        self.__recipient_email = inv_recp_email

    def get_invoice(self) -> "Invoice":
        return self


class InsurancePlanType(enum.Enum):
    Basic = 1,
    Premium = 2


class InsurancePlan(object):
    def __init__(self):
        self.__name: str = ''
        self.__plan_id: int = random.randint(20001, 25000)  # assume InsurancePlan id is within this range
        self.__type: InsurancePlanType
        self.__price: float = 0.0
        self.__num_months: int

    def set_insurance_plan_info(self, plan_name, plan_type, plan_price, plan_duration):
        self.__name = plan_name
        self.__type = plan_type
        self.__price = plan_price
        self.__num_months = plan_duration

    def get_insurance_plan_info(self) -> List:
        return [self.__name, self.__plan_id, self.__type, self.__price, self.__num_months]

    def calculate_insurance_plan_price(self, points):
        discount_coefficient = 0.1  # 10 % discount on the plan's price
        plan_price = random.randint(50, 250)  # assume that the price range for the Insurance Plans is [50€, 250€]
        return plan_price - (discount_coefficient * points)  # apply discount


class Location(object):
    def __init__(self, location_coordinates: Tuple[float, float]):
        self.__coordinates: Tuple[float, float] = location_coordinates

    # Override the default __eq__ dunder method, to provide the comparison basis for two Location objects.
    # We only need to check if their coordinates are equal
    def __eq__(self, other):
        if self.__coordinates == other.__coordinates:
            return True

        return False

    def set_location(self, new_coordinates: Tuple[float, float]):
        self.__coordinates = new_coordinates

    def get_location(self) -> Tuple[float, float]:
        return self.__coordinates

    def check_location_validity(self) -> bool:
        # check latitude then longitude. Assume that the city of Patras is within the values below for long and lat.
        if 38.16505110795069 <= self.__coordinates[0] <= 38.31297891120904 and \
                21.656052138460673 <= self.__coordinates[1] <= 21.817232185432744:
            return True  # location is within Patras, return true
        else:
            return False  # location is outside of Patras, return false


class CarCompanies(enum.Enum):  # companies enum
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


class TestDrive(object):
    def __init__(self):
        self.__listing: CarListing = None
        self.__date: datetime
        self.__user: User = None

    def set_test_drive_info(self, td_listing, td_driver):
        self.__listing = td_listing
        self.__user = td_driver

    def set_test_drive_date(self, td_date):
        self.__date = td_date

    def register_test_drive(self) -> bool:
        if self not in system_scheduled_test_drives:  # check if the appointment is not already registered
            system_scheduled_test_drives.append(self)
            return True  # new test drive added

        return False  # attempt to register an already-existing test drive, to the schedules ones

    def is_date_available(self) -> bool:
        for test_drive in system_scheduled_test_drives:
            # test drive booked for the same car listing and at the same day and time, therefore the date is unavailable
            if test_drive.__date == self.__date and test_drive.__listing == self.__listing:
                return False

        return True  # date is available


class TransportationType(enum.Enum):  # transportation type enum
    express = 1,
    standard = 2


class OperationStatus(enum.Enum):  # transportation status enum
    Pending = 1,
    Ongoing = 2,
    Completed = 3


class InspectionType(enum.Enum):  # Inspection Type enum
    Basic = 1,
    CarEngine = 2,
    Thorough = 3


class CarInspection(object):
    def __init__(self):
        self.__inspector: Inspector = None
        self.__transaction: Transaction = None
        self.__car_listing: CarListing = None
        self.__status: OperationStatus = OperationStatus.Pending
        self.__inspection_time: datetime.date
        self.__docs: List["CarDocument"] = []
        self.__inspection_type: InspectionType
        self.__location: Location = None

    # This method is used, when the User chose an Inspector different from the system recommended one
    def set_car_inspection_inspector(self, check_inspector: Inspector):
        self.__inspector = check_inspector

    def set_car_inspection_transaction(self, payment_transaction):  # set car inspection payment transaction
        self.__transaction = payment_transaction

    def set_car_to_inspect(self, check_car_listing: CarListing):
        self.__car_listing = check_car_listing

    def set_car_inspection_info(self, check_type, check_time, check_location):
        self.__inspection_type = check_type
        self.__inspection_time = check_time
        self.__location = check_location

    def register_car_inspection(self) -> bool:
        if self not in system_scheduled_car_inspections:  # if appointment not already registered
            system_scheduled_car_inspections.append(self)
            if self.__inspector.add_inspection(self):  # add the appointment to the Inspector's CarInspection list
                return True  # return true, adding a non-existing car inspection

        return False  # return false, as an attempt to add an already-existing car inspection, was made

    # find a recommended inspector, based on the location the user entered. We assume that the user's location
    # must be **exactly** the same (i.e. equal) to the inspector's location. In reality, we would search an Inspector
    # that is **near** the user (within some radius), and not in the exact same location
    def find_recommended_inspector(self) -> Inspector:
        for user in system_registered_users:
            if isinstance(user, Inspector):
                # inspector's location is the same as the location the user entered
                if user.get_inspector_location() == self.__location:
                    self.__inspector = user  # set the inspection's inspector to the recommended one
                    return user

    # check to see if the User entered a valid Inspector
    def find_inspector(self, telephone, email) -> Inspector:
        for user in system_registered_users:
            if isinstance(user, Inspector):
                if user.get_telephone() == telephone and user.get_email() == email:
                    return user

    def start_car_inspection(self):
        self.__status = OperationStatus.Ongoing  # set status to Ongoing

    def finish_car_inspection(self):
        self.__status = OperationStatus.Completed  # set status to Completed

    def get_inspector(self) -> Inspector:
        return self.__inspector


class CarTransportation(object):
    def __init__(self):
        self.__car_transaction: Transaction = None
        self.__delivery_location: Location = None
        self.__status: OperationStatus = OperationStatus.Pending
        self.__package: TransportationType
        self.__transporter: Transporter = None
        self.__car_listing: CarListing = None
        self.__transportation_time: datetime = None

    def set_car_purchase_transaction(self, transaction_id):
        self.__car_transaction = TransactionLog.find_transaction(transaction_id)
        self.find_car()

    def find_car(self):  # find the listing of the car to be transported
        for listing in system_posted_listings:
            if isinstance(listing, CarListing):
                if listing.get_listing_id() == self.__car_transaction.get_transaction_product_id():
                    self.__car_listing = listing

        self.find_transporter()

    def estimate_transportation_duration(self, transportation_package: TransportationType) -> int:
        if transportation_package == 'standard':
            return 3  # assume that the standard transportation package, has an estimated delivery time of 3 days
        elif transportation_package == 'express':
            return 1  # assume that the express transportation package, has an estimated delivery time of 1 day

    def set_car_transportation_info(self, new_delivery_location, new_package):
        self.__delivery_location = new_delivery_location
        self.__package = new_package
        self.__transportation_time = self.estimate_transportation_duration(new_package)

    def register_car_transportation(self) -> bool:
        if self not in system_scheduled_car_transportations:
            system_scheduled_car_transportations.append(self)
            if self.__transporter.add_transportation(self):  # also add the transportation, to the transporter's list
                return True  # registering a new car transportation

        return False  # return false, as an attempt to add an already-existing car transportation was made

    # find a transporter based on the location of the car
    def find_transporter(self):
        for user in system_registered_users:
            if isinstance(user, Transporter):
                # transporter's location is the same as the car's location
                if user.get_transporter_location() == self.__car_listing.get_listing_location():
                    # if the transporter has less than 10 pending transportations
                    if user.add_transportation(self):  # if Transporter has available "transportation-slots"
                        self.__transporter = user
                        break

    def start_car_transportation(self):
        self.__status = OperationStatus.Ongoing  # set status to Ongoing

    def finish_car_transportation(self):
        self.__status = OperationStatus.Completed  # set status to Compelted


class CarComparison(object):
    def __init__(self):
        self.__car_listings: List[CarListing] = []
        self.__criteria: List[str] = []
        self.__price_range: Tuple[float, float] = (0.0, 0.0)
        self.__comp_results: List[Car] = []
        self.__recommended_car: Car = None

    def set_listings_to_compare(self, listings: List[CarListing]):
        self.__car_listings = listings

    def get_car_listings(self) -> List[CarListing]:
        return self.__car_listings

    def set_car_comparison_info(self, comp_criteria, comp_price_range):
        self.__criteria = comp_criteria
        self.__price_range = comp_price_range

    # Choose a car at random for the recommended one. Normally, we would pick a car based on the criteria the user entered
    def find_recommended_car(self):
        self.__recommended_car = self.__car_listings[random.randint(0, len(self.__car_listings) - 1)].get_car()

    def generate_comparison_results(self):  # just append the cars to the results list, no actual comparison is made
        for car_lst in self.__car_listings:
            self.__comp_results.append(car_lst.get_car())

        CarListingsStatisticsLog.register_car_comparison(self)  # add CarComparison the system's log


class CarSearch(object):
    def __init__(self):
        self.__search_results: List[CarListing] = []
        self.__criteria: List[str] = []
        self.__location: Location = None
        self.__search_radius: int
        self.__price_range: Tuple[float, float] = (0.0, 0.0)

    # __criteria has: [category, company, model, year, mileage_from, mileage_to,
    #                 engine_from, engine_to, power_from, power_to, condition
    #                 transmission, fuel_type, num_doors, int_color, ext_color
    #                 price_from, price_to

    def set_car_search_info(self, search_criteria, search_location, search_radius, search_price_range):
        self.__criteria = search_criteria
        self.__location = search_location
        self.__search_radius = search_radius
        self.__price_range = search_price_range

    def generate_search_results(self):  # just check for car category, company, model and price
        if self.__criteria:  # if the user entered search criteria, search for the appropriate car listings
            for lst in system_posted_listings:
                if isinstance(lst, CarListing):  # check is Listing is a CarListing
                    car_info = lst.get_car().get_car_info()

                    # same category, company, model
                    if self.__criteria[0] == car_info[0] and self.__criteria[1] == car_info[1] and self.__criteria[2] == \
                            car_info[2]:
                        # car price within price range
                        if float(self.__criteria[16]) <= lst.get_car_price() <= float(self.__criteria[17]):
                            self.__search_results.append(lst)  # append the current listing to the search results
        else:  # the user didn't enter any criteria, fetch popular car listings
            self.__search_results = CarListingsStatisticsLog.get_popular_car_listings()

        CarListingsStatisticsLog.register_car_search(self)  # register the CarSearch to the system's log

    def get_search_results_list(self) -> List[CarListing]:
        return self.__search_results


class CarExchange(object):
    def __init__(self):
        self.__vehicle: Car = None
        self.__car_estimated_price: float = 0.0
        self.__car_owner: User = None
        self.__exchange_reward: float = 0.0
        self.__legal_documents: List[CarDocument] = []
        self.__transaction: Transaction = None
        self.__dealerships: List[DealershipStore] = None
        self.__chosen_store: DealershipStore = None

    # find the stores that accept the user's car
    def find_stores(self) -> List[DealershipStore]:
        exchange_car_info = self.__vehicle.get_car_info()
        for store in system_registered_stores:
            cars_list = store.get_cars_list()  # retrieve each store's car list
            for car in cars_list:
                car_info = car.get_car_info()  # retrieve each car's info
                # If the under-exchange car has the same manufacturing company and if of the same model, as a car
                # found in the store's list, then the current store accepts the user's car.
                if car_info[1] == exchange_car_info[1] and car_info[2] == exchange_car_info[2]:
                    self.__dealerships.append(store)  # add the current store the CarExchange's store list

        return self.__dealerships

    # set which store was chosen from the user and the exchange's reward
    def set_chosen_store(self, store, exchange_reward):
        self.__chosen_store = store
        self.__exchange_reward = exchange_reward

    def set_car_info(self, exchange_car, exchange_car_price, exchange_car_owner):
        self.__vehicle = exchange_car
        self.__car_estimated_price = exchange_car_price
        self.__car_owner = exchange_car_owner

    def set_transaction(self, exchange_transaction):
        self.__transaction = exchange_transaction

    def set_docs(self, new_docs):
        self.__legal_documents = new_docs


# Similarly, to the TransactionLog class, this class is used to model the behavior of some DB tables, that would contain
# records of all the car searches and car comparisons, made by the users of the platform.
# The class won't ever be instantiated, as we assume it is a Database.
# Since the class won't be instantiated, all of its methods have the **@staticmethod** decorator, so that they can
# be called from other classes, without requiring access to an instance of the CarListingsStatisticsLog class.
# Also, the class has some **class** attributes, and no **instance** attributes, since an __init__ method won't ever
# be called
class CarListingsStatisticsLog(object):
    car_search_log: List[CarSearch] = []  # a log of all the car searches
    car_comparison_log: List[CarComparison] = []  # a log of all the car comparisons
    popular_car_listings: List[CarListing] = []  # a "DB table" with the most popular car listings

    @staticmethod
    def get_popular_car_listings() -> List[CarListing]:
        return CarListingsStatisticsLog.popular_car_listings

    @staticmethod
    def register_car_search(new_car_search) -> bool:
        if new_car_search not in CarListingsStatisticsLog.car_search_log:  # if car search not already registered
            CarListingsStatisticsLog.car_search_log.append(new_car_search)
            # since a new item was added on the CarListingsStatisticsLog class, we need to update the "DB table"
            # storing the most popular car listings, to account for the new data being entered
            CarListingsStatisticsLog.update_popular_car_listings(new_car_search)
            return True  # registration success
        else:
            return False  # registration failure

    @staticmethod
    def register_car_comparison(new_car_comparison) -> bool:
        if new_car_comparison not in CarListingsStatisticsLog.car_comparison_log:  # if car comparison not registered
            CarListingsStatisticsLog.car_comparison_log.append(new_car_comparison)
            # since a new item was added on the CarListingsStatisticsLog class, we need to update the "DB table"
            # storing the most popular car listings, to account for the new data being entered
            CarListingsStatisticsLog.update_popular_car_listings(new_car_comparison)
            return True
        else:
            return False

    # This method does not execute any *statistical analysis*, which would be its "real-world" function.
    # We just get the car listings, involved in each operation (CarSearch or CarComparison) and check if they appear
    # at least 3 times in operations of the same kind. If they do, we assume that the specific listing, is a
    # popular one, and we add it to popular_car_listings
    @staticmethod
    def update_popular_car_listings(operation):
        if isinstance(operation, CarSearch):  # if operation is a CarSearch
            # get each CarSearch's results list, which consists of a list of CarListings. Then count the number of
            # occurrences of each CarListing, in the search results list of all the CarSearches. If the current
            # CarListing is present in at least 3 of the search results lists, then we can conclude that it is a
            # popular CarListings, and thus we add it to the popular_car_listings list.
            # In the following else-if statement, we do the same for the CarComparisons
            for car_search in CarListingsStatisticsLog.car_search_log:
                car_listings = car_search.get_search_results_list()
                for listing in car_listings:
                    listing_count = 0
                    for curr_search in CarListingsStatisticsLog.car_search_log:
                        if listing in curr_search.get_search_results_list():
                            listing_count += 1
                            if listing_count >= 3:
                                if listing not in CarListingsStatisticsLog.popular_car_listings:
                                    CarListingsStatisticsLog.popular_car_listings.append(listing)

        elif isinstance(operation, CarComparison):
            for car_comparison in CarListingsStatisticsLog.car_comparison_log:
                car_listings = car_comparison.get_car_listings()
                for listing in car_listings:
                    listing_count = 0
                    for curr_comp in CarListingsStatisticsLog.car_comparison_log:
                        if listing in curr_comp.get_car_listings():
                            listing_count += 1
                            if listing_count >= 3:
                                if listing not in CarListingsStatisticsLog.popular_car_listings:
                                    CarListingsStatisticsLog.popular_car_listings.append(listing)


class Advertisement(object):
    def __init__(self):
        self.__creator: User = None
        self.__text: str = ''
        self.__photos = []
        self.__creation_date: datetime = None

    def set_ad_info(self, creator, text, date, photos_list):
        self.__creator = creator
        self.__text = text
        self.__photos = photos_list
        self.__creation_date = date

    def get_ad_info(self) -> List:
        return [self.__creator.get_user_info(), self.__text, self.__photos, str(self.__creation_date)]


class PushNotification(object):
    def __init__(self):
        self.__creator: User = None
        self.__text: str = ''
        self.__issue_time: datetime = None
        self.__recipients: List["User"] = []

    def set_notification_info(self, creator, text, time):
        self.__creator = creator
        self.__text = text
        self.__issue_time = time

    def get_notification_info(self) -> List:
        return [self.__creator.get_user_info(), self.__text, str(self.__issue_time), self.__recipients]

    def add_recipient(self, recp):
        self.__recipients.append(recp)


class Message(object):
    def __init__(self):
        self.__sender: User = None
        self.__recipient: User = None
        self.__text: str = ''
        self.__creation_timestamp: datetime = None

    def set_message_info(self, new_sender, new_recipient, new_text, new_timestamp):
        self.__sender = new_sender
        self.__recipient = new_recipient
        self.__text = new_text
        self.__creation_timestamp = new_timestamp

    def get_message_info(self) -> List:
        return [self.__sender.get_user_info(), self.__recipient.get_user_info(), self.__text,
                str(self.__creation_timestamp)]


class Review(object):
    def __init__(self):
        self.__text: str
        self.__stars: int
        self.__writer: User
        self.__creation_date: datetime = datetime.date.today()

    def set_review_info(self, new_text, new_stars, new_writer):
        self.__text = new_text
        self.__stars = new_stars
        self.__writer = new_writer

    def get_review_info(self) -> List:
        return [self.__text, self.__stars, self.__writer.get_user_info(), str(self.__creation_date)]

    def is_review_positive(self) -> bool:
        if self.__stars >= 3:  # assume that reviews with more than 3 stars are positive
            return True

        return False


class ListingReport(object):
    def __init__(self):
        self.__listing: Listing = None
        self.__creator: User = None
        self.__report_id: int = random.randint(30000, 35000)  # assume ListingReport IDs are withing this range
        self.__status: str = 'Unchecked'
        self.__text: str = ''
        self.__creation_date: datetime.date = datetime.date.today()
        self.__report_auditor: InsuranceCompanyEmployee = None

    def set_listing_report_info(self, reported_listing, report_creator, report_text, report_auditor):
        self.__listing = reported_listing
        self.__creator = report_creator
        self.__text = report_text
        self.__report_auditor = report_auditor

    def get_listing_report(self) -> "ListingReport":
        return self

    @staticmethod
    def is_listing_report_id_valid(search_id: int) -> bool:
        for report in system_registered_listing_reports:
            if report.__report_id == search_id:
                return True  # a ListingReport with the given ID was found, return True

        return False  # no ListingReport found with the given ID, thus the given ID is invalid

    def get_listing_report_status(self):
        return self.__status

    def set_status_checked(self):
        self.__status = 'Checked'

    def register_listing_report(self) -> bool:
        if self not in system_registered_listing_reports:  # if ListingReport not in the "DB"
            system_registered_listing_reports.append(self)
            return True

        return False


class ListingDeletionForm(object):
    def __init__(self):
        self.__listing_report: ListingReport = None
        self.__text: str = ''
        self.__creation_date: datetime.date = datetime.date.today()

    def set_listing_deletion_form_info(self, listing_report, text):
        self.__listing_report = listing_report
        self.__text = text

    def get_deletion_form(self) -> "ListingDeletionForm":
        return self


# if __name__ == "__main__":
def main():
    test_user_location = Location((38.25, 21.75))

    test_user = User()
    test_user.set_name('john', 'doe')
    test_user.set_username('jdoe91823')
    test_user.set_email('jdoe@gmail.com')
    test_user.set_telephone('2610987567')
    system_registered_users.append(test_user)

    inspector_location = Location((38.2, 21.7))
    test_inspector = Inspector(inspector_location)
    test_inspector.set_name('Bob', 'Green')
    test_inspector.set_username('bgreen123')
    test_inspector.set_email('green123@gmail.com')
    test_inspector.set_telephone('6900012344')
    system_registered_users.append(test_inspector)

    inspector_location2 = Location((38.3, 21.8))
    test_inspector2 = Inspector(inspector_location2)
    test_inspector2.set_name('Jim', 'Brown')
    test_inspector2.set_username('jbr0wn33')
    test_inspector2.set_email('jbrown33@gmail.com')
    test_inspector2.set_telephone('6911122233')
    system_registered_users.append(test_inspector2)

    rev1 = Review()
    rev1.set_review_info('The best Inspector', 5, test_user)
    test_inspector.add_user_review(rev1)
    rev2 = Review()
    rev2.set_review_info('The worst Inspector', 0, test_user)
    test_inspector.add_user_review(rev2)
    rev3 = Review()
    rev3.set_review_info('A decent Inspector', 3, test_user)
    test_inspector.add_user_review(rev3)
    rev4 = Review()
    rev4.set_review_info('Would recommend', 4, test_user)
    test_inspector.add_user_review(rev4)
    rev5 = Review()
    rev5.set_review_info('Would not recommend', 2, test_user)
    test_inspector.add_user_review(rev5)

    c3 = Car()
    c3.set_car_info('Hatchback', 'Citroen', 'C3', 2005, 4500, 1200, 90, 'Automatic',
                    'Fuel', 6, 5, 'Blue', 'Grey', 5, 'XAA2233')

    car_listing = CarListing(ProductCondition.Used, 500)
    car_listing.set_listing_info("Citroen C3 for sale", test_user, test_user_location)
    car_listing.set_description("The car is in excellent condition, contact me for more")
    car_listing.set_car(c3)
    car_listing.post_listing()
    system_registered_cars.append(c3)

    giulietta = Car()
    giulietta.set_car_info('Hatchback', 'Alfa Romeo', 'Giulietta', 2010, 5000, 123, 32, 'Manual',
                           'Diesel', 555, 666, 'Red', 'Black', 5, 'AXE1234')

    system_registered_cars.append(giulietta)
