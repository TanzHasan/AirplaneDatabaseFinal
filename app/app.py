from flask import Flask, render_template, request, redirect, session
import pymysql
import os
import datetime
from queries import *
from dotenv import load_dotenv
import random

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
        email_addresses = request.form.getlist("email_address")
        phone_numbers = request.form.getlist("phone_numbers")

        connection = pymysql.connect(**mysql_config)
        try:
            with connection.cursor() as cursor:
                query = """
                    INSERT INTO AirlineStaff
                    VALUES (%s, %s, MD5(%s), %s, %s, %s)
                """
                cursor.execute(
                    query, (username, airline_name, password, first_name, last_name, dob)
                )

                for email_address in email_addresses:
                    query = """
                        INSERT INTO EmailAddress
                        VALUES (%s, %s, %s)
                    """
                    cursor.execute(query, (username, airline_name, email_address))
                
                for phone_number in phone_numbers:
                    query = """
                        INSERT INTO PhoneNumber
                        VALUES (%s, %s, %s)
                    """
                    cursor.execute(query, (username, airline_name, phone_number))

                connection.commit()

                query = "SELECT * FROM AirlineStaff WHERE username = %s AND airline_name = %s AND password = MD5(%s)"
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
        phone_numbers = request.form.getlist("phone_numbers")

        if "@" not in email:
            return render_template("login_user.html", error="Bad email")

        connection = pymysql.connect(**mysql_config)

        try:
            with connection.cursor() as cursor:
                query = """
                    INSERT INTO Customers
                    VALUES (%s, MD5(%s), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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

                for phone_number in phone_numbers:
                    query = """
                        INSERT INTO Customer_Phone
                        VALUES (%s, %s)
                    """
                    cursor.execute(query, (email, phone_number))

                connection.commit()  # I need to do this to save

                # just logging in again
                query = (
                    "SELECT * FROM Customers WHERE Email = %s AND password = MD5(%s)"
                )
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
        return redirect("/")
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        connection = pymysql.connect(**mysql_config)
        try:
            with connection.cursor() as cursor:
                query = (
                    "SELECT * FROM Customers WHERE Email = %s AND password = MD5(%s)"
                )
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
        return redirect("/")
    if request.method == "POST":
        username = request.form["username"]
        airline_name = request.form["airline_name"]
        password = request.form["password"]
        connection = pymysql.connect(**mysql_config)
        try:
            with connection.cursor() as cursor:
                query = "SELECT * FROM AirlineStaff WHERE username = %s AND airline_name = %s AND password = MD5(%s)"
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

    connection = pymysql.connect(**mysql_config)
    if "email" in session:
        email = session["email"]

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
                    "home_user.html",
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
        try:
            with connection.cursor() as cursor:
                query = "SELECT * FROM AirlineStaff WHERE username = %s"
                cursor.execute(query, (session["username"]))
                staffinfo = cursor.fetchone()
            return render_template(
                "home_staff.html",
                first_name=staffinfo["first_name"],
                last_name=staffinfo["last_name"],
                error=error,
            )
        except Exception as E:
            session["error"] = str(E)
            return render_template(
                "home_staff.html",
                first_name="Something",
                last_name="Went Wrong",
                error=error,
            )
        finally:
            connection.close()
    else:
        return render_template("home_user.html", login=True, error=error)


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
            cursor.execute(
                query,
                (
                    email,
                    airline_name,
                    identification,
                    number,
                    departure_date,
                    departure_time,
                ),
            )

            rated = cursor.fetchone()

            if rated:
                query = customer_rated_delete
                cursor.execute(
                    query,
                    (
                        email,
                        airline_name,
                        identification,
                        number,
                        departure_date,
                        departure_time,
                    ),
                )
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

            delete_query = "DELETE FROM Ticket WHERE Ticket_ID = %s"
            cursor.execute(delete_query, (ticket_id,))
            connection.commit()
            connection.commit()

    except Exception as E:
        session["error"] = str(E)
        return redirect("/")

    finally:
        connection.close()

    return redirect("/")


@app.route("/search_flights", methods=["GET", "POST"])
def search_flights():
    if request.method == "POST":
        source = request.form["source"]
        source_type = request.form["source_type"]
        destination = request.form["destination"]
        destination_type = request.form["destination_type"]
        departure_date = request.form["departure_date"]
        trip_type = request.form["trip_type"]
        return_date = request.form["return_date"] if trip_type == "round_trip" else None

        connection = pymysql.connect(**mysql_config)

        try:
            with connection.cursor() as cursor:
                query = """
                    SELECT 
                    f.Airline_Name, f.Identification, f.number, f.departure_date, f.departure_time, 
                    f.arrival_date, f.arrival_time, f.base_price, f.status, f.isroundtrip, 
                    f.departure_airport, f.arrival_airport
                FROM 
                    FROM Flight f, Airport a, Airport b WHERE f.departure_airport = a.airport_code AND f.arrival_airport = b.airport_code AND
                    f.departure_date = %s 
                    AND f.departure_date >= %s
                    AND (
                        a.country = b.country 
                        OR (
                            (a.type = 'international' OR a.type = 'both') 
                            AND (b.type = 'international' OR b.type = 'both')
                        )
                    )
                """
                params = [departure_date, str(datetime.date.today())]

                if source_type == "airport":
                    query += " AND f.departure_airport = %s"
                    params.append(source)
                else:
                    query += " AND a.city = %s"
                    params.append(source)

                if destination_type == "airport":
                    query += " AND f.arrival_airport = %s"
                    params.append(destination)
                else:
                    query += " AND b.city = %s"
                    params.append(destination)

                cursor.execute(query, params)
                print(query)
                print(params)
                outbound_flights = cursor.fetchall()
                if trip_type == "round_trip":
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
                            AND (
                                a.country = b.country 
                                OR (
                                    (a.type = 'international' OR a.type = 'both') 
                                    AND (b.type = 'international' OR b.type = 'both')
                                )
                            )
                    """
                    params = [return_date, departure_date]

                    if destination_type == "airport":
                        query += " AND f.departure_airport = %s"
                        params.append(destination)
                    else:
                        query += " AND a.city = %s"
                        params.append(destination)

                    if source_type == "airport":
                        query += " AND f.arrival_airport = %s"
                        params.append(source)
                    else:
                        query += " AND b.city = %s"
                        params.append(source)

                    cursor.execute(query, params)
                    return_flights = cursor.fetchall()
                else:
                    return_flights = None

                if "email" in session:
                    return render_template(
                        "search_results_user.html",
                        outbound_flights=outbound_flights,
                        return_flights=return_flights,
                        rt=trip_type == "round_trip",
                    )
                elif "username" in session:
                    return render_template(
                        "search_results_staff.html",
                        outbound_flights=outbound_flights,
                        return_flights=return_flights,
                        rt=trip_type == "round_trip",
                    )
                else:
                    return render_template(
                        "search_results.html",
                        outbound_flights=outbound_flights,
                        return_flights=return_flights,
                        rt=trip_type == "round_trip",
                    )

        finally:
            connection.close()

    return render_template("search_flights.html")


@app.route("/purchase_ticket", methods=["POST"])
def purchase_ticket():
    if "email" not in session:
        session["error"] = "Please log in to purchase a ticket."
        return redirect("/")

    email = session["email"]
    airline = request.form["airline"]
    flight_number = request.form["flight_number"]
    departure_date = request.form["departure_date"]
    departure_time = request.form["departure_time"]
    DOB = request.form["DOB"]
    CardType = request.form["CardType"]
    CardNumber = request.form["CardNumber"]
    CardExpiration = request.form["CardExpiration"]
    CardName = request.form["CardName"]
    
    connection = pymysql.connect(**mysql_config)

    try:
        with connection.cursor() as cursor:

            query_customer = customer_name
            cursor.execute(query_customer, (email,))
            customer = cursor.fetchone()
            
            first_name = customer["first_name"]
            last_name = customer["last_name"]
            query = """
                SELECT *
                FROM Flight
                WHERE Airline_Name = %s AND number = %s AND departure_date = %s
            """
            cursor.execute(query, (airline, flight_number, departure_date))
            flight = cursor.fetchone()

            if flight:
            
                a = """
                SELECT Identification from Flight
                WHERE Airline_Name = %s AND number = %s
                """
                cursor.execute(a, (airline, flight_number))
                identification = cursor.fetchone()['Identification']
                b = '''
                SELECT numseats from Airplane
                WHERE Airline_Name = %s AND Identification = %s
                '''
                cursor.execute(b, (airline, identification))
                print(airline, identification)
                seats = cursor.fetchone()

                c = '''
                    SELECT COUNT(*) as amount
                    FROM Ticket
                    WHERE Airline_Name = %s AND Number = %s AND Depart_Date = %s
                '''
                cursor.execute(c, (airline, flight_number, departure_date))
                seen = cursor.fetchone()
                print("Number of seats:", seats)
                print("Number of tickets:", seen)
                
                if seats['numseats'] > seen['amount']:
                    surge = 1 if seats['numseats']*.8 >= seen['amount'] else 1.25
                    while True:
                        ticket_id = random.randint(1, 1000000)  # Adjust the range as needed
                        query_check_ticket_id = """
                            SELECT COUNT(*) as count
                            FROM Ticket
                            WHERE Ticket_ID = %s
                        """
                        cursor.execute(query_check_ticket_id, (ticket_id,))
                        result = cursor.fetchone()
                        if result['count'] == 0:
                            break
                    item = """
                        INSERT INTO Ticket
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURDATE(), CURTIME(), %s, %s, %s, %s, %s)
                    """
                    cursor.execute(
                            item,
                            (
                                ticket_id,
                                airline,
                                identification,
                                float(flight_number),
                                departure_date,
                                departure_time,
                                session["email"],
                                first_name,
                                last_name,
                                DOB,
                                CardType,
                                CardNumber,
                                str(CardExpiration),
                                CardName,
                                flight["base_price"]*surge,
                            ),
                        )
                    connection.commit()
                    return redirect("/")
                else:
                    print(f"""{seats['numseats']} > {seen['amount']}""")
                    session["error"] = "No Tickets available"
                    return redirect("/")
            else:
                session["error"] = "Flight not found"
                return redirect("/")

    finally:
        connection.close()


@app.route("/see_flight_status", methods=["GET", "POST"])
def see_flight_status():
    if request.method == "POST":
        airline = request.form["airline"]
        flightnum = request.form["flightnum"]
        departure_arrival = request.form["departure_arrival"]
        airport = request.form["airport"]

        connection = pymysql.connect(**mysql_config)
        try:
            with connection.cursor() as cursor:
                query = """
                SELECT f.status
                FROM Flight f
                WHERE f.Airline_Name = %s AND f.number = %s
                """
                if departure_arrival == "departure":
                    query += " AND f.departure_airport = %s"
                else:
                    query += " AND f.arrival_airport = %s"

                cursor.execute(query, (airline, flightnum, airport))

                result = cursor.fetchone()

                if result:
                    print(result)
                    flight_status = result["status"]

                    return render_template(
                        "flight_status.html", flight_status=flight_status
                    )
                else:
                    return render_template(
                        "flight_status.html", error="Flight not found"
                    )

        except Exception as E:
            session["error"] = str(E)
            return redirect("/")
        finally:
            connection.close()

    return render_template("flight_status.html")


@app.route("/spending", methods=["GET", "POST"])
def spending():
    if "email" not in session:
        session["error"] = "Must be logged in"
        return redirect("/")

    email = session["email"]

    if request.method == "POST":
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
    else:
        end_date = datetime.date.today()
        start_date = end_date - datetime.timedelta(days=365)

    connection = pymysql.connect(**mysql_config)

    try:
        with connection.cursor() as cursor:
            query = """
                SELECT SUM(price) AS total_spent
                FROM Ticket
                WHERE email = %s AND PurchaseDate BETWEEN %s AND %s
            """

            cursor.execute(query, (email, start_date, end_date))
            total_spent = cursor.fetchone()["total_spent"]

            query = """
                SELECT YEAR(PurchaseDate) AS year, MONTH(PurchaseDate) AS month, SUM(price) AS total_spent
                FROM Ticket
                WHERE email = %s AND PurchaseDate BETWEEN %s AND %s
                GROUP BY YEAR(PurchaseDate), MONTH(PurchaseDate)
                ORDER BY YEAR(PurchaseDate), MONTH(PurchaseDate)
            """
            cursor.execute(query, (email, start_date, end_date))
            monthly_spending = cursor.fetchall()

        return render_template(
            "spending.html",
            total_spent=total_spent,
            monthly_spending=monthly_spending,
            start_date=start_date,
            end_date=end_date,
        )

    finally:
        connection.close()


@app.route("/staff_view_flights", methods=["GET", "POST"])
def staff_view_flights():
    if "username" not in session:
        return redirect("/login")

    username = session["username"]

    connection = pymysql.connect(**mysql_config)
    try:
        with connection.cursor() as cursor:
            query = "SELECT airline_name FROM AirlineStaff WHERE username = %s"
            cursor.execute(query, (username,))
            airline = cursor.fetchone()["airline_name"]
    except Exception as E:
        session["error"] = str(E)
        return redirect("/")
    finally:
        connection.close()

    if request.method == "POST":
        start_date = request.form["start_date"]
        end_date = request.form["end_date"]
        source = request.form["source"]
        destination = request.form["destination"]
    else:
        end_date = datetime.date.today() + datetime.timedelta(days=30)
        start_date = datetime.date.today()
        source = ""
        destination = ""

    connection = pymysql.connect(**mysql_config)
    try:
        with connection.cursor() as cursor:
            query = """
                SELECT *
                FROM Flight
                WHERE Airline_Name = %s AND departure_date BETWEEN %s AND %s
            """
            params = [airline, start_date, end_date]

            if source:
                query += " AND departure_airport = %s"
                params.append(source)

            if destination:
                query += " AND arrival_airport = %s"
                params.append(destination)

            cursor.execute(query, params)
            flights = cursor.fetchall()
            for flight in flights:
                query = """
                    SELECT AVG(rating) AS average_rating
                    FROM Ratings
                    WHERE airline_name = %s AND number = %s AND departure_date = %s AND departure_time = %s
                """
                cursor.execute(
                    query,
                    (
                        flight["Airline_Name"],
                        flight["number"],
                        flight["departure_date"],
                        flight["departure_time"],
                    ),
                )
                result = cursor.fetchone()
                flight["average_rating"] = (
                    result["average_rating"] if result["average_rating"] else "N/A"
                )

        return render_template(
            "staff_view_flights.html",
            flights=flights,
            start_date=start_date,
            end_date=end_date,
            source=source,
            destination=destination,
        )
    except Exception as E:
        session["error"] = str(E)
        return redirect("/")
    finally:
        connection.close()


@app.route("/staff_view_customers", methods=["GET", "POST"])
def staff_view_customers():
    if "username" not in session:
        return redirect("/login")

    if request.method == "POST":
        airline_name = request.form["airline_name"]
        flight_number = request.form["flight_number"]
        departure_date = request.form["departure_date"]
        departure_time = request.form["departure_time"]

        connection = pymysql.connect(**mysql_config)
        connection = pymysql.connect(**mysql_config)
        try:
            with connection.cursor() as cursor:
                query = """
                    SELECT c.email, c.first_name, c.last_name
                    FROM Ticket t
                    JOIN Customers c ON t.email = c.email
                    WHERE t.Airline_Name = %s AND t.Number = %s AND t.Depart_Date = %s AND t.Depart_Time = %s
                """
                cursor.execute(
                    query, (airline_name, flight_number, departure_date, departure_time)
                )
                customers = cursor.fetchall()

            return render_template(
                "staff_view_customers.html",
                customers=customers,
                airline_name=airline_name,
                flight_number=flight_number,
                departure_date=departure_date,
                departure_time=departure_time,
            )
        except Exception as E:
            session["error"] = str(E)
            return redirect("/")
        finally:
            connection.close()

    return redirect("/")


@app.route("/create_flight", methods=["GET", "POST"])
def create_flight():
    if "username" not in session:
        session["error"] = "Must be logged in as staff"
        return redirect("/")

    username = session["username"]

    connection = pymysql.connect(**mysql_config)
    try:
        with connection.cursor() as cursor:
            query = "SELECT airline_name FROM AirlineStaff WHERE username = %s"
            cursor.execute(query, (username,))
            airline_name = cursor.fetchone()["airline_name"]
    except Exception as E:
        session["error"] = str(E)
        return redirect("/")
    finally:
        connection.close()

    if request.method == "POST":
        flight_number = request.form["flight_number"]
        identification = request.form["identification"]
        departure_airport = request.form["departure_airport"]
        arrival_airport = request.form["arrival_airport"]
        departure_date = request.form["departure_date"]
        departure_time = request.form["departure_time"]
        arrival_date = request.form["arrival_date"]
        arrival_time = request.form["arrival_time"]
        base_price = request.form["base_price"]
        status = "normal" if request.form["status"] == "On Time" else "Delayed"
        isroundtrip = "isroundtrip" in request.form

        connection = pymysql.connect(**mysql_config)
        try:
            with connection.cursor() as cursor:
                query = "SELECT type FROM Airport WHERE airport_code = %s"
                cursor.execute(query, (departure_airport,))
                departure_airport_type = cursor.fetchone()["type"]

                cursor.execute(query, (arrival_airport,))
                arrival_airport_type = cursor.fetchone()["type"]

                if departure_airport_type != arrival_airport_type:
                    session[
                        "error"
                    ] = "Error: Domestic and international airports cannot be mixed for a flight."
                    return redirect("/")
                query = """
                    SELECT *
                    FROM Procedures
                    WHERE Airline_Name = %s AND Identification = %s
                    AND (
                        (StartDate BETWEEN %s AND %s) OR
                        (EndDate BETWEEN %s AND %s)
                    )
                """
                cursor.execute(
                    query,
                    (
                        airline_name,
                        identification,
                        departure_date,
                        arrival_date,
                        departure_date,
                        arrival_date,
                    ),
                )
                overlapping_flight = cursor.fetchone()

                if overlapping_flight:
                    session[
                        "error"
                    ] = "A maintenance period is scheduled during the flight. Cannot schedule maintenance."
                    return redirect("/")

            with connection.cursor() as cursor:
                query = """
                    INSERT INTO Flight
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(
                    query,
                    (
                        airline_name,
                        identification,
                        flight_number,
                        departure_date,
                        departure_time,
                        arrival_date,
                        arrival_time,
                        base_price,
                        status,
                        isroundtrip,
                        departure_airport,
                        arrival_airport,
                    ),
                )
                connection.commit()

            return redirect("/")

        except Exception as E:
            if "Unknown column" in str(E):
                return redirect("/")
            session["error"] = str(E)
            return redirect("/")

        finally:
            connection.close()

    return render_template("create_flight.html", airline_name=airline_name)


@app.route("/change_status", methods=["POST"])
def change_status():
    if "username" not in session:
        session["error"] = "Must be logged in as staff"
        return redirect("/")

    airline = request.form["airline"]
    flight_number = request.form["flight_number"]
    departure_date = request.form["departure_date"]
    departure_time = request.form["departure_time"]
    new_departure_date = request.form["new_departure_date"]
    new_departure_time = request.form["new_departure_time"]
    new_arrival_date = request.form["new_arrival_date"]
    new_arrival_time = request.form["new_arrival_time"]
    new_status = request.form["new_status"]

    connection = pymysql.connect(**mysql_config)
    try:
        with connection.cursor() as cursor:
            query = """
                SELECT Ticket_ID, email, FirstName, LastName, DOB, PurchaseDate, PurchaseTime,
                       CardType, CardNumber, CardExpiration, CardName, price, Identification
                FROM Ticket
                WHERE Airline_Name = %s AND Number = %s AND Depart_Date = %s AND Depart_Time = %s
            """
            cursor.execute(
                query, (airline, flight_number, departure_date, departure_time)
            )
            tickets = cursor.fetchall()

            query = """
                DELETE FROM Ticket
                WHERE Airline_Name = %s AND Number = %s AND Depart_Date = %s AND Depart_Time = %s
            """
            cursor.execute(
                query, (airline, flight_number, departure_date, departure_time)
            )
            connection.commit()

            query = """
                UPDATE Flight
                SET status = %s, departure_date = %s, departure_time = %s, arrival_date = %s, arrival_time = %s
                WHERE Airline_Name = %s AND number = %s AND departure_date = %s AND departure_time = %s
            """
            cursor.execute(
                query,
                (
                    new_status,
                    new_departure_date,
                    new_departure_time,
                    new_arrival_date,
                    new_arrival_time,
                    airline,
                    flight_number,
                    departure_date,
                    departure_time,
                ),
            )
            connection.commit()

            for ticket in tickets:
                query = """
                    INSERT INTO Ticket
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(
                    query,
                    (
                        ticket["Ticket_ID"],
                        airline,
                        ticket["Identification"],
                        flight_number,
                        new_departure_date,
                        new_departure_time,
                        ticket["email"],
                        ticket["FirstName"],
                        ticket["LastName"],
                        ticket["DOB"],
                        ticket["PurchaseDate"],
                        ticket["PurchaseTime"],
                        ticket["CardType"],
                        ticket["CardNumber"],
                        ticket["CardExpiration"],
                        ticket["CardName"],
                        ticket["price"],
                    ),
                )
            connection.commit()

        return redirect("/")

    except Exception as E:
        if "Unknown column" in str(E):
            return redirect("/")
        session["error"] = str(E)
        return redirect("/")

    finally:
        connection.close()


@app.route("/add_airplane", methods=["GET", "POST"])
def add_airplane():
    if "username" not in session:
        session["error"] = "Must be logged in as staff"
        return redirect("/")

    username = session["username"]

    connection = pymysql.connect(**mysql_config)
    try:
        with connection.cursor() as cursor:
            query = "SELECT airline_name FROM AirlineStaff WHERE username = %s"
            cursor.execute(query, (username,))
            airline_name = cursor.fetchone()["airline_name"]

            query = "SELECT * FROM Airplane WHERE Airline_Name = %s"
            cursor.execute(query, (airline_name,))
            airplanes = cursor.fetchall()

        if request.method == "POST":
            identification = request.form["identification"]
            seats = request.form["seats"]
            model = request.form["model"]
            manufacturing_company = request.form["manufacturing_company"]
            manufacture_date = request.form["manufacture_date"]
            age = request.form["age"]

            with connection.cursor() as cursor:
                query = """
                    INSERT INTO Airplane
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(
                    query,
                    (
                        airline_name,
                        identification,
                        seats,
                        model,
                        manufacturing_company,
                        manufacture_date,
                        age,
                    ),
                )
                connection.commit()

            return redirect("/add_airplane")

        return render_template(
            "add_airplane.html", airline_name=airline_name, airplanes=airplanes
        )

    except Exception as e:
        session["error"] = str(e)
        return redirect("/")

    finally:
        connection.close()


@app.route("/add_airport", methods=["GET", "POST"])
def add_airport():
    if "username" not in session:
        session["error"] = "Unauthorized access"
        return redirect("/")

    if request.method == "POST":
        airport_code = request.form["airport_code"]
        airport_name = request.form["airport_name"]
        city = request.form["city"]
        country = request.form["country"]
        num_terminals = request.form["num_terminals"]
        airport_type = request.form["type"]

        connection = pymysql.connect(**mysql_config)
        try:
            with connection.cursor() as cursor:
                query = """
                    INSERT INTO Airport
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(
                    query,
                    (
                        airport_code,
                        airport_name,
                        city,
                        country,
                        num_terminals,
                        airport_type,
                    ),
                )
                connection.commit()

            return redirect("/")

        except Exception as e:
            session["error"] = str(e)
            return redirect("/")

        finally:
            connection.close()

    return render_template("add_airport.html")


@app.route("/staff_view_ratings", methods=["POST"])
def staff_view_ratings():
    airline_name = request.form["airline_name"]
    flight_number = request.form["flight_number"]
    departure_date = request.form["departure_date"]
    departure_time = request.form["departure_time"]

    connection = pymysql.connect(**mysql_config)
    try:
        with connection.cursor() as cursor:
            query = """
                SELECT email, rating, comment_ratings
                FROM Ratings
                WHERE airline_name = %s AND number = %s AND departure_date = %s AND departure_time = %s
            """
            cursor.execute(
                query, (airline_name, flight_number, departure_date, departure_time)
            )
            ratings = cursor.fetchall()

        return render_template(
            "staff_view_ratings.html",
            ratings=ratings,
            airline_name=airline_name,
            flight_number=flight_number,
            departure_date=departure_date,
            departure_time=departure_time,
        )

    finally:
        connection.close()


@app.route("/schedule_procedure", methods=["GET", "POST"])
def schedule_procedure():
    if "username" not in session:
        session["error"] = "Unauthorized access"
        return redirect("/")

    if request.method == "POST":
        airplane_id = request.form["airplane_id"]
        start_date = request.form["start_date"]
        start_time = request.form["start_time"]
        end_date = request.form["end_date"]
        end_time = request.form["end_time"]

        connection = pymysql.connect(**mysql_config)
        try:
            with connection.cursor() as cursor:
                query = "SELECT airline_name FROM AirlineStaff WHERE username = %s"
                cursor.execute(query, (session["username"],))
                airline_name = cursor.fetchone()["airline_name"]

                query = "SELECT * FROM Airplane WHERE Airline_Name = %s AND Identification = %s"
                cursor.execute(query, (airline_name, airplane_id))
                airplane = cursor.fetchone()

                if not airplane:
                    session["error"] = "Airplane not found"
                    return redirect("/")

                query = """
                SELECT *
                FROM Flight
                WHERE Airline_Name = %s AND Identification = %s
                AND (
                    (departure_date BETWEEN %s AND %s) OR
                    (arrival_date BETWEEN %s AND %s)
                )
                """
                cursor.execute(
                    query,
                    (
                        airline_name,
                        airplane_id,
                        start_date,
                        end_date,
                        start_date,
                        end_date,
                    ),
                )
                overlapping_flight = cursor.fetchone()

                if overlapping_flight:
                    session[
                        "error"
                    ] = "A flight is scheduled during the maintenance period. Cannot schedule maintenance."
                    return redirect("/")

                query = """
                    INSERT INTO Procedures
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(
                    query,
                    (
                        airline_name,
                        airplane_id,
                        start_date,
                        start_time,
                        end_date,
                        end_time,
                    ),
                )
                connection.commit()

            return redirect("/")

        finally:
            connection.close()

    return render_template("schedule_procedure.html")


@app.route("/frequent_customers", methods=["GET", "POST"])
def frequent_customers():
    if "username" not in session:
        return redirect("/staff_login")

    current_date = datetime.date.today()
    one_year_ago = current_date - datetime.timedelta(days=365)

    connection = pymysql.connect(**mysql_config)
    try:
        with connection.cursor() as cursor:
            query = "SELECT airline_name FROM AirlineStaff WHERE username = %s"
            cursor.execute(query, (session["username"],))
            airline_name = cursor.fetchone()["airline_name"]
            query = """
                SELECT c.email, c.first_name, c.last_name, COUNT(*) AS flight_count
                FROM Ticket t
                NATURAL JOIN Customers c
                WHERE t.Airline_Name = %s AND c.email != 'None'
                AND t.Depart_Date BETWEEN %s AND %s
                GROUP BY c.email, c.first_name, c.last_name
                ORDER BY flight_count DESC
                LIMIT 1
            """
            cursor.execute(query, (airline_name, one_year_ago, current_date))
            frequent_customer = cursor.fetchone()

            flights = None
            if request.method == "POST":
                email = request.form["email"]
                query = """
                    SELECT f.number, f.departure_date, f.departure_time, f.arrival_date, f.arrival_time, f.departure_airport, f.arrival_airport
                    FROM Ticket t
                    JOIN Flight f ON t.Airline_Name = f.Airline_Name AND t.Number = f.number AND t.Depart_Date = f.departure_date AND t.Depart_Time = f.departure_time
                    WHERE t.email = %s AND t.Airline_Name = %s
                """
                cursor.execute(query, (email, airline_name))
                flights = cursor.fetchall()

        return render_template(
            "frequent_customers.html",
            frequent_customer=frequent_customer,
            flights=flights,
        )

    finally:
        connection.close()


@app.route("/earned_revenue")
def earned_revenue():
    if "username" not in session:
        return redirect("/staff_login")

    current_date = datetime.date.today()
    one_month_ago = current_date - datetime.timedelta(days=30)
    one_year_ago = current_date - datetime.timedelta(days=365)

    connection = pymysql.connect(**mysql_config)
    try:
        with connection.cursor() as cursor:
            query = "SELECT airline_name FROM AirlineStaff WHERE username = %s"
            cursor.execute(query, (session["username"],))
            airline_name = cursor.fetchone()["airline_name"]

            query = """
                SELECT SUM(t.price) AS total_revenue
                FROM Ticket t
                WHERE t.airline_name = %s
                AND t.PurchaseDate BETWEEN %s AND %s
            """
            cursor.execute(query, (airline_name, one_month_ago, current_date))
            last_month_revenue = cursor.fetchone()["total_revenue"]

            query = """
                SELECT SUM(t.price) AS total_revenue
                FROM Ticket t
                WHERE t.airline_name = %s
                AND t.PurchaseDate BETWEEN %s AND %s
            """
            cursor.execute(query, (airline_name, one_year_ago, current_date))
            last_year_revenue = cursor.fetchone()["total_revenue"]
            last_month_revenue = 0 if last_month_revenue is None else last_month_revenue
            last_year_revenue = 0 if last_year_revenue is None else last_year_revenue
        return render_template(
            "earned_revenue.html",
            last_month_revenue=last_month_revenue,
            last_year_revenue=last_year_revenue,
        )
    except Exception as e:
        session["error"] = str(e)
        return redirect("/")
    finally:
        connection.close()


if __name__ == "__main__":
    app.run()
