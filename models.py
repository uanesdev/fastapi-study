from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base
#from sqlalchemy_utils import ChoiceType


# Create the database connection
db = create_engine("sqlite:///database.db")

# Create the base class
Base = declarative_base()

# Create the models and tables
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    email = Column(String, nullable=False, unique=True)
    password = Column(String)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean)

    def __init__(self, name, email, password, is_admin=False, is_active=True):
        self.name = name
        self.email = email
        self.password = password
        self.is_admin = is_admin
        self.is_active = is_active

class Order(Base):
    __tablename__ = "orders"
    
    # Define the status choices
    # STATUS_CHOICES = [
    #     ("PENDING", "pending"),
    #     ("COMPLETED", "completed"),
    #     ("CANCELLED", "cancelled"),
    # ]

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String)
    user = Column(ForeignKey("users.id"))
    price = Column(Float)

    def __init__(self, user, status,  price=0):
        self.user = user
        self.status = status
        self.price = price

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    quantity = Column(Integer)
    size = Column(String)
    unit_price = Column(Float)
    order = Column(ForeignKey("orders.id"))

    def __init__(self, quantity, size, unit_price, order):
        self.quantity = quantity
        self.size = size
        self.unit_price = unit_price
        self.order = order

# Execute the create_all method to create the tables