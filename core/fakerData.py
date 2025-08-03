from faker import Faker
import json

# Initialize faker
fake = Faker()


def generate_fake_customer():
    return {

    }


fake_customers = [generate_fake_customer() for _ in range(10)]
fake_customers_json = json.dumps(fake_customers, indent=4)
print(fake_customers_json)

# "first_name": fake.first_name(),
# "last_name": fake.last_name(),
# "phone_number": fake.phone_number(),
# "age": fake.random_number(),
# "role": fake.boolean(),
# "is_active": fake.boolean(),
# "is_staff": fake.boolean(),
# "address": fake.address(),
# "location": fake.location_on_land(),

