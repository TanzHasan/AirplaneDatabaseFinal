from flask import Flask, render_template, request, redirect, session
import pymysql
import os
import datetime
from queries import *
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


@app.route("/register_staff", methods=["GET", "POST"])
def register_staff():
    if request.method == "POST":
        username = request.form["username"]
        airline_name = request.form["airline_name"]
        password = request.form["password"]
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        dob = request.form["dob"]

        connection = pymysql.connect(**mysql_config)

        try:
            with connection.cursor() as cursor:
                query = """
                    INSERT INTO AirlineStaff
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(
                    query,
                    (username, airline_name, password, first_name, last_name, dob),
                )

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

    return render_template("register_staff.html")


@app.route("/register_user", methods=["GET", "POST"])
def register_user():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        building_number = request.form["building_number"]
        street = request.form["street"]
        city = request.form["city"]
        state = request.form["state"]
        zipcode = request.form["zipcode"]
        passport_number = request.form["passport_number"]
        passport_expiration = request.form["passport_expiration"]
        passport_country = request.form["passport_country"]
        dob = request.form["dob"]

        if '@' not in email:
            return render_template("login_user.html", error="Bad email")

        connection = pymysql.connect(**mysql_config)

        try:
            with connection.cursor() as cursor:
                query = """
                    INSERT INTO Customers
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(
                    query,
                    (
                        email,
                        password,
                        first_name,
                        last_name,
                        building_number,
                        street,
                        city,
                        state,
                        zipcode,
                        passport_number,
                        passport_expiration,
                        passport_country,
                        dob,
                    ),
                )
                connection.commit()  # I need to do this to save

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

    return render_template("register_user.html")


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
    if "error" in session:
        error = session["error"]
        session["error"] = ""
    else:
        error = ""

    if "email" in session:
        email = session["email"]

        connection = pymysql.connect(**mysql_config)

        try:
            with connection.cursor() as cursor:
                today = datetime.date.today()
                tomorrow = today + datetime.timedelta(days=1)
                # I was silly with my fields
                query = customer_future_flights
                cursor.execute(query, (email, today))
                future_flights = cursor.fetchall()

                query = customer_future_flights
                cursor.execute(query, (email, tomorrow))
                cancellable_flights = cursor.fetchall()

                query = customer_past_flights
                cursor.execute(query, (email, today))
                past_flights = cursor.fetchall()

                query_customer = customer_name
                cursor.execute(query_customer, (email,))
                customer = cursor.fetchone()

                query_ratings = customer_rated_flights
                cursor.execute(query_ratings, (email,))
                ratings = cursor.fetchall()

                return render_template(
                    "home.html",
                    future_flights=future_flights,
                    past_flights=past_flights,
                    first_name=customer["first_name"],
                    last_name=customer["last_name"],
                    cancellable_flights=cancellable_flights,
                    ratings=ratings,
                    error=error,
                )

        finally:
            connection.close()

    elif "username" in session:
        return render_template(
            "home.html",
            first_name="testing",
            last_name="testing",
        )
    else:
        return render_template("home.html", login=True)


@app.route("/rate_flight", methods=["POST"])
def rate_flight():
    email = session["email"]
    airline_name = request.form["airline_name"]
    identification = request.form["identification"]
    number = request.form["number"]
    departure_date = request.form["departure_date"]
    departure_time = request.form["departure_time"]
    rating = request.form["rating"]
    comment = request.form["comment"]

    connection = pymysql.connect(**mysql_config)

    try:
        with connection.cursor() as cursor:
            query = customer_rated_check
            cursor.execute(query,
                (
                    email,
                    airline_name,
                    identification,
                    number,
                    departure_date,
                    departure_time,
                ),)
            
            rated = cursor.fetchone()

            if rated:
                query = customer_rated_delete
                cursor.execute(query,
                    (
                        email,
                        airline_name,
                        identification,
                        number,
                        departure_date,
                        departure_time,
                    ),)
                connection.commit()

            query = customer_rate
            cursor.execute(
                query,
                (
                    email,
                    airline_name,
                    identification,
                    number,
                    departure_date,
                    departure_time,
                    rating,
                    comment,
                ),
            )

        connection.commit()
    except Exception as E:
        session["error"] = str(E)
        return redirect("/")
    finally:
        connection.close()

    return redirect("/")

@app.route("/cancel_ticket", methods=["POST"])
def cancel_ticket():
    email = session["email"]

    ticket_id = request.form["Ticket_ID"]
    connection = pymysql.connect(**mysql_config)
    try:
        with connection.cursor() as cursor:
            flight_query = """
                SELECT 
                    Ticket_ID, Airline_Name, Identification, Number, Depart_Date, Depart_Time,
                    FirstName, LastName, DOB, CardType, CardNumber, CardExpiration, CardName
                FROM 
                    Ticket
                WHERE 
                    Ticket_ID = %s
            """
            cursor.execute(flight_query, (ticket_id,))
            flight_details = cursor.fetchone()

            delete_query = "DELETE FROM Ticket WHERE Ticket_ID = %s"
            cursor.execute(delete_query, (ticket_id,))
            connection.commit()

            if flight_details:
                insert_query = """
                    INSERT INTO Ticket (
                        Ticket_ID, Airline_Name, Identification, Number, Depart_Date, Depart_Time,
                        Email, FirstName, LastName, DOB, PurchaseDate, PurchaseTime, 
                        CardType, CardNumber, CardExpiration, CardName
                    )
                    VALUES (
                        %s, %s, %s, %s, %s, %s,
                        "None", %s, %s, %s, CURDATE(), CURTIME(),
                        %s, %s, %s, %s
                    )
                """
                insert_values = (
                    flight_details["Ticket_ID"],
                    flight_details["Airline_Name"],
                    flight_details["Identification"],
                    flight_details["Number"],
                    flight_details["Depart_Date"],
                    flight_details["Depart_Time"],
                    flight_details["FirstName"],
                    flight_details["LastName"],
                    flight_details["DOB"],
                    flight_details["CardType"],
                    flight_details["CardNumber"],
                    flight_details["CardExpiration"],
                    flight_details["CardName"]
                )
                cursor.execute(insert_query, insert_values)

            connection.commit()

    except Exception as E:
        session["error"] = str(E)
        return redirect("/")

    finally:
        connection.close()

    return redirect("/")

@app.route('/search_flights', methods=['GET', 'POST'])
def search_flights():
    if request.method == 'POST':
        source = request.form['source']
        source_type = request.form['source_type']
        destination = request.form['destination']
        destination_type = request.form['destination_type']
        departure_date = request.form['departure_date']
        trip_type = request.form['trip_type']
        return_date = request.form['return_date'] if trip_type == 'round_trip' else None

        connection = pymysql.connect(**mysql_config)

        try:
            with connection.cursor() as cursor:
                if trip_type != 'round_trip':
                    query = """
                        SELECT 
                            f.Airline_Name, f.Identification, f.number, f.departure_date, f.departure_time,
                            f.arrival_date, f.arrival_time, f.base_price, f.status, f.isroundtrip,
                            f.departure_airport, f.arrival_airport
                        FROM 
                            Flight f, Airport a, Airport b
                        WHERE 
                            f.departure_airport = a.airport_code AND
                            f.arrival_airport = b.airport_code AND
                            f.departure_date = %s AND
                            f.departure_date >= %s
                    """
                    params = [departure_date, datetime.date.today()]

                    if source_type == 'airport':
                        query += " AND f.departure_airport = %s"
                        params.append(source)
                    else:
                        query += " AND a.city = %s"
                        params.append(source)

                    if destination_type == 'airport':
                        query += " AND f.arrival_airport = %s"
                        params.append(destination)
                    else:
                        query += " AND b.city = %s"
                        params.append(destination)


                    cursor.execute(query, params)
                    flights = cursor.fetchall()
                    if 'email' in session:
                        return render_template('search_results_user.html', flights=flights, rt=False)
                    elif 'username' in session:
                        return render_template('search_results_staff.html', flights=flights, rt=False)
                    else:
                        return render_template('search_results.html', flights=flights, rt=False)
                else:
                    query = """
                        SELECT 
                            f.Airline_Name, f.Identification, f.number, f.departure_date, f.departure_time,
                            f.arrival_date, f.arrival_time, f.base_price, f.status, f.isroundtrip,
                            f.departure_airport, f.arrival_airport
                        FROM 
                            ReturnFlight f, Airport a, Airport b
                        WHERE 
                            f.departure_airport = a.airport_code AND
                            f.arrival_airport = b.airport_code AND
                            f.departure_date = %s AND
                            f.Returndeparture_date = %s AND
                            f.departure_date >= %s
                    """
                    params = [departure_date, return_date, datetime.date.today()]

                    if source_type == 'airport':
                        query += " AND f.departure_airport = %s"
                        params.append(source)
                    else:
                        query += " AND a.city = %s"
                        params.append(source)

                    if destination_type == 'airport':
                        query += " AND f.arrival_airport = %s"
                        params.append(destination)
                    else:
                        query += " AND b.city = %s"
                        params.append(destination)
                    if 'email' in session:
                        return render_template('search_results_user.html', flights=flights, rt=True)
                    elif 'username' in session:
                        return render_template('search_results_staff.html', flights=flights, rt=True)
                    else:
                        return render_template('search_results.html', flights=flights, rt=True)
        
        finally:
            connection.close()

    return render_template('search_flights.html')

if __name__ == "__main__":
    app.run()
