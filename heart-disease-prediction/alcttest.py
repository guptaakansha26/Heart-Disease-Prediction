from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Test

# Create SQLAlchemy engine to connect to database
engine = create_engine('sqlite:///mydb.sqlite', echo=True)

# Create a session factory for interacting with the database
Session = sessionmaker(bind=engine)

# Create a session to interact with the database
session = Session()

# Create a new user
new_user = User(username='johndoe', email='joh2ndoe@example.com', phone='123-456-7890', password='password')


# Add the new user to the session
session.add(new_user)

# Commit the session to save the new user to the database
session.commit()

# Close the session
session.close()






# Create a session to interact with the database
session = Session()
new_test = Test(user_id=1, age=45, gender='Male', chest_pain_type='Atypical angina',
                resting_bp=140, cholesterol=230, fasting_bs='120',
                resting_ecg=1, max_hr=150, exercise_angina='No', oldpeak=1.5,
                st_slope='Flat', result='Positive')


# Add the new test to the session
session.add(new_test)

# Commit the session to save the new test to the database
session.commit()

# Close the session
session.close()



