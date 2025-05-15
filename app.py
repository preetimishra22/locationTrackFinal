# from flask import Flask,flash, render_template, request, session, url_for, redirect
# import pymysql
# from werkzeug.utils import secure_filename
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# import pathlib
# import smtplib
# import os
# import geocoder
# import requests
# import pandas as pd
# app = Flask(__name__)
# app.secret_key = 'any random string'

# # Replace 'YOUR_API_KEY' with your actual Google Maps API key
# GOOGLE_MAPS_API_KEY = 'AIzaSyDwaXa3JZsFqv71812tm1k5FokRzLrX0RM'

# def dbConnection():
#     connection = pymysql.connect(host="localhost", user="root", password="root", database="track&go")
#     return connection


# def dbClose():
#     try:
#         dbConnection().close()
#     except:
#         print("Something went wrong in Close DB Connection")
        
                       
# con = dbConnection()
# cursor = con.cursor()

# @app.route('/')
# def main():
#     return render_template('main.html')

# # @app.route('/')
# # def index():
# #     return render_template('index.html')  # Render a page to ask for location

# @app.route('/index')
# def index():
#     try:
#         if(session['user'] is not None):
#             current_location = get_current_location()
#             if current_location:
#                 latitude, longitude = current_location
#             # user = session["user"]
#                 con = dbConnection()
#                 cursor = con.cursor()
#                 cursor.execute("SELECT * FROM feedback")
#                 result1 = cursor.fetchall()
#                 return render_template('index.html',result1=result1, latitude=latitude, longitude=longitude, api_key=GOOGLE_MAPS_API_KEY)
#         else:
#             return render_template('login.html')
#     except:
#         return redirect(url_for('login'))

# # Logout route
# @app.route('/logout')
# def logout():
#     session.pop('user', None)  # Remove user from session
#     # flash('You have been logged out.', 'info')
#     return redirect(url_for('login'))



# @app.route('/contact', methods=['POST', 'GET'])
# def contact():
#     try:
#         if(session['user'] is not None):
#             if request.method == "POST":
#                 username = request.form.get("name")
#                 emailaddress = request.form.get("email")
#                 subject = request.form.get("subject")
#                 message = request.form.get("message")
                
#                 print(username,emailaddress,subject,message)
#                 con = dbConnection()
#                 cursor = con.cursor()
#                 sql2 = "INSERT INTO contact(username,email,subject,message) VALUES (%s, %s, %s, %s)"
#                 val2 = (str(username), str(emailaddress), str(subject), str(message))
#                 cursor.execute(sql2, val2)
#                 con.commit()
#                 return render_template('contact.html')  
#             return render_template('contact.html')
#     except:
#         return redirect(url_for('login'))


# @app.route('/about')
# def about():
#     try:
#         if(session['user'] is not None):
#             return render_template('about.html')
#     except:
#         return redirect(url_for('login'))

# @app.route('/register', methods=['POST', 'GET'])
# def register():
#     if request.method == "POST":
#        username = request.form.get("Username")
#        emailaddress = request.form.get("Email")
#        phoneno = request.form.get("Contact")
#        password = request.form.get("Password")
       
#        con = dbConnection()
#        cursor = con.cursor()
#        sql2 = "INSERT INTO register(Username,Email,Contact,Password) VALUES (%s, %s, %s, %s)"
#        val2 = (str(username), str(emailaddress), str(phoneno), str(password))
#        cursor.execute(sql2, val2)
#        con.commit()
#        return render_template('login.html')
    
#     return render_template('register.html')

# @app.route('/login', methods=['POST', 'GET'])
# def login():
#     if request.method == "POST":
#            username = request.form.get("Username")
#            print("username", username)
#            password = request.form.get("Password")
#            con = dbConnection()
#            cursor = con.cursor()
#            cursor.execute('SELECT * FROM register WHERE Username = %s AND Password = %s', (username, password))
#            result = cursor.fetchone()
#            print("result", result)
#            if result:
#                session['user'] = result[0]
#                session['user_email'] = result[1]  # Store email in session
#                return redirect(url_for('index'))

#            else:
#                msg = 'Incorrect username/password!'
#                return msg
#                return render_template('login.html')
#     return render_template('login.html')


# @app.route('/services')
# def services():
#     try:
#         if(session['user'] is not None):
#             # Read CSV data
#             data = pd.read_csv('static/wap.csv')
#             print(data)
#         # Get longitude and latitude values
#             longitude = data['long'].tolist()
#             print(longitude)
#             latitude = data['lat'].tolist()
            
            
#             return render_template('services.html', longitude=longitude, latitude=latitude,api_key=GOOGLE_MAPS_API_KEY)
#     except:
#         return redirect(url_for('login'))
  



# @app.route('/servicedetails', methods=['POST', 'GET'])
# def servicedetails():
#     try:
#         if(session['user'] is not None):
#             if request.method == "POST":
#                 name = request.form.get("name")
#                 email = request.form.get("email")
#                 Contact = request.form.get("Contact")
#                 Address = request.form.get("Address")
#                 subject = request.form.get("subject")
                
#                 con = dbConnection()
#                 cursor = con.cursor()
#                 sql2 = "INSERT INTO feedback(name,email,Contact,Address,subject) VALUES (%s, %s, %s, %s, %s)"
#                 val2 = (str(name), str(email), str(Contact), str(Address), str(subject))
#                 cursor.execute(sql2, val2)
#                 con.commit()
#                 return render_template('service-details.html')  
#             return render_template('service-details.html')
#     except:
#         return redirect(url_for('login'))


# def get_nearby_places(latitude, longitude, keyword):
#     url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius=5000&keyword={keyword}&key={GOOGLE_MAPS_API_KEY}"
#     response = requests.get(url)
#     data = response.json()
#     return data.get('results', [])

    
    
# @app.route('/sampleinnerpage')
# def sampleinnerpage():
#     current_location = get_current_location()
#     if current_location:
#         latitude, longitude = current_location

#         hospitals = get_nearby_places(latitude, longitude, 'hospital')
#         hotels = get_nearby_places(latitude, longitude, 'hotel')
        
#         return render_template('sample-inner-page.html', api_key=GOOGLE_MAPS_API_KEY, hospitals=hospitals, hotels=hotels)


# @app.route('/pricing')
# def pricing():
#     # Read CSV data
#     data = pd.read_csv('static/bad_wap.csv')

#     # Extract data
#     longitude = data['long'].tolist()
#     latitude = data['lat'].tolist()
#     wap = data['wap'].tolist()
#     count = data['count'].tolist()

#     return render_template('pricing.html', longitude=longitude, latitude=latitude, api_key=GOOGLE_MAPS_API_KEY, wap=wap, count=count)

# @app.route('/getaquote')
# def getaquote():
#     return render_template('get-a-quote.html')

# def get_current_location():
#     g = geocoder.ip('me')
#     if g.latlng:
#         return g.latlng
#     else:
#         return None

# def get_nearby_hospitals(latitude, longitude):
#     url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius=1500&type=hospital&key={GOOGLE_MAPS_API_KEY}"
#     response = requests.get(url)
#     data = response.json()
#     print(data)

#     if data.get("status") == "REQUEST_DENIED":
#         return None

#     return data.get("results", [])

# def get_nearby_hostel(latitude, longitude):
#     url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius=1500&type=lodging&key={GOOGLE_MAPS_API_KEY}"
#     response = requests.get(url)
#     data = response.json()
#     print(data)

#     if data.get("status") == "REQUEST_DENIED":
#         return None

#     return data.get("results", [])



# @app.route('/hospitals')
# def hospitals():
#     try:
#         if(session['user'] is not None):
#             current_location = get_current_location()
#             if current_location:
#                 latitude, longitude = current_location
#                 hospitals = get_nearby_hospitals(latitude, longitude)
#                 print(hospitals)
#                 return render_template('hospitals.html', latitude=latitude, longitude=longitude, api_key=GOOGLE_MAPS_API_KEY, hospitals=hospitals)
#             else:
#                 return "Could not determine current location."
#     except:
#         return redirect(url_for('login'))

# @app.route('/hostel')
# def hostel():
#     try:
#         if(session['user'] is not None):
#             latitude = request.args.get('latitude')
#             longitude = request.args.get('longitude')
#             if latitude and longitude:
#                 hostel = get_nearby_hostel(latitude, longitude)
#                 return render_template('hostel.html', latitude=latitude, longitude=longitude, api_key=GOOGLE_MAPS_API_KEY, hostel=hostel)
#             else:
#                 return "Could not determine current location."
#     except:
#         return redirect(url_for('login'))


# @app.route('/restaurants')
# def restaurants():
#     try:
#         if(session['user'] is not None):
#             current_location = get_current_location()
#             if current_location:
#                 latitude, longitude = current_location
#                 restaurants = get_nearby_places(latitude, longitude, 'restaurant')
#                 return render_template('restaurants.html', latitude=latitude, longitude=longitude, api_key=GOOGLE_MAPS_API_KEY, restaurants=restaurants)
#             else:
#                 return "Could not determine current location."
#     except:
#         return redirect(url_for('login'))


# @app.route('/malls')
# def malls():
#     try:
#         if(session['user'] is not None):
#             current_location = get_current_location()
#             if current_location:
#                 latitude, longitude = current_location
#                 malls = get_nearby_places(latitude, longitude, 'mall')
#                 return render_template('malls.html', latitude=latitude, longitude=longitude, api_key=GOOGLE_MAPS_API_KEY, malls=malls)
#             else:
#                 return "Could not determine current location."
#     except:
#         return redirect(url_for('login'))


# @app.route('/parks')
# def parks():
#     try:
#         if(session['user'] is not None):
#             current_location = get_current_location()
#             if current_location:
#                 latitude, longitude = current_location
#                 parks = get_nearby_places(latitude, longitude, 'park')
#                 return render_template('parks.html', latitude=latitude, longitude=longitude, api_key=GOOGLE_MAPS_API_KEY, parks=parks)
#             else:
#                 return "Could not determine current location."
#     except:
#         return redirect(url_for('login'))


# @app.route('/departmental_stores')
# def departmental_stores():
#     try:
#         if(session['user'] is not None):
#             current_location = get_current_location()
#             if current_location:
#                 latitude, longitude = current_location
#                 stores = get_nearby_places(latitude, longitude, 'departmental store')
#                 return render_template('departmental_stores.html', latitude=latitude, longitude=longitude, api_key=GOOGLE_MAPS_API_KEY, stores=stores)
#             else:
#                 return "Could not determine current location."
#     except:
#         return redirect(url_for('login'))


# @app.route('/police_stations')
# def police_stations():
#     try:
#         if(session['user'] is not None):
#             current_location = get_current_location()
#             if current_location:
#                 latitude, longitude = current_location
#                 police_stations = get_nearby_places(latitude, longitude, 'police station')
#                 return render_template('police_stations.html', latitude=latitude, longitude=longitude, api_key=GOOGLE_MAPS_API_KEY, police_stations=police_stations)
#             else:
#                 return "Could not determine current location."
#     except:
#         return redirect(url_for('login'))


# @app.route('/send_email', methods = ['POST', 'GET'])
# def send_email_to_user():
#     user_email = session.get('user_email')

#     if not user_email:
#         flash("You must be logged in to receive an email.")
#         return redirect(url_for('login'))

#     try:
#         sender_email = "pm4592108@gmail.com"
#         sender_password = "E17qQ1EJ@m-_OFn"  # Use app password if 2FA is on

#         # Email content
#         message = MIMEMultipart()
#         message["From"] = sender_email
#         message["To"] = user_email
#         message["Subject"] = "Thank you for contacting TRACK&GO!"

#         body = "Hi there,\n\nThanks for reaching out to TRACK&GO. We have received your message and will get back to you shortly.\n\nBest regards,\nTRACK&GO Team"
#         message.attach(MIMEText(body, "plain"))

#         # Gmail SMTP
#         server = smtplib.SMTP("smtp.gmail.com", 587)
#         server.starttls()
#         server.login(sender_email, sender_password)
#         server.send_message(message)
#         server.quit()

#         return "Email sent successfully to {}".format(user_email)

#     except Exception as e:
#         print(sender_email, sender_password)
#         return f"Error sending email: {str(e)}"

# ################################################################################################################################
# if __name__ == '__main__':
#     app.run(debug=True)
#     # app.run('0.0.0.0')



from flask import Flask, flash, render_template, request, session, url_for, redirect
import pymysql
from werkzeug.utils import secure_filename
import geocoder
import requests
import pandas as pd
import json
import pickle
import datetime

app = Flask(__name__)
app.secret_key = 'any random string'

# Replace with your actual Google Maps API key
GOOGLE_MAPS_API_KEY = 'AIzaSyDwaXa3JZsFqv71812tm1k5FokRzLrX0RM'

# DB Connection

def dbConnection():
    return pymysql.connect(host="localhost", user="root", password="root", database="track&go")


# Routes
@app.route('/')
def main():
    return render_template('main.html')

# @app.route('/index')
# def index():
#     if 'user' in session:
#         current_location = get_current_location()
#         latitude, longitude = current_location if current_location else (None, None)

#         # Log current location
#         user_email = session.get('user_email')
#         if latitude and longitude:
#             log_user_location(user_email, latitude, longitude)

#         # Get top 3 locations
#         top_locations = get_top_locations(user_email)

#         # Load feedback
#         con = dbConnection()
#         cursor = con.cursor()
#         cursor.execute("SELECT * FROM feedback")
#         result1 = cursor.fetchall()

#         return render_template('index.html',
#                                result1=result1,
#                                latitude=latitude,
#                                longitude=longitude,
#                                api_key=GOOGLE_MAPS_API_KEY,
#                                top_locations=get_location_name(latitude, longitude))
#     return redirect(url_for('login'))

@app.route('/index')
def index():
    if 'user' in session:
        user = session['user']
        user_email = session.get('user_email')

        current_location = get_current_location()
        latitude, longitude = current_location if current_location else (None, None)

        if latitude and longitude:
            log_user_location(user_email, latitude, longitude)

        # Predict city
        predicted_city = None
        try:
            # Load encoders and model
            with open('city_model.pkl', 'rb') as f:
                model = pickle.load(f)
            with open('city_encoder.pkl', 'rb') as f:
                city_encoder = pickle.load(f)
            with open('day_encoder.pkl', 'rb') as f:
                day_encoder = pickle.load(f)
            with open('user_encoder.pkl', 'rb') as f:
                user_encoder = pickle.load(f)

            current_day = datetime.today().strftime('%A')
            # testing
            # sunday_date = datetime(2025, 5, 25)
            # current_day = sunday_date.strftime('%A')
            day_enc = day_encoder.transform([current_day])[0]
            user_enc = user_encoder.transform([user_email])[0]

            X_input = [[user_enc, day_enc]]
            y_pred = model.predict(X_input)
            predicted_city = city_encoder.inverse_transform(y_pred)[0]

        except Exception as e:
            print(f"Prediction failed: {e}")
            predicted_city = "Unavailable"

        # Load feedback
        con = dbConnection()
        cursor = con.cursor()
        cursor.execute("SELECT * FROM feedback")
        result1 = cursor.fetchall()

        return render_template('index.html',
                               result1=result1,
                               latitude=latitude,
                               longitude=longitude,
                               api_key=GOOGLE_MAPS_API_KEY,
                               top_locations=get_location_name(latitude, longitude),
                               predicted_city=predicted_city)

    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/contact', methods=['POST', 'GET'])
def contact():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == "POST":
        username = request.form.get("name")
        emailaddress = request.form.get("email")
        subject = request.form.get("subject")
        message = request.form.get("message")
        con = dbConnection()
        cursor = con.cursor()
        cursor.execute("INSERT INTO contact(username,email,subject,message) VALUES (%s, %s, %s, %s)",
                       (username, emailaddress, subject, message))
        con.commit()
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html') if 'user' in session else redirect(url_for('login'))

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        username = request.form.get("Username")
        emailaddress = request.form.get("Email")
        phoneno = request.form.get("Contact")
        password = request.form.get("Password")
        con = dbConnection()
        cursor = con.cursor()
        cursor.execute("INSERT INTO register(Username,Email,Contact,Password) VALUES (%s, %s, %s, %s)",
                       (username, emailaddress, phoneno, password))
        con.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        username = request.form.get("Username")
        password = request.form.get("Password")
        print("username", username)
        con = dbConnection()
        cursor = con.cursor()
        cursor.execute('SELECT * FROM register WHERE Username = %s AND Password = %s', (username, password))
        result = cursor.fetchone()
        print(result)
        if result:
            session['user'] = result[0]
            session['user_email'] = result[1]
            return redirect(url_for('index'))
        flash('Incorrect username/password!', 'danger')
    return render_template('login.html')

@app.route('/services')
def services():
    if 'user' not in session:
        return redirect(url_for('login'))

    data = pd.read_csv('static/wap.csv')
    longitude = data['long'].tolist()
    latitude = data['lat'].tolist()
    return render_template('services.html', longitude=longitude, latitude=latitude, api_key=GOOGLE_MAPS_API_KEY)

@app.route('/servicedetails', methods=['POST', 'GET'])
def servicedetails():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        contact = request.form.get("Contact")
        address = request.form.get("Address")
        subject = request.form.get("subject")
        con = dbConnection()
        cursor = con.cursor()
        cursor.execute("INSERT INTO feedback(name,email,Contact,Address,subject) VALUES (%s, %s, %s, %s, %s)",
                       (name, email, contact, address, subject))
        con.commit()
    return render_template('service-details.html')

@app.route('/pricing')
def pricing():
    data = pd.read_csv('static/bad_wap.csv')
    return render_template('pricing.html',
                           longitude=data['long'].tolist(),
                           latitude=data['lat'].tolist(),
                           wap=data['wap'].tolist(),
                           count=data['count'].tolist(),
                           api_key=GOOGLE_MAPS_API_KEY)

@app.route('/getaquote')
def getaquote():
    return render_template('get-a-quote.html')

# Location Utilities
def get_current_location():
    g = geocoder.ip('me')
    return g.latlng if g.latlng else None

def get_nearby_places(latitude, longitude, keyword):
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius=5000&keyword={keyword}&key={GOOGLE_MAPS_API_KEY}"
    response = requests.get(url)
    return response.json().get('results', [])

@app.route('/sampleinnerpage')
def sampleinnerpage():
    current_location = get_current_location()
    if current_location:
        latitude, longitude = current_location
        return render_template('sample-inner-page.html',
                               api_key=GOOGLE_MAPS_API_KEY,
                               hospitals=get_nearby_places(latitude, longitude, 'hospital'),
                               hotels=get_nearby_places(latitude, longitude, 'hotel'))
    return redirect(url_for('login'))

# Dynamic Place Routes
@app.route('/<place_type>')
def show_places(place_type):
    place_keywords = {
        'hospitals': 'hospital',
        'hostel': 'lodging',
        'restaurants': 'restaurant',
        'malls': 'mall',
        'parks': 'park',
        'departmental_stores': 'departmental store',
        'police_stations': 'police station'
    }

    if 'user' not in session or place_type not in place_keywords:
        return redirect(url_for('login'))

    current_location = get_current_location()
    if current_location:
        latitude, longitude = current_location
        places = get_nearby_places(latitude, longitude, place_keywords[place_type])
        return render_template(f'{place_type}.html', latitude=latitude, longitude=longitude,
                               api_key=GOOGLE_MAPS_API_KEY, **{place_type: places})
    return "Could not determine current location."


import os
from collections import Counter

LOCATION_FILE = 'user_location_history.json'

def load_location_data():
    if not os.path.exists(LOCATION_FILE):
        return []
    with open(LOCATION_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_location_data(data):
    with open(LOCATION_FILE, 'w') as f:
        json.dump(data, f, indent=4)

from datetime import datetime

def log_user_location(email, lat, lng):
    data = load_location_data()
    # testing
    # sunday_date = datetime(2025, 5, 18)
    # current_day = sunday_date.strftime('%A')
    current_day = datetime.today().strftime('%A')
    city = get_location_name(lat, lng)  # or keep it None if unknown

    entry = {
        "user": email,
        "day": current_day,
        "lat": round(lat, 3),
        "lng": round(lng, 3),
        "city": city
    }

    data.append(entry)
    save_location_data(data)


def get_top_locations(email, top_n=3):
    data = load_location_data()
    if email not in data:
        return []
    loc_list = [(entry["lat"], entry["lng"]) for entry in data[email]]
    counter = Counter(loc_list)

    # Get location names
    top_locations = []
    for (lat, lng), count in counter.most_common(top_n):
        location_name = get_location_name(lat, lng)
        top_locations.append((location_name, count))

    return top_locations


def get_location_name(lat, lng):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&key={GOOGLE_MAPS_API_KEY}"
    response = requests.get(url)
    result = response.json()
    print('lat', lat, 'lng', lng, 'result', result)
    if result['status'] == 'OK':
        address_components = result['results'][0]['address_components']
        
        # Extracting specific address components (city, state, country)
        city = None
        state = None
        country = None
        
        for component in address_components:
            if 'locality' in component['types']:
                city = component['long_name']
            elif 'administrative_area_level_1' in component['types']:
                state = component['long_name']
            elif 'country' in component['types']:
                country = component['long_name']
        
        # Construct a more readable address
        location_name = f"{city}, {state}, {country}" if city and state and country else "Unknown Location"
        print(location_name)
        return location_name
    return "Unknown Location"



################################################################################################################################
if __name__ == '__main__':
    app.run(debug=True)
    # app.run('0.0.0.0')