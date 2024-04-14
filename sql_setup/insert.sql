insert into Airline values
			('Jetblue');

insert into airport 
values
	('JFK', 'John F. Kennedy Airport', 'New York City','United States', 4, 'Both'),
	('PVG', 'Shanghai international airport', 'Shanghai', 'China', 4, 'Both');

insert into customers values
("hi@gmail.com", "notgood", "alex", "ander", 370, "Jay Street Metrotech", "New York City", "New York", "11101", "123456789", "2026-12-17", "United States", "2001-11-11"),
("hello@gmail.com", "amazing", "bob", "ert", 371, "Jay Street Metroootech", "New York City", "New York", "11101", "123457891", "2026-10-17", "United States", "2003-12-15"),
("bye@gmail.com", "password123", "calvin", "hobbes", 372, "Jay Street Metroootech", "New York City", "New York", "11101", "132457891", "2026-10-17", "United States", "2003-12-15");


insert into airplane values 
("Jetblue", 12, 8, "Boeing 10", "Boeing", "2022-10-17", 2), 
("Jetblue", 13, 8, "Airbus 737", "Airbus", "2022-10-18", 2), 
("Jetblue", 14, 8, "Boeing 747", "Boeing", "2022-10-19", 2);

insert into airlinestaff values 
("AliceB", "Jetblue", "Boeinglove", "Alice", "Boeing", "2022-10-17");

insert into PhoneNumber values
("AliceB", "Jetblue", "9127630738");

insert into EmailAddress values
("AliceB", "Jetblue", "boring@gmail.com");

insert into flight values 
('Jetblue', 13, 102, '2023-06-01', '08:50:10', '2023-06-02', '11:35:00', 150.00, 'normal', true, 'PVG', 'JFK'),
('Jetblue', 14, 104, '2023-07-11', '11:50:10', '2023-07-12', '11:35:00', 150.00, 'normal', true, 'JFK', 'PVG'),
('Jetblue', 12, 101, '2023-06-01', '08:00:00', '2023-06-01', '10:30:00', 150.00, 'normal', true, 'PVG', 'JFK'),
('Jetblue', 13, 109, '2023-06-01', '08:50:10', '2023-06-02', '11:35:00', 150.00, 'delayed', true, 'PVG', 'JFK');


INSERT INTO Ticket values 
(1, 'Jetblue', 13, 102, '2023-06-01', '08:50:10', 'hi@gmail.com', 'alex', 'ander', '2001-11-11', '2023-05-20', '10:30:00', 'Visa', '1234567890123456', '2024-12-31', 'Alex Ander'),
(2, 'Jetblue', 14, 104, '2023-07-11', '11:50:10', 'hello@gmail.com', 'bob', 'ert', '2003-12-15', '2023-06-25', '09:45:00', 'Mastercard', '9876543210987654', '2025-06-30', 'Bob Ert'),
(3, 'Jetblue', 12, 101, '2023-06-01', '08:00:00', 'bye@gmail.com', 'calvin', 'hobbes', '2003-12-15', '2023-05-28', '14:20:00', 'American Express', '1111222233334444', '2023-11-30', 'Calvin Hobbes'),
(4, 'Jetblue', 13, 109, '2023-06-01', '08:50:10', 'hi@gmail.com', 'alex', 'ander', '2001-11-11', '2023-05-30', '16:00:00', 'Visa', '5555666677778888', '2024-09-30', 'Alex Ander');