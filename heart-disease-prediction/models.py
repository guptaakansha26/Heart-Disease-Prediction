from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

# Create SQLAlchemy engine to connect to database
engine = create_engine('sqlite:///mydb.sqlite', echo=True)

# Declare base class for SQLAlchemy models
Base = declarative_base()




# Define User model class
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    phone = Column(String(20), unique=True, nullable=False)
    password = Column(String(50), nullable=False)
    
    def __repr__(self):
        return f'<User(username={self.username}, email={self.email}, phone={self.phone})>'
    




# Define Test model class
class Test(Base):
    __tablename__ = 'tests'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(10), nullable=False)
    chest_pain_type = Column(String(50), nullable=False)
    resting_bp = Column(Integer, nullable=False)
    cholesterol = Column(Integer, nullable=False)
    fasting_bs = Column(String(10), nullable=False)
    resting_ecg = Column(Integer, nullable=False)
    max_hr = Column(Integer, nullable=False)
    exercise_angina = Column(String(10), nullable=False)
    oldpeak = Column(Float, nullable=False)
    st_slope = Column(String(50), nullable=False)
    result = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f'<Test(user_id={self.user_id}, age={self.age}, gender={self.gender}, result={self.result})>'


    
# Create the users table in the database
Base.metadata.create_all(engine)
