create table Airline(
	Airline_Name 			varchar(20) NOT NULL,
	PRIMARY KEY(Airline_Name)
);
create table Airplane(
	Airline_Name			VARCHAR(20) NOT NULL,	
	Identification		DOUBLE(10,0) UNSIGNED NOT NULL,
	numseats 		DOUBLE(4,0) UNSIGNED NOT NULL,
    model		VARCHAR(20) NOT NULL,
	manufacturer		VARCHAR(20) NOT NULL,
    manufacture_date		DATE NOT NULL,
	age		DOUBLE(10, 0) UNSIGNED NOT NULL,
	PRIMARY KEY(Airline_Name, Identification),
	FOREIGN KEY(Airline_Name) references Airline(Airline_Name)
);

create table Airport(
	airport_code				VARCHAR(20) NOT NULL, 
	airport_name			VARCHAR(20) NOT NULL, 
	city				VARCHAR(20) NOT NULL,
	country 			VARCHAR(20) NOT NULL, 
	num_terminals		DOUBLE(4,0) UNSIGNED NOT NULL,
	type 				VARCHAR(15) CHECK (type in ('domestic', 'international', 'both')),
	PRIMARY KEY(airport_code)
);

CREATE TABLE Flight (
    Airline_Name VARCHAR(20) NOT NULL,
    Identification DOUBLE(10, 0) UNSIGNED NOT NULL,
    number DOUBLE(10, 0) UNSIGNED NOT NULL,
    departure_date DATE NOT NULL,
    departure_time TIME(3) NOT NULL,
    arrival_date DATE NOT NULL,
    arrival_time TIME(3) NOT NULL,
    base_price DOUBLE(10, 0) UNSIGNED NOT NULL,
    status VARCHAR(10) NOT NULL CHECK (status IN ('delayed', 'normal', 'canceled')),
    isroundtrip BOOLEAN,
    departure_airport VARCHAR(20),
    arrival_airport VARCHAR(20),
    PRIMARY KEY (Airline_Name, Identification, number, departure_date, departure_time),
    FOREIGN KEY (Airline_Name, Identification) REFERENCES Airplane(Airline_Name, Identification),
    FOREIGN KEY (departure_airport) REFERENCES Airport(airport_code),
    FOREIGN KEY (arrival_airport) REFERENCES Airport(airport_code)
);

CREATE TABLE ReturnFlight (
    ReturnAirline_Name VARCHAR(20) NOT NULL,
    ReturnIdentification DOUBLE(10, 0) UNSIGNED NOT NULL,
    Returnnumber DOUBLE(10, 0) UNSIGNED NOT NULL,
    Returndeparture_date DATE NOT NULL,
    Returndeparture_time TIME(3) NOT NULL,
    Returndeparture_airport VARCHAR(20),
    Returnarrival_airport VARCHAR(20),
    Airline_Name VARCHAR(20) NOT NULL,
    Identification DOUBLE(10, 0) UNSIGNED NOT NULL,
    number DOUBLE(10, 0) UNSIGNED NOT NULL,
    departure_date DATE NOT NULL,
    departure_time TIME(3) NOT NULL,
    departure_airport VARCHAR(20),
    arrival_airport VARCHAR(20),
    PRIMARY KEY (Airline_Name, Identification, number, departure_date, departure_time),
    FOREIGN KEY (Airline_Name, Identification, number, departure_date, departure_time)
        REFERENCES Flight(Airline_Name, Identification, number, departure_date, departure_time)
);
create table AirlineStaff(
	username 			VARCHAR(20) NOT NULL,
	airline_name			VARCHAR(20) NOT NULL, 
	password			VARCHAR(20) NOT NULL, 
	first_name			VARCHAR(20),
	last_name			VARCHAR(20), 
	DOB			DATE, 
	PRIMARY KEY (username, airline_name),
	FOREIGN KEY (airline_name) references Airline(airline_name)
);

create table PhoneNumber(
	username			VARCHAR(20) NOT NULL,
	Airline_Name			VARCHAR(20) NOT NULL,
	phone_number		CHAR(12),
PRIMARY KEY (username, airline_name, phone_number),
FOREIGN KEY (username, Airline_Name) references AirlineStaff(username, Airline_Name)
);

create table EmailAddress(
	username			VARCHAR(20) NOT NULL,
	Airline_Name			VARCHAR(20) NOT NULL,
	email_address	 		VARCHAR(20) NOT NULL,
	PRIMARY KEY (username, Airline_Name, email_address),
	FOREIGN KEY (username, Airline_Name) references AirlineStaff(username, Airline_Name)

);

CREATE TABLE Customers (
    email VARCHAR(20) NOT NULL,
    password VARCHAR(20) NOT NULL, 
    first_name VARCHAR(20) NOT NULL, 
    last_name VARCHAR(20) NOT NULL, 
    building_number DOUBLE(10, 0) UNSIGNED NOT NULL,
    street VARCHAR(30) NOT NULL,
    city VARCHAR(20) NOT NULL,
    state VARCHAR(20) NOT NULL,
    zipcode VARCHAR(20) NOT NULL,
    passport_number CHAR(9) NOT NULL,
    passport_expiration DATE NOT NULL,
    passport_country VARCHAR(20) NOT NULL, 
    DOB DATE NOT NULL,
    PRIMARY KEY (email)
);

CREATE TABLE Ratings (
    email VARCHAR(20) NOT NULL,
    airline_name VARCHAR(20) NOT NULL,
    identification DOUBLE(10, 0) UNSIGNED NOT NULL,
    number DOUBLE(10, 0) UNSIGNED NOT NULL, 
    departure_date DATE NOT NULL,
    departure_time TIME(3) NOT NULL,
    rating DOUBLE(10, 0) UNSIGNED NOT NULL,
    comment_ratings VARCHAR(600),
    PRIMARY KEY (email, airline_name, identification, number, departure_date, departure_time),
    FOREIGN KEY (email) REFERENCES Customers(email),
    FOREIGN KEY (airline_name, identification, number, departure_date, departure_time)
        REFERENCES Flight(Airline_Name, Identification, number, departure_date, departure_time)
);

CREATE TABLE Customer_Phone (
    email VARCHAR(20) NOT NULL,
    phone_number CHAR(12) NOT NULL,
    PRIMARY KEY (email, phone_number),
    FOREIGN KEY (email) REFERENCES Customers(email)
);


CREATE TABLE Ticket (
    Ticket_ID 					DOUBLE(10, 0) NOT NULL, 
    Airline_Name 				VARCHAR(20) NOT NULL,
    Identification 				DOUBLE(10, 0) UNSIGNED NOT NULL,
    Number 					DOUBLE(10, 0) UNSIGNED NOT NULL,
    Depart_Date 				DATE NOT NULL,
    Depart_Time 				TIME(3) NOT NULL,
    email 					VARCHAR(20) NOT NULL,
    FirstName 					VARCHAR(20) NOT NULL,
    LastName 					VARCHAR(20) NOT NULL,
    DOB 					DATE NOT NULL,
    PurchaseDate 				DATE NOT NULL,
    PurchaseTime 				TIME(3) NOT NULL,
    CardType 					VARCHAR(20) NOT NULL,
    CardNumber 					DOUBLE(16, 0) NOT NULL,
    CardExpiration 				DATE NOT NULL,
    CardName 					VARCHAR(50) NOT NULL,
    PRIMARY KEY (Ticket_ID),
    FOREIGN KEY (Airline_Name, Identification, Number, Depart_Date, Depart_Time)
        REFERENCES Flight(Airline_Name, Identification, number, departure_date, departure_time),
    FOREIGN KEY (email) REFERENCES Customers(email)
);


CREATE TABLE Procedures (
    Airline_Name VARCHAR(20) NOT NULL,
    Identification DOUBLE(10, 0) UNSIGNED NOT NULL,
    StartDate DATE NOT NULL,
    StartTime TIME(3) NOT NULL,
    EndDate DATE NOT NULL,
    EndTime TIME(3) NOT NULL,
    PRIMARY KEY (Airline_Name, Identification, StartDate, StartTime),
    FOREIGN KEY (Airline_Name, Identification) REFERENCES Airplane(Airline_Name, Identification)
);
