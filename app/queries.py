customer_future_flights = """
    SELECT 
        f.Airline_Name, f.Identification, f.number, f.departure_date, f.departure_time,
        f.arrival_date, f.arrival_time, f.base_price, f.status, f.isroundtrip,
        f.departure_airport, f.arrival_airport, t.Ticket_ID
    FROM 
        Flight f
        NATURAL JOIN Ticket t
    WHERE 
        t.Email = %s AND
        f.departure_date >= %s
"""

customer_past_flights = """
    SELECT 
        f.Airline_Name, f.Identification, f.number, f.departure_date, f.departure_time,
        f.arrival_date, f.arrival_time, f.base_price, f.status, f.isroundtrip,
        f.departure_airport, f.arrival_airport, t.Ticket_ID
    FROM 
        Flight f
        NATURAL JOIN Ticket t
    WHERE 
        t.Email = %s AND
        f.departure_date < %s
"""

customer_rated_flights = """
SELECT 
    airline_name, identification, number, departure_date, departure_time, rating, comment_ratings
FROM 
    Ratings
WHERE 
    email = %s
"""

customer_rated_check = """
SELECT COUNT(*) 
FROM Ratings
WHERE email = %s
    AND airline_name = %s
    AND identification = %s
    AND number = %s
    AND departure_date = %s
    AND departure_time = %s
"""

customer_rated_delete = """
DELETE FROM Ratings
WHERE email = %s
    AND airline_name = %s
    AND identification = %s
    AND number = %s
    AND departure_date = %s
    AND departure_time = %s
"""

customer_name = """
SELECT 
    first_name, last_name
FROM 
    Customers
WHERE 
    email = %s
"""

customer_rate = """
INSERT INTO Ratings
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""
