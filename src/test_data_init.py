from classes import *


# create some test data
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
