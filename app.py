from flask import Flask, render_template, request, session, url_for, redirect
import pymysql
from werkzeug.utils import secure_filename
import pathlib
import os
import geocoder
import requests
import pandas as pd
app = Flask(__name__)
app.secret_key = 'any random string'

# Replace 'YOUR_API_KEY' with your actual Google Maps API key
GOOGLE_MAPS_API_KEY = 'AIzaSyDwaXa3JZsFqv71812tm1k5FokRzLrX0RM'

def dbConnection():
    connection = pymysql.connect(host="localhost", user="root", password="root", database="track&go")
    return connection


def dbClose():
    try:
        dbConnection().close()
    except:
        print("Something went wrong in Close DB Connection")
        
                       
con = dbConnection()
cursor = con.cursor()

@app.route('/')
def main():
    return render_template('main.html')

# @app.route('/')
# def index():
#     return render_template('index.html')  # Render a page to ask for location

@app.route('/index')
def index():
    try:
        if(session['user'] is not None):
            current_location = get_current_location()
            if current_location:
                latitude, longitude = current_location
            # user = session["user"]
                con = dbConnection()
                cursor = con.cursor()
                cursor.execute("SELECT * FROM feedback")
                result1 = cursor.fetchall()
                return render_template('index.html',result1=result1, latitude=latitude, longitude=longitude, api_key=GOOGLE_MAPS_API_KEY)
        else:
            return render_template('login.html')
    except:
        return redirect(url_for('login'))

# Logout route
@app.route('/logout')
def logout():
    session.pop('user', None)  # Remove user from session
    # flash('You have been logged out.', 'info')
    return redirect(url_for('login'))



@app.route('/contact', methods=['POST', 'GET'])
def contact():
    try:
        if(session['user'] is not None):
            if request.method == "POST":
                username = request.form.get("name")
                emailaddress = request.form.get("email")
                subject = request.form.get("subject")
                message = request.form.get("message")
                
                print(username,emailaddress,subject,message)
                con = dbConnection()
                cursor = con.cursor()
                sql2 = "INSERT INTO contact(username,email,subject,message) VALUES (%s, %s, %s, %s)"
                val2 = (str(username), str(emailaddress), str(subject), str(message))
                cursor.execute(sql2, val2)
                con.commit()
                return render_template('contact.html')  
            return render_template('contact.html')
    except:
        return redirect(url_for('login'))


@app.route('/about')
def about():
    try:
        if(session['user'] is not None):
            return render_template('about.html')
    except:
        return redirect(url_for('login'))

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "POST":
       username = request.form.get("Username")
       emailaddress = request.form.get("Email")
       phoneno = request.form.get("Contact")
       password = request.form.get("Password")
       
       con = dbConnection()
       cursor = con.cursor()
       sql2 = "INSERT INTO register(Username,Email,Contact,Password) VALUES (%s, %s, %s, %s)"
       val2 = (str(username), str(emailaddress), str(phoneno), str(password))
       cursor.execute(sql2, val2)
       con.commit()
       return render_template('login.html')
    
    return render_template('register.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
           username = request.form.get("Username")
           print("username", username)
           password = request.form.get("Password")
           con = dbConnection()
           cursor = con.cursor()
           cursor.execute('SELECT * FROM register WHERE Username = %s AND Password = %s', (username, password))
           result = cursor.fetchone()
           print("result", result)
           if result:
               session['user'] = result[0]
               return redirect(url_for('index'))

           else:
               msg = 'Incorrect username/password!'
               return msg
               return render_template('login.html')
    return render_template('login.html')


@app.route('/services')
def services():
    try:
        if(session['user'] is not None):
            # Read CSV data
            data = pd.read_csv('static/wap.csv')
            print(data)
        # Get longitude and latitude values
            longitude = data['long'].tolist()
            print(longitude)
            latitude = data['lat'].tolist()
            
            
            return render_template('services.html', longitude=longitude, latitude=latitude,api_key=GOOGLE_MAPS_API_KEY)
    except:
        return redirect(url_for('login'))
  



@app.route('/servicedetails', methods=['POST', 'GET'])
def servicedetails():
    try:
        if(session['user'] is not None):
            if request.method == "POST":
                name = request.form.get("name")
                email = request.form.get("email")
                Contact = request.form.get("Contact")
                Address = request.form.get("Address")
                subject = request.form.get("subject")
                
                con = dbConnection()
                cursor = con.cursor()
                sql2 = "INSERT INTO feedback(name,email,Contact,Address,subject) VALUES (%s, %s, %s, %s, %s)"
                val2 = (str(name), str(email), str(Contact), str(Address), str(subject))
                cursor.execute(sql2, val2)
                con.commit()
                return render_template('service-details.html')  
            return render_template('service-details.html')
    except:
        return redirect(url_for('login'))


def get_nearby_places(latitude, longitude, keyword):
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius=5000&keyword={keyword}&key={GOOGLE_MAPS_API_KEY}"
    response = requests.get(url)
    data = response.json()
    return data.get('results', [])

    
    
@app.route('/sampleinnerpage')
def sampleinnerpage():
    current_location = get_current_location()
    if current_location:
        latitude, longitude = current_location

        hospitals = get_nearby_places(latitude, longitude, 'hospital')
        hotels = get_nearby_places(latitude, longitude, 'hotel')
        
        return render_template('sample-inner-page.html', api_key=GOOGLE_MAPS_API_KEY, hospitals=hospitals, hotels=hotels)


@app.route('/pricing')
def pricing():
    # Read CSV data
    data = pd.read_csv('static/bad_wap.csv')

    # Extract data
    longitude = data['long'].tolist()
    latitude = data['lat'].tolist()
    wap = data['wap'].tolist()
    count = data['count'].tolist()

    return render_template('pricing.html', longitude=longitude, latitude=latitude, api_key=GOOGLE_MAPS_API_KEY, wap=wap, count=count)

@app.route('/getaquote')
def getaquote():
    return render_template('get-a-quote.html')

def get_current_location():
    g = geocoder.ip('me')
    if g.latlng:
        return g.latlng
    else:
        return None

def get_nearby_hospitals(latitude, longitude):
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius=1500&type=hospital&key={GOOGLE_MAPS_API_KEY}"
    response = requests.get(url)
    data = response.json()
    print(data)

    if data.get("status") == "REQUEST_DENIED":
        return None

    return data.get("results", [])

def get_nearby_hostel(latitude, longitude):
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius=1500&type=hotels&key={GOOGLE_MAPS_API_KEY}"
    response = requests.get(url)
    data = response.json()
    print(data)

    if data.get("status") == "REQUEST_DENIED":
        return None

    return data.get("results", [])



@app.route('/hospitals')
def hospitals():
    try:
        if(session['user'] is not None):
            current_location = get_current_location()
            if current_location:
                latitude, longitude = current_location
                hospitals = get_nearby_hospitals(latitude, longitude)
                print(hospitals)
                return render_template('hospitals.html', latitude=latitude, longitude=longitude, api_key=GOOGLE_MAPS_API_KEY, hospitals=hospitals)
            else:
                return "Could not determine current location."
    except:
        return redirect(url_for('login'))

@app.route('/hostel')
def hostel():
    try:
        if(session['user'] is not None):
            latitude = request.args.get('latitude')
            longitude = request.args.get('longitude')
            if latitude and longitude:
                hostel = get_nearby_hostel(latitude, longitude)
                return render_template('hostel.html', latitude=latitude, longitude=longitude, api_key=GOOGLE_MAPS_API_KEY, hostel=hostel)
            else:
                return "Could not determine current location."
    except:
        return redirect(url_for('login'))




################################################################################################################################
if __name__ == '__main__':
    app.run(debug=True)
    # app.run('0.0.0.0')