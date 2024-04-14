SELECT Airline_Name, Identification, number, departure_date, departure_time
FROM Flight
WHERE departure_date > CAST(CURDATE() AS DATE);

SELECT *
FROM Flight
WHERE status = 'delayed';

SELECT DISTINCT FirstName, LastName
FROM Ticket
NATURAL JOIN Customers;

SELECT Identification
FROM Airplane
WHERE Airline_Name = 'Jetblue';