from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine, Session
from sqlalchemy.orm import sessionmaker
from pprint import pprint

# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:////web/Sqlite-Data/example.db')
Session = sessionmaker(bind=engine)
session = Session()
# this loads the sqlalchemy base class
Base = declarative_base()

# Setting up the classes that create the record objects and define the schema

class Customer(Base):
    __tablename__ = 'customer'
    first_name = Column(String(250), nullable=False)
    last_name = Column(String(250), nullable=False)
    username = Column(String(250), nullable=False)
    email = Column(String(250))
    address = Column(String(250))
    town = Column(String(250))

class Item(Base):
    __tablename__ = 'items'
    name = Column(String(250))
    cost_price = Column(Integer)
    selling_price = Column(Integer)
    quantity = Column(Integer)

class Person(Base):
    __tablename__ = 'person'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


class Address(Base):
    __tablename__ = 'address'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    street_name = Column(String(250))
    street_number = Column(String(250))
    post_code = Column(String(250), nullable=False)
    # creates the field to store the person id
    person_id = Column(Integer, ForeignKey('person.id'))
    # creates the relationship between the person and addresses.  backref adds a property to the Person class to retrieve addresses
    person = relationship("Person", backref="addresses")

c1 = Customer(first_name = 'Toby',
              last_name = 'Miller',
              username = 'tmiller',
              email = 'tmiller@example.com',
              address = '1662 Kinney Street',
              town = 'Wolfden'
              )
c2 = Customer(first_name = 'Scott',
              last_name = 'Harvey',
              username = 'scottharvey',
              email = 'scottharvey@example.com',
              address = '424 Patterson Street',
              town = 'Beckinsdale'
              )
c3 = Customer(first_name="John",
              last_name="Lara",
              username="johnlara",
              email="johnlara@mail.com",
              address="3073 Derek Drive",
              town="Norfolk"
              )
c4 = Customer(first_name="Sarah",
              last_name="Tomlin",
              username="sarahtomlin",
              email="sarahtomlin@mail.com",
              address="3572 Poplar Avenue",
              town="Norfolk"
              )
c5 = Customer(first_name='Toby',
              last_name='Miller',
              username='tmiller',
              email='tmiller@example.com',
              address='1662 Kinney Street',
              town='Wolfden'
              )
c6 = Customer(first_name='Scott',
              last_name='Harvey',
              username='scottharvey',
              email='scottharvey@example.com',
              address='424 Patterson Street',
              town='Beckinsdale'
              )

session.add_all([c1, c2, c3, c4, c5, c6])
session.commit()

i1 = Item(name='Chair', cost_price=9.21, selling_price=10.81, quantity=5)
i2 = Item(name='Pen', cost_price=3.45, selling_price=4.51, quantity=3)
i3 = Item(name='Headphone', cost_price=15.52, selling_price=16.81, quantity=50)
i4 = Item(name='Travel Bag', cost_price=20.1, selling_price=24.21, quantity=50)
i5 = Item(name='Keyboard', cost_price=20.1, selling_price=22.11, quantity=50)
i6 = Item(name='Monitor', cost_price=200.14, selling_price=212.89, quantity=50)
i7 = Item(name='Watch', cost_price=100.58, selling_price=104.41, quantity=50)
i8 = Item(name='Water Bottle', cost_price=20.89, selling_price=25, quantity=50)

session.add_all([i1, i2, i3, i4, i5, i6, i7, i8])
session.commit()

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Insert a Person in the person table
new_person1 = Person(name='Keith')
session.add(new_person1)
# this adds the person to the session
new_person2 = Person(name='Joe')
session.add(new_person1)

new_person3 = Person(name='Steve')
session.add(new_person1)
session.commit()
# commit saves the changes
# Insert an Address in the address table using a loop

addresses = [
    Address(post_code='00001', person=new_person1),
    Address(post_code='00002', person=new_person2),
    Address(post_code='00003', person=new_person3),
]

# Loop through addresses and commit them to the database
for address in addresses:
    session.add(address)
    session.commit()

# joins Person on Address
all_people = session.query(Person).join(Address).all()

# Accessing a person with their address, You have to loop the addresses property and remember it was added by the
# backref on the addresses class
for person in all_people:
    # use the __dict__ magic method to have the object print it's properties
    pprint(person.__dict__)
    for address in person.addresses:
        pprint(address.__dict__)

# Retrieving the inverse of the relationship.  Notice I reverse the Person and Address to load the Address table
all_addresses = session.query(Address).join(Person).all()
for address in all_addresses:
    # showing how to use the print function with printing text and data at the same time easily
    print(f'{address.person.name} has a postal code of {address.post_code}')