INSERT INTO Airline (Airline_Name) VALUES ('United');

INSERT INTO AirlineStaff (username, airline_name, password, first_name, last_name, DOB)
VALUES ('admin', 'United', MD5('abcd'), 'Roe', 'Jones', '1978-05-25');

INSERT INTO PhoneNumber (username, Airline_Name, phone_number)
VALUES ('admin', 'United', '111-2222-3333');

INSERT INTO PhoneNumber (username, Airline_Name, phone_number)
VALUES ('admin', 'United', '444-5555-6666');

INSERT INTO EmailAddress (username, Airline_Name, email_address)
VALUES ('admin', 'United', 'staff@nyu.edu');

INSERT INTO Airplane (Airline_Name, Identification, numseats, model, manufacturer, manufacture_date, age)
VALUES ('United', 1, 4, 'B-101', 'Boeing', '2013-05-02', 10);

INSERT INTO Airplane (Airline_Name, Identification, numseats, model, manufacturer, manufacture_date, age)
VALUES ('United', 2, 4, 'A-101', 'Airbus', '2011-05-02', 12);

INSERT INTO Airplane (Airline_Name, Identification, numseats, model, manufacturer, manufacture_date, age)
VALUES ('United', 3, 50, 'B-101', 'Boeing', '2015-05-02', 8);

INSERT INTO Procedures (Airline_Name, Identification, StartDate, StartTime, EndDate, EndTime)
VALUES ('United', 1, '2024-06-27', '13:25:25', '2024-06-29', '07:25:25');

INSERT INTO Procedures (Airline_Name, Identification, StartDate, StartTime, EndDate, EndTime)
VALUES ('United', 2, '2024-01-27', '13:25:25', '2024-01-29', '07:25:25');

INSERT INTO Airport (airport_code, airport_name, city, country, num_terminals, type)
VALUES ('JFK', 'JFK', 'NYC', 'USA', 4, 'both');

INSERT INTO Airport (airport_code, airport_name, city, country, num_terminals, type)
VALUES ('BOS', 'BOS', 'Boston', 'USA', 2, 'both');

INSERT INTO Airport (airport_code, airport_name, city, country, num_terminals, type)
VALUES ('PVG', 'PVG', 'Shanghai', 'China', 2, 'both');

INSERT INTO Airport (airport_code, airport_name, city, country, num_terminals, type)
VALUES ('BEI', 'BEI', 'Beijing', 'China', 2, 'both');

INSERT INTO Airport (airport_code, airport_name, city, country, num_terminals, type)
VALUES ('SFO', 'SFO', 'San Francisco', 'USA', 2, 'both');

INSERT INTO Airport (airport_code, airport_name, city, country, num_terminals, type)
VALUES ('LAX', 'LAX', 'Los Angeles', 'USA', 2, 'both');

INSERT INTO Airport (airport_code, airport_name, city, country, num_terminals, type)
VALUES ('HKA', 'HKA', 'Hong Kong', 'China', 2, 'both');

INSERT INTO Airport (airport_code, airport_name, city, country, num_terminals, type)
VALUES ('SHEN', 'SHEN', 'Shenzhen', 'China', 2, 'both');

INSERT INTO Customers (email, password, first_name, last_name, building_number, street, city, state, zipcode, passport_number, passport_expiration, passport_country, DOB)
VALUES ('testcustomer@nyu.edu', MD5('1234'), 'Jon', 'Snow', 1555, 'Jay St', 'Brooklyn', 'New York', '', '54321', '2025-12-24', 'USA', '1999-12-19');

INSERT INTO Customer_Phone (email, phone_number)
VALUES ('testcustomer@nyu.edu', '123-4321-4321');

INSERT INTO Customers (email, password, first_name, last_name, building_number, street, city, state, zipcode, passport_number, passport_expiration, passport_country, DOB)
VALUES ('user1@nyu.edu', MD5('1234'), 'Alice', 'Bob', 5405, 'Jay Street', 'Brooklyn', 'New York', '', '54322', '2025-12-25', 'USA', '1999-11-19');

INSERT INTO Customer_Phone (email, phone_number)
VALUES ('user1@nyu.edu', '123-4322-4322');

INSERT INTO Customers (email, password, first_name, last_name, building_number, street, city, state, zipcode, passport_number, passport_expiration, passport_country, DOB)
VALUES ('user2@nyu.edu', MD5('1234'), 'Cathy', 'Wood', 1702, 'Jay Street', 'Brooklyn', 'New York', '', '54323', '2025-10-24', 'USA', '1999-10-19');

INSERT INTO Customer_Phone (email, phone_number)
VALUES ('user2@nyu.edu', '123-4323-4323');

INSERT INTO Customers (email, password, first_name, last_name, building_number, street, city, state, zipcode, passport_number, passport_expiration, passport_country, DOB)
VALUES ('user3@nyu.edu', MD5('1234'), 'Trudy', 'Jones', 1890, 'Jay Street', 'Brooklyn', 'New York', '', '54324', '2025-09-24', 'USA', '1999-09-19');

INSERT INTO Customer_Phone (email, phone_number)
VALUES ('user3@nyu.edu', '123-4324-4324');

INSERT INTO Flight (Airline_Name, Identification, number, departure_date, departure_time, arrival_date, arrival_time, base_price, status, isroundtrip, departure_airport, arrival_airport)
VALUES ('United', 3, 102, '2024-02-12', '13:25:25', '2024-02-12', '16:50:25', 300, 'normal', NULL, 'SFO', 'LAX');

INSERT INTO Flight (Airline_Name, Identification, number, departure_date, departure_time, arrival_date, arrival_time, base_price, status, isroundtrip, departure_airport, arrival_airport)
VALUES ('United', 3, 104, '2024-03-04', '13:25:25', '2024-03-04', '16:50:25', 300, 'normal', NULL, 'PVG', 'BEI');

INSERT INTO Flight (Airline_Name, Identification, number, departure_date, departure_time, arrival_date, arrival_time, base_price, status, isroundtrip, departure_airport, arrival_airport)
VALUES ('United', 3, 106, '2024-01-04', '13:25:25', '2024-01-04', '16:50:25', 350, 'delayed', NULL, 'SFO', 'LAX');

INSERT INTO Flight (Airline_Name, Identification, number, departure_date, departure_time, arrival_date, arrival_time, base_price, status, isroundtrip, departure_airport, arrival_airport)
VALUES ('United', 2, 206, '2024-07-04', '13:25:25', '2024-07-04', '16:50:25', 400, 'normal', NULL, 'SFO', 'LAX');

INSERT INTO Flight (Airline_Name, Identification, number, departure_date, departure_time, arrival_date, arrival_time, base_price, status, isroundtrip, departure_airport, arrival_airport)
VALUES ('United', 2, 207, '2024-08-04', '13:25:25', '2024-08-04', '16:50:25', 300, 'normal', NULL, 'LAX', 'SFO');

INSERT INTO Flight (Airline_Name, Identification, number, departure_date, departure_time, arrival_date, arrival_time, base_price, status, isroundtrip, departure_airport, arrival_airport)
VALUES ('United', 3, 134, '2024-12-12', '13:25:25', '2024-12-12', '16:50:25', 300, 'delayed', NULL, 'JFK', 'BOS');

INSERT INTO Flight (Airline_Name, Identification, number, departure_date, departure_time, arrival_date, arrival_time, base_price, status, isroundtrip, departure_airport, arrival_airport)
VALUES ('United', 1, 296, '2024-05-30', '13:25:25', '2024-05-30', '16:50:25', 3000, 'normal', NULL, 'PVG', 'SFO');

INSERT INTO Flight (Airline_Name, Identification, number, departure_date, departure_time, arrival_date, arrival_time, base_price, status, isroundtrip, departure_airport, arrival_airport)
VALUES ('United', 1, 715, '2024-02-28', '10:25:25', '2024-02-28', '13:50:25', 500, 'delayed', NULL, 'PVG', 'BEI');

INSERT INTO Flight (Airline_Name, Identification, number, departure_date, departure_time, arrival_date, arrival_time, base_price, status, isroundtrip, departure_airport, arrival_airport)
VALUES ('United', 3, 839, '2023-05-26', '13:25:25', '2023-05-26', '16:50:25', 300, 'normal', NULL, 'SHEN', 'BEI');

INSERT INTO Ticket (Ticket_ID, Airline_Name, Identification, Number, Depart_Date, Depart_Time, email, FirstName, LastName, DOB, PurchaseDate, PurchaseTime, CardType, CardNumber, CardExpiration, CardName, price)
VALUES (1, 'United', 3, 104, '2024-03-04', '13:25:25', 'testcustomer@nyu.edu', 'Jon', 'Snow', '1999-12-19', '2024-01-07', '11:55:55', 'credit', 1111222233334444, '2025-03-01', 'Jon Snow', 300);

INSERT INTO Ticket (Ticket_ID, Airline_Name, Identification, Number, Depart_Date, Depart_Time, email, FirstName, LastName, DOB, PurchaseDate, PurchaseTime, CardType, CardNumber, CardExpiration, CardName, price)
VALUES (2, 'United', 3, 104, '2024-03-04', '13:25:25', 'user1@nyu.edu', 'Alice', 'Bob', '1999-11-19', '2024-01-06', '11:55:55', 'credit', 1111222233335555, '2025-03-01', 'Alice Bob', 300);

INSERT INTO Ticket (Ticket_ID, Airline_Name, Identification, Number, Depart_Date, Depart_Time, email, FirstName, LastName, DOB, PurchaseDate, PurchaseTime, CardType, CardNumber, CardExpiration, CardName, price)
VALUES (3, 'United', 1, 715, '2024-02-28', '10:25:25', 'user2@nyu.edu', 'Cathy', 'Wood', '1999-10-19', '2024-02-04', '11:55:55', 'credit', 1111222233335555, '2025-03-01', 'Cathy Wood', 300);

INSERT INTO Ticket (Ticket_ID, Airline_Name, Identification, Number, Depart_Date, Depart_Time, email, FirstName, LastName, DOB, PurchaseDate, PurchaseTime, CardType, CardNumber, CardExpiration, CardName, price)
VALUES (4, 'United', 3, 134, '2024-12-12', '13:25:25', 'user1@nyu.edu', 'Alice', 'Bob', '1999-11-19', '2024-01-21', '11:55:55', 'credit', 1111222233335555, '2024-03-01', 'Alice Bob', 300);

INSERT INTO Ticket (Ticket_ID, Airline_Name, Identification, Number, Depart_Date, Depart_Time, email, FirstName, LastName, DOB, PurchaseDate, PurchaseTime, CardType, CardNumber, CardExpiration, CardName, price)
VALUES (5, 'United', 1, 715, '2024-02-28', '10:25:25', 'testcustomer@nyu.edu', 'Jon', 'Snow', '1999-12-19', '2024-02-28', '11:55:55', 'credit', 1111222233334444, '2024-03-01', 'Jon Snow', 300);

INSERT INTO Ticket (Ticket_ID, Airline_Name, Identification, Number, Depart_Date, Depart_Time, email, FirstName, LastName, DOB, PurchaseDate, PurchaseTime, CardType, CardNumber, CardExpiration, CardName, price)
VALUES (6, 'United', 3, 106, '2024-01-04', '13:25:25', 'testcustomer@nyu.edu', 'Jon', 'Snow', '1999-12-19', '2024-01-02', '11:55:55', 'credit', 1111222233334444, '2024-03-01', 'Jon Snow', 350);

INSERT INTO Ticket (Ticket_ID, Airline_Name, Identification, Number, Depart_Date, Depart_Time, email, FirstName, LastName, DOB, PurchaseDate, PurchaseTime, CardType, CardNumber, CardExpiration, CardName, price)
VALUES (7, 'United', 3, 106, '2024-01-04', '13:25:25', 'user3@nyu.edu', 'Trudy', 'Jones', '1999-09-19', '2023-12-03', '11:55:55', 'credit', 1111222233335555, '2024-03-01', 'Trudy Jones', 350);

INSERT INTO Ticket (Ticket_ID, Airline_Name, Identification, Number, Depart_Date, Depart_Time, email, FirstName, LastName, DOB, PurchaseDate, PurchaseTime, CardType, CardNumber, CardExpiration, CardName, price)
VALUES (8, 'United', 3, 839, '2023-05-26', '13:25:25', 'user3@nyu.edu', 'Trudy', 'Jones', '1999-09-19', '2023-05-23', '11:55:55', 'credit', 1111222233335555, '2024-03-01', 'Trudy Jones', 300);

INSERT INTO Ticket (Ticket_ID, Airline_Name, Identification, Number, Depart_Date, Depart_Time, email, FirstName, LastName, DOB, PurchaseDate, PurchaseTime, CardType, CardNumber, CardExpiration, CardName, price)
VALUES (9, 'United', 3, 134, '2024-12-12', '13:25:25', 'user3@nyu.edu', 'Trudy', 'Jones', '1999-09-19', '2023-12-04', '11:55:55', 'credit', 1111222233335555, '2024-03-01', 'Trudy Jones', 300);

INSERT INTO Ticket (Ticket_ID, Airline_Name, Identification, Number, Depart_Date, Depart_Time, email, FirstName, LastName, DOB, PurchaseDate, PurchaseTime, CardType, CardNumber, CardExpiration, CardName, price)
VALUES (11, 'United', 3, 104, '2024-03-04', '13:25:25', 'user3@nyu.edu', 'Trudy', 'Jones', '1999-09-19', '2023-10-23', '11:55:55', 'credit', 1111222233335555, '2024-03-01', 'Trudy Jones', 300);

INSERT INTO Ticket (Ticket_ID, Airline_Name, Identification, Number, Depart_Date, Depart_Time, email, FirstName, LastName, DOB, PurchaseDate, PurchaseTime, CardType, CardNumber, CardExpiration, CardName, price)
VALUES (12, 'United', 1, 715, '2024-02-28', '10:25:25', 'testcustomer@nyu.edu', 'Jon', 'Snow', '1999-12-19', '2023-10-02', '11:55:55', 'credit', 1111222233334444, '2024-03-01', 'Jon Snow', 500);

INSERT INTO Ticket (Ticket_ID, Airline_Name, Identification, Number, Depart_Date, Depart_Time, email, FirstName, LastName, DOB, PurchaseDate, PurchaseTime, CardType, CardNumber, CardExpiration, CardName, price)
VALUES (14, 'United', 2, 206, '2024-07-04', '13:25:25', 'user3@nyu.edu', 'Trudy', 'Jones', '1999-09-19', '2024-04-20', '11:55:55', 'credit', 1111222233335555, '2024-03-01', 'Trudy Jones', 400);

INSERT INTO Ticket (Ticket_ID, Airline_Name, Identification, Number, Depart_Date, Depart_Time, email, FirstName, LastName, DOB, PurchaseDate, PurchaseTime, CardType, CardNumber, CardExpiration, CardName, price)
VALUES (15, 'United', 2, 206, '2024-07-04', '13:25:25', 'user1@nyu.edu', 'Alice', 'Bob', '1999-11-19', '2024-04-21', '11:55:55', 'credit', 1111222233335555, '2024-03-01', 'Alice Bob', 400);

INSERT INTO Ticket (Ticket_ID, Airline_Name, Identification, Number, Depart_Date, Depart_Time, email, FirstName, LastName, DOB, PurchaseDate, PurchaseTime, CardType, CardNumber, CardExpiration, CardName, price)
VALUES (16, 'United', 2, 206, '2024-07-04', '13:25:25', 'user2@nyu.edu', 'Cathy', 'Wood', '1999-10-19', '2024-02-19', '11:55:55', 'credit', 1111222233335555, '2024-03-01', 'Cathy Wood', 400);

INSERT INTO Ticket (Ticket_ID, Airline_Name, Identification, Number, Depart_Date, Depart_Time, email, FirstName, LastName, DOB, PurchaseDate, PurchaseTime, CardType, CardNumber, CardExpiration, CardName, price)
VALUES (17, 'United', 3, 102, '2024-02-12', '13:25:25', 'user1@nyu.edu', 'Alice', 'Bob', '1999-11-19', '2024-01-11', '11:55:55', 'credit', 1111222233335555, '2024-03-01', 'Alice Bob', 300);

INSERT INTO Ticket (Ticket_ID, Airline_Name, Identification, Number, Depart_Date, Depart_Time, email, FirstName, LastName, DOB, PurchaseDate, PurchaseTime, CardType, CardNumber, CardExpiration, CardName, price)
VALUES (18, 'United', 3, 102, '2024-02-12', '13:25:25', 'testcustomer@nyu.edu', 'Jon', 'Snow', '1999-12-19', '2024-02-25', '11:55:55', 'credit', 1111222233334444, '2024-03-01', 'Jon Snow', 300);

INSERT INTO Ticket (Ticket_ID, Airline_Name, Identification, Number, Depart_Date, Depart_Time, email, FirstName, LastName, DOB, PurchaseDate, PurchaseTime, CardType, CardNumber, CardExpiration, CardName, price)
VALUES (19, 'United', 1, 296, '2024-05-30', '13:25:25', 'user1@nyu.edu', 'Alice', 'Bob', '1999-11-19', '2024-04-22', '11:55:55', 'credit', 1111222233334444, '2024-03-01', 'Alice Bob', 3000);

INSERT INTO Ticket (Ticket_ID, Airline_Name, Identification, Number, Depart_Date, Depart_Time, email, FirstName, LastName, DOB, PurchaseDate, PurchaseTime, CardType, CardNumber, CardExpiration, CardName, price)
VALUES (20, 'United', 1, 296, '2024-05-30', '13:25:25', 'testcustomer@nyu.edu', 'Jon', 'Snow', '1999-12-19', '2023-12-12', '11:55:55', 'credit', 1111222233334444, '2024-03-01', 'Jon Snow', 3000);

INSERT INTO Ratings (email, airline_name, identification, number, departure_date, departure_time, rating, comment_ratings)
VALUES ('testcustomer@nyu.edu', 'United', 3, 102, '2024-02-12', '13:25:25', 4, 'Very Comfortable');

INSERT INTO Ratings (email, airline_name, identification, number, departure_date, departure_time, rating, comment_ratings)
VALUES ('user1@nyu.edu', 'United', 3, 102, '2024-02-12', '13:25:25', 5, 'Relaxing, check-in and onboarding very professional');

INSERT INTO Ratings (email, airline_name, identification, number, departure_date, departure_time, rating, comment_ratings)
VALUES ('user2@nyu.edu', 'United', 3, 102, '2024-02-12', '13:25:25', 3, 'Satisfied and will use the same flight again');

INSERT INTO Ratings (email, airline_name, identification, number, departure_date, departure_time, rating, comment_ratings)
VALUES ('testcustomer@nyu.edu', 'United', 3, 104, '2024-03-04', '13:25:25', 1, 'Customer Care services are not good');

INSERT INTO Ratings (email, airline_name, identification, number, departure_date, departure_time, rating, comment_ratings)
VALUES ('user1@nyu.edu', 'United', 3, 104, '2024-03-04', '13:25:25', 5, 'Comfortable journey and Professional');