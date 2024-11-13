import re
import getpass
from abc import ABC, abstractmethod


# Abstract Base Class for the Flight Booking System
class FlightBookingSystem(ABC):
    @abstractmethod
    def search_flights(self, flights, departure, destination):
        pass

    @abstractmethod
    def book_flight(self, flight, passenger_name, seat):
        pass

    @abstractmethod
    def view_bookings(self):
        pass


# Flight class
class Flight:
    def __init__(self, flight_number, departure, destination, date, takeOff_time, landing_time, seats):
        self.flight_number = flight_number
        self.departure = departure
        self.destination = destination
        self.date = date
        self.takeOff_time = takeOff_time
        self.landing_time = landing_time
        self.seats = seats

    def __str__(self):
        return f"{self.flight_number} from {self.departure} to {self.destination} on {self.date} - Seats available: {self.seats}"


# Booking class
class Booking:
    def __init__(self, flight, passenger_name, seat):
        self.flight = flight
        self.passenger_name = passenger_name
        self.seat = seat
        self.booking_id = f"BK-{hash(self)}"

    def __str__(self):
        return f"Booking ID: {self.booking_id}, Flight: {self.flight}, Passenger: {self.passenger_name}, Seat: {self.seat}"


# Concrete class for User
class User(FlightBookingSystem):
    def __init__(self, name, email, password, gender, marital_status=None):
        self.name = name
        self.email = email
        self.password = password
        self.gender = gender
        self.marital_status = marital_status
        self.bookings = []

    def search_flights(self, flights, departure, destination):
        return [flight for flight in flights if flight.departure == departure and flight.destination == destination]

    def book_flight(self, flight, passenger_name, seat):
        if flight.seats > 0:
            flight.seats -= 1
            booking = Booking(flight, passenger_name, seat)
            self.bookings.append(booking)
            print(f"Booking successful: {booking}")
        else:
            print("No seats available.")

    def view_bookings(self):
        if not self.bookings:
            print("No bookings found.")
            return
        for booking in self.bookings:
            print(f"Booking ID: {booking.booking_id}, Flight: {booking.flight}, Passenger: {booking.passenger_name}, Seat: {booking.seat}")


# Input validation functions
def validate_name(name):
    if not re.match("^[A-Za-z ]+$", name):
        print("Error: Please enter a valid name.")
        return False
    return True

def validate_email(email):
    if "@" not in email or "." not in email:
        print("Error: Please enter a valid email.")
        return False
    return True

def validate_gender(gender):
    if gender.lower() not in ['m', 'f']:
        print("Error: Please enter the correct gender.")
        return False
    return True

def validate_password(password):
    correct_password = "Flight:08"
    if password != correct_password:
        print("Incorrect password. Please try again.")
        return False
    return True

def choose_payment_plan():
    print("\nChoose a payment plan:")
    print("1. VISA")
    print("2. Mastercard")
    print("3. MOMO Pay")
    print("4. Airtel Money Pay")
    print("5. Bitcoin")
    choice = input("We are almost done! Select a payment option:")
    if choice not in ['1', '2', '3', '4', '5']:
        print("Invalid option.")
        return choose_payment_plan()
    return choice


# Main program
def main():
    print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
    print("|WELCOME! AND THANK YOU FOR CHOOSING AIR UGANDA.|\n")
    print("|        Where Comfort Meets Serenity...        |\n")
    print("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*\n")
    
    # Sample Flights
    flights = [
        Flight("AA123", "Kampala", "Nairobi", "2024-12-01", "Take off: 8:00am", "Landing: 12:00pm", 10),
        Flight("BB456", "Kampala", "Nairobi", "2024-12-02", "Take off: 9:00pm", "Landing: 1:00am", 5),
        Flight("CC789", "Kampala", "Dar Es Salaam", "2024-12-03", "Take off: 4:00am", "Landing: 6:30am", 8)
    ]

    # User input with validation
    name = input("Enter your name: ")
    while not validate_name(name):
        name = input("Enter your name: ")

    email = input("Enter your email: ")
    while not validate_email(email):
        email = input("Enter your email: ")
        
    # Gender and title input
    gender = input("Enter your gender (Enter either m/f): ").strip().lower()
    while not validate_gender(gender):
        gender = input("Enter your gender (Enter either m/f): ").strip().lower()

    marital_status = None
    if gender == 'f':
        marital_status = input("Are you married or not? (yes/no): ").strip().lower()
        if marital_status == "yes":
            print(f"You are welcome to the Air Uganda airline official reservation system, Mrs. {name}!!")
        elif marital_status == "no":
            print(f"You are welcome to the Air Uganda airline official reservation system, Miss {name}!!")
        else:
            print("Your input was invalid. You may try again.")
            return
    elif gender == 'm':
        print(f"You are welcome to the Air Uganda official reservation system, Mr. {name}!!")

    # Password input (hidden and validation)
    while True:
        password = getpass.getpass("Enter your password: ")  # Hide the password input
        if validate_password(password):
            break

    # Now create the User object after password is validated
    user = User(name, email, password, gender, marital_status)

    # Booking process
    while True:
        print("\nAvailable Flights:")
        for idx, flight in enumerate(flights, 1):
            print(f"{idx}. {flight}")

        departure = input("\nEnter departure city: ")
        destination = input("Enter destination city: ")

        available_flights = user.search_flights(flights, departure, destination)

        if available_flights:
            print("\nAvailable Flights:")
            for idx, flight in enumerate(available_flights, 1):
                print(f"{idx}. {flight}")

            flight_choice = input("Select a flight number to book (1, 2, 3...): ")
            if not flight_choice.isdigit() or int(flight_choice) < 1 or int(flight_choice) > len(available_flights):
                print("Invalid choice. Please enter a valid number corresponding to the flight.")
                continue

            selected_flight = available_flights[int(flight_choice) - 1]

            # Class Selection
            print("\nAvailable Classes and Prices:")
            print("1. First Class - $400")
            print("2. Business Class - $300")
            print("3. Premium Economy - $250")
            print("4. Economy - $180")
            class_choice = input("Select a class (1, 2, 3, 4): ")

            if class_choice == '1':
                seats = ['A', 'B'] * 5  # First Class: 2 seats per row
                price = 400
                rows = 5
            elif class_choice == '2':
                seats = ['A', 'B'] * 5  # Business Class: 2 seats per row
                price = 300
                rows = 5
            elif class_choice == '3':
                seats = ['A', 'B', 'C'] * 4  # Premium Economy: 3 seats per row
                price = 250
                rows = 4
            elif class_choice == '4':
                seats = ['A', 'B', 'C', 'D'] * 3  # Economy: 4 seats per row
                price = 180
                rows = 3
            else:
                print("Invalid class choice.")
                continue

            # Display available seats in row and seat format (e.g., 2B, E8)
            print(f"\nAvailable seats in {['First Class', 'Business Class', 'Premium Economy', 'Economy'][int(class_choice)-1]}:")
            for i in range(rows):
                row_seats = [f"{i+1}{seat}" for seat in seats[i*2:(i+1)*2]]
                print(" ".join(row_seats))

            seat_choice = input("Select a seat (e.g., 2B, 3A): ")
            if seat_choice not in [f"{i+1}{seat}" for i in range(rows) for seat in seats[i*2:(i+1)*2]]:
                print("Invalid seat choice. Please try again.")
                continue

            passenger_name = input("Enter passenger name: ")
            while not validate_name(passenger_name):
                passenger_name = input("Enter passenger name: ")

            user.book_flight(selected_flight, passenger_name, seat_choice)

            print(f"\nBooking Details: {selected_flight}")
            print(f"Class: {['First Class', 'Business Class', 'Premium Economy', 'Economy'][int(class_choice)-1]}")
            print(f"Seat: {seat_choice}")
            print(f"Price: ${price}")

            satisfied = input("Are you satisfied with your booking? (yes/no): ").strip().lower()
            if satisfied == 'yes':
                print(f"Booking confirmed! Ticket ID: {user.bookings[-1].booking_id}")
                payment_choice = choose_payment_plan()
                print(f"Payment option {payment_choice} selected.")
                print("THANK YOU FOR CHOOSING AIR UGANDA! Be sure to book with us to go anywhere around the world. CHEERS!!")
                break
            elif satisfied == 'no':
                change_flight = input("Do you want to select a different flight? (yes/no): ").strip().lower()
                if change_flight == 'no':
                    print("Too bad :(. We hope you enjoyed the interaction though... Feel free to book with us to go anywhere around the world. CHEERS!!")
                    break
        else:
            print("No available flights for the selected route.")


if __name__ == "__main__":
    main()
