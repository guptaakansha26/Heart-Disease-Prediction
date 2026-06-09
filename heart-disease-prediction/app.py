from flask import Flask, render_template, request, redirect, session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Test
import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

# Create SQLAlchemy engine to connect to database
engine = create_engine('sqlite:///mydb.sqlite', echo=True)

# Declare base class for SQLAlchemy models
Base = declarative_base()

DbSession = sessionmaker(bind=engine)

# Create Flask app instance
app = Flask(__name__)
app.secret_key = '67tyrteytertwiruih67456bcagd'

import pickle

model_lgr = None

with open("model_lgr.pkl", "rb") as f:
    model_lgr = pickle.load(f)

sex_map = {'Male':1, 'Female':2}
chest_pain_type_map = {'ATA':1, 'NAP':2, 'ASY':3, 'TA':4 }
resting_ecg_map = {'Normal':1, 'ST':2, 'LVH':3}
excercise_angina_map = {'No':1, 'Yes':2}
st_slop_map = {'Up':1, 'Flat':2, 'Down':3 }



@app.route('/', methods=['GET','POST'])
def index():
    if request.method == "GET":
        return render_template('index.html')
    else:
        phone = request.form['phone']
        password = request.form['pass']
        db_session = DbSession()

        user = db_session.query(User).filter(User.phone == phone).filter(User.password == password).first()
        
        db_session.close()

        if user is None:
            return render_template('index.html', message = "Username or password are not match!")
        else:
            session['User'] = user.phone
            return redirect('/useraccount')

@app.route('/logout')
def logout():
    session['User'] = None
    return redirect('/')




@app.route('/useraccount')
def useraccount():
    if session['User'] is None:
        return redirect('/')
    opt = 'new_test'
    records = []
    ratio = 0
    if request.args.get('opt') == 'records' :
        opt = 'records'

        # Create a session to interact with the database
        db_session = DbSession()
        user = db_session.query(User).filter(User.phone == session['User']).first()
        user_id = user.id
        # Commit the session to save the new user to the database
        res = db_session.commit()
        print(res)# Close the session
      

        records =  db_session.query(Test).filter(Test.user_id == user_id).all()

        print(records)

      

        totaltest = len(records)

        positive = len(db_session.query(Test).filter(Test.user_id == user_id).filter(Test.result == 1).all())


        db_session.close()

        if totaltest == 0:
            ratio = 0
        else:
            ratio = (positive/totaltest)*100;




    return render_template('account.html',active=opt, records = records, ratio = ratio)


@app.route('/register', methods=['GET','POST'] ) #,methods=['GET'])
def register():

    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        password2 = request.form['password2']
        if not password == password2:
            return render_template('register.html', message = "Both passwords are not match!", name=name, email=email, phone=phone)
        
        try:
            # Create a session to interact with the database
            db_session = DbSession()
            # Create a new user
            new_user = User(name=name, email=email, phone=phone, password=password)
            # Add the new user to the session
            db_session.add(new_user)
            # Commit the session to save the new user to the database
            res = db_session.commit()
            print(res)# Close the session
            db_session.close()
            
            session['User'] = phone
            return redirect('/useraccount')
        

        except sqlalchemy.exc.IntegrityError:
            return render_template('register.html', message = "email or phone already exist!", name=name, email=email, phone=phone)


    return render_template('register.html', message = None)




@app.route('/predict', methods=['POST'])
def predict():
    
    global model_lgr

    if session['User'] is None:
        return redirect('/')
    
    if request.method == "POST":
        age = float(request.form['age'])
        gender = request.form['gender']
        chest_pain_type = request.form['chest_pain_type']
        resting_bp = float(request.form['resting_bp'])
        cholesterol = float(request.form['cholesterol'])
        fasting_bs = float(request.form['fasting_bs'])
        resting_ecg = request.form['resting_ecg']
        maxhr = float(request.form['maxhr'])
        exercise_angina = request.form['exercise_angina']
        oldpeak = float(request.form['oldpeak'])
        st_slope = request.form['st_slope']



        sex_int = sex_map[gender]
        sex_int = float(sex_int)

        chest_pain_type_int = chest_pain_type_map[chest_pain_type]
        chest_pain_type_int = float(chest_pain_type_int)

        resting_ecg_int = resting_ecg_map[resting_ecg]
        resting_ecg_int = float(resting_ecg_int)

        selected_exercise_int = excercise_angina_map[exercise_angina]
        selected_exercise_int = float(selected_exercise_int)

        selected_st_slope_int = st_slop_map[st_slope]
        selected_st_slope_int = float(selected_st_slope_int)

        result = model_lgr.predict([[age, sex_int, chest_pain_type_int, resting_bp
                                    , cholesterol, fasting_bs, resting_ecg_int, maxhr,
                                         selected_exercise_int, oldpeak, selected_st_slope_int]])
        
        final_result = int(result[0])

        if result[0]==0:
            print("Heart disease not deteacted!")
        elif result[0]==1:
            print("Heart disease deteacted!")


        #try:
        # Create a session to interact with the database
        db_session = DbSession()

        user = db_session.query(User).filter(User.phone == session['User']).first()

    
        
        # Print the user's name (assuming the user was found)
        if user:
            print(user.name)
        else:
            return redirect('/register')

            # Create a new user
        new_test = Test(user_id=user.id, age=age, gender=gender, chest_pain_type=chest_pain_type,
            resting_bp=resting_bp, cholesterol=cholesterol, fasting_bs=fasting_bs,
            resting_ecg=resting_ecg, max_hr=maxhr, exercise_angina=exercise_angina, oldpeak=oldpeak,
            st_slope=st_slope, result=final_result)

        
        # Add the new user to the session
        db_session.add(new_test)
        # Commit the session to save the new user to the database
        res = db_session.commit()
        print(res)# Close the session
        db_session.close()


        return redirect('/useraccount?opt=records')




    return render_template('account.html',active="")






# Run the app
if __name__ == '__main__':
    app.run( debug=True)
