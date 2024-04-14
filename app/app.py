from flask import Flask, render_template, request, redirect, session
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

mysql_config = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "db": os.getenv("DB_NAME"),
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor,
}

@app.route('/register_staff', methods=['GET', 'POST'])
def register_staff():
    if request.method == 'POST':
        username = request.form['username']
        airline_name = request.form['airline_name']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        dob = request.form['dob']
        
        connection = pymysql.connect(**mysql_config)
        
        try:
            with connection.cursor() as cursor:
                query = """
                    INSERT INTO AirlineStaff
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (username, airline_name, password, first_name, last_name, dob))
            
                connection.commit()
                query = "SELECT * FROM AirlineStaff WHERE username = %s AND airline_name = %s AND password = %s"
                cursor.execute(query, (username, airline_name, password))
                user = cursor.fetchone()

            if user:
                session["username"] = user["username"]
                return redirect("/")
            else:
                error = "Invalid email or password"
                return render_template("login_staff.html", error=error)
        except Exception as E:
            return render_template("login_staff.html", error=E)        
        finally:
            connection.close()
    
    return render_template('register_staff.html')


@app.route('/register_user', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        building_number = request.form['building_number']
        street = request.form['street']
        city = request.form['city']
        state = request.form['state']
        zipcode = request.form['zipcode']
        passport_number = request.form['passport_number']
        passport_expiration = request.form['passport_expiration']
        passport_country = request.form['passport_country']
        dob = request.form['dob']
        
        connection = pymysql.connect(**mysql_config)
        
        try:
            with connection.cursor() as cursor:
                query = """
                    INSERT INTO Customers
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (email, password, first_name, last_name, building_number, street, city, state, zipcode, passport_number, passport_expiration, passport_country, dob))
                connection.commit() # I need to do this to save

                # just logging in again
                query = "SELECT * FROM Customers WHERE Email = %s AND password = %s"
                cursor.execute(query, (email, password))
                user = cursor.fetchone()

                if user:
                    session["email"] = user["email"]
                    return redirect("/")
                else:
                    error = "Invalid email or password"
                    return render_template("login_user.html", error=error)
        except Exception as E:
            return render_template("login_user.html", error=E)
        finally:
            connection.close()
    
    return render_template('register_user.html')

@app.route("/login_user", methods=["GET", "POST"])
def login_user():
    if "username" in session or "email" in session:
        return home()
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        connection = pymysql.connect(**mysql_config)
        try:
            with connection.cursor() as cursor:
                query = "SELECT * FROM Customers WHERE Email = %s AND password = %s"
                cursor.execute(query, (email, password))
                user = cursor.fetchone()

                if user:
                    session["email"] = user["email"]
                    return redirect("/")
                else:
                    error = "Invalid email or password"
                    return render_template("login_user.html", error=error)
        except Exception as E:
            return render_template("login_user.html", error=E)

        finally:
            connection.close()

    return render_template("login_user.html")


@app.route("/login_staff", methods=["GET", "POST"])
def login_staff():
    if "username" in session or "email" in session:
        return home()
    if request.method == "POST":
        username = request.form["username"]
        airline_name = request.form["airline_name"]
        password = request.form["password"]
        connection = pymysql.connect(**mysql_config)
        try:
            with connection.cursor() as cursor:
                query = "SELECT * FROM AirlineStaff WHERE username = %s AND airline_name = %s AND password = %s"
                cursor.execute(query, (username, airline_name, password))
                user = cursor.fetchone()

                if user:
                    session["username"] = user["username"]
                    return redirect("/")
                else:
                    error = "Invalid email or password"
                    return render_template("login_staff.html", error=error)
        except Exception as E:
            return render_template("login_staff.html", error=E)

        finally:
            connection.close()

    return render_template("login_staff.html")


@app.route("/logout", methods=["POST", "GET"])
def logout():
    session.clear()
    return redirect("/")

@app.route("/")
def home():
    if "email" in session:
        email = session["email"]

        connection = pymysql.connect(**mysql_config)

        try:
            with connection.cursor() as cursor:
                # I was silly with my fields
                query = """
                    SELECT 
                        f.Airline_Name, f.Identification, f.number, f.departure_date, f.departure_time,
                        f.arrival_date, f.arrival_time, f.base_price, f.status, f.isroundtrip,
                        f.departure_airport, f.arrival_airport
                    FROM 
                        Flight f
                    WHERE 
                        (f.Airline_Name, f.Identification, f.number, f.departure_date, f.departure_time) IN (
                            SELECT 
                                t.Airline_Name, t.Identification, t.Number, t.Depart_Date, t.Depart_Time
                            FROM 
                                Ticket t
                            WHERE 
                                t.Email = %s
                        )
                """
                cursor.execute(query, (email,))
                flights = cursor.fetchall()

                query_customer = """
                    SELECT 
                        first_name, last_name
                    FROM 
                        Customers
                    WHERE 
                        email = %s
                """
                cursor.execute(query_customer, (email,))
                customer = cursor.fetchone()

                query_ratings = """
                    SELECT 
                        airline_name, identification, number, departure_date, departure_time, rating, comment_ratings
                    FROM 
                        Ratings
                    WHERE 
                        email = %s
                """
                cursor.execute(query_ratings, (email,))
                ratings = cursor.fetchall()
                return render_template(
                    "home.html",
                    flights=flights,
                    first_name=customer["first_name"],
                    last_name=customer["last_name"],
                    ratings=ratings,
                )

        finally:
            connection.close()
    elif 'username' in session:
        return render_template(
                    "home.html",
                    first_name='testing',
                    last_name='testing',
                )
    else:
        return redirect("/login_user")


@app.route('/rate_flight', methods=['POST'])
def rate_flight():
    email = session['email']
    airline_name = request.form['airline_name']
    identification = request.form['identification']
    number = request.form['number']
    departure_date = request.form['departure_date']
    departure_time = request.form['departure_time']
    rating = request.form['rating']
    comment = request.form['comment']

    return redirect('/')

if __name__ == "__main__":
    app.run()
