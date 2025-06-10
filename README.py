import pwinput
import pickle
import os

class Book_My_Car:
    def __init__(self):
        self.cars = {
            "Regular": {
                "R001": ["Honda City", 1000, "Available"],
                "R002": ["Hyundai i10", 900, "Available"],
                "R003": ["Suzuki Swift", 950, "Available"],
                "R004": ["Ford Figo", 980, "Available"],
                "R005": ["Toyota Etios", 970, "Available"],
                "R006": ["Volkswagen Polo", 960, "Available"],
                "R007": ["Tata Tiago", 850, "Available"],
                "R008": ["Renault Kwid", 800, "Available"],
                "R009": ["Maruti Alto", 750, "Available"],
                "R010": ["Honda Brio", 920, "Available"]
            },
            "Luxury": {
                "L001": ["BMW 5 Series", 5000, "Available"],
                "L002": ["Mercedes-Benz E-Class", 5500, "Available"],
                "L003": ["Audi A6", 5200, "Available"],
                "L004": ["Jaguar XF", 5300, "Available"],
                "L005": ["Lexus ES", 5100, "Available"]
            }
        }
        self.rented_cars = {}
        self.charge_per_hour = 10
        self.charge_per_day = 500
        self.discount_days = 7
        self.discount_rate = 0.10
        self.load_data()   # Load saved data when program starts

    def save_data(self):
        with open("cars_data.pkl", "wb") as f:
            pickle.dump((self.cars, self.rented_cars), f)

    def load_data(self):
        if os.path.exists("cars_data.pkl"):
            with open("cars_data.pkl", "rb") as f:
                self.cars, self.rented_cars = pickle.load(f)

    def add_car(self):
        while True:
            category = input("Enter car category (Regular/Luxury): ").capitalize()
            if category in ["Regular", "Luxury"]:
                break
            print("Invalid category! Please enter either 'Regular' or 'Luxury'.")

        while True:
            car_id = input("Enter new Car ID: ").upper()
            if car_id not in self.cars[category]:
                break
            print("Car ID already exists! Please enter a unique ID.")

        car_name = input("Enter car name: ")

        while True:
            try:
                price = float(input("Enter rental price per day: "))
                if price <= 0:
                    print("Price must be positive.")
                    continue 
                break
            except ValueError:
                print("Enter a valid number.")
        
        self.cars[category][car_id] = [car_name, price, "Available"]
        self.save_data()
        print("Car added successfully!")

    def remove_car(self):
        category = input("Enter car category (Regular/Luxury): ").capitalize()
        car_id = input("Enter Car ID to remove: ").upper()
        if car_id in self.cars.get(category, {}):
            del self.cars[category][car_id]
            self.save_data()
            print("Car removed successfully!")
        else:
            print("Invalid Car ID!")

    def rent_car(self):
        while True:
            category = input("Enter car category (Regular/Luxury): ").capitalize()
            if category in ["Regular", "Luxury"]:
                break
            print("Invalid category! Please enter 'Regular' or 'Luxury'.")
        
        car_id = input("Enter Car ID: ").upper()
        if car_id not in self.cars.get(category, {}):
            print("Invalid Car ID!")
            return
        
        if self.cars[category][car_id][2] != "Available":
            print("Car not available!")
            return
        
        while True:
            ride_type = input("Enter ride type (Daily/Rental): ").capitalize()
            if ride_type in ["Daily", "Rental"]:
                break
            print("Invalid ride type! Please enter 'Daily' or 'Rental'.")
        
        driver_needed = True  # Default to True for Daily rides

        if ride_type == "Daily":
            hours = int(input("Enter number of hours: "))
            base_cost = (self.cars[category][car_id][1] / 24) * hours
            driver_cost = self.charge_per_hour * hours  # Driver is always applicable
        else:
            days = int(input("Enter number of days: "))
            driver_needed = input("Do you need a driver? (yes/no): ").lower() == "yes"
            base_cost = self.cars[category][car_id][1] * days
            driver_cost = self.charge_per_day * days if driver_needed else 0
          
            if days >= self.discount_days:
                discount = self.discount_rate * base_cost
                base_cost -= discount
                print(f"Discount applied: {discount}")
        
        total_cost = base_cost + driver_cost
        self.cars[category][car_id][2] = "Rented"
        self.rented_cars[car_id] = [ride_type, total_cost, driver_needed, False]
        self.save_data()
        print(f"Car rented. Total cost: {total_cost} (Driver: {driver_needed}) Payment pending!")
  
    def make_payment(self):
        attempts = 3
        while attempts > 0:
            car_id = input("Enter car id for payment: ").upper()
            if car_id in self.rented_cars:
                details = self.rented_cars[car_id]

                if len(details) < 4:
                    details.append(False)

                if details[3]:
                    print("Payment Already Done!")
                else:
                    print(f"Amount to be paid {details[1]}")
                    confirm = input("Confirm Payment? (Yes or No): ").upper()
                    if confirm == "YES":
                        self.rented_cars[car_id][3] = True
                        self.save_data()
                        print("Payment Successful!!")
                        return
                    else:
                        print("Payment Not Completed!")
                        return
            else:
                attempts -= 1
                print(f"This Car ID Not Rented. Please Enter Valid Car ID! \n{attempts} attempts left!")

    def return_car(self):
        car_id = input("Enter Car ID to return: ").upper()
        for category in self.cars:
            if car_id in self.cars[category]:
                if self.cars[category][car_id][2] == "Rented":
                    if car_id in self.rented_cars and not self.rented_cars[car_id][3]:
                        print("Payment not Completed. Please pay before Returning!")
                        return

                    self.cars[category][car_id][2] = "Available"
                    del self.rented_cars[car_id]
                    self.save_data()
                    print("Car returned successfully!")
                    return
                else:
                    print("This car is not rented.")
                    return
        print("Invalid Car ID!")

    def view_all_cars(self):
        print("All Cars:")
        for category, cars in self.cars.items():
            for car_id, details in cars.items():
                print(f"{category} - {car_id}: {details[0]}, Price: {details[1]}, Status: {details[2]}")

    def view_available_cars(self):
        print("Available Cars:")
        for category, cars in self.cars.items():
            for car_id, details in cars.items():
                if details[2] == "Available":
                    print(f"{category} - {car_id}: {details[0]}, Price: {details[1]}")
    
    def view_rented_cars(self):
        if not self.rented_cars:
            print("No cars are currently rented.")
        else:
            print("Rented Cars:")
            for car_id, details in self.rented_cars.items():
                print(f"Car ID: {car_id},Ride Type: {details[0]}, Total Cost: {details[1]}, Driver Needed: {details[2]}")

if __name__ == "__main__":
    system = Book_My_Car()

    while True:
        user_type = input("\nAre you an Admin, a User, or do you want to Exit? (Admin/User/Exit): ").capitalize()

        if user_type == 'Exit'.capitalize():
            break
    
        elif user_type == "Admin":
            admin_pass = "admin@123"
            attempts = 3
            while attempts > 0:
                i = pwinput.pwinput(prompt="Enter admin password: ", mask='*')
                if admin_pass == i:
                    break
                else:
                    attempts -= 1
                    print(f"Wrong Password. {attempts} attempts left!")
        
            if i == admin_pass:
                print("Access granted!")
                while True:
                    print("\n1. Add a Car\n2. Remove a Car\n3. View All Cars\n4. View Available Cars\n5. View Rented Cars\n6. Exit")
                    choice = input("Enter your choice: ")
                    if choice == "1":
                        system.add_car()
                    elif choice == "2":
                        system.remove_car()
                    elif choice == "3":
                        system.view_all_cars()
                    elif choice == "4":
                        system.view_available_cars()
                    elif choice == "5":
                        system.view_rented_cars()
                    elif choice == "6":
                        print("Logging Out Admin!")
                        break
                    else:
                        print("Invalid choice! Please enter a number from 1 to 6.")
            else:
                print("Access denied! Try again.")

        elif user_type == "User":
            while True:
                print("\n1. View Available Cars\n2. Rent a Car\n3. Make Payment \n4. Return a Car\n5. Exit")
                choice = input("Enter your choice: ")
                if choice == "1":
                    system.view_available_cars()
                elif choice == "2":
                    system.rent_car()
                elif choice == "3":
                    system.make_payment()
                elif choice == "4":
                    system.return_car()
                elif choice == "5":
                    print("Logging Out User!")
                    break
                else:
                        print("Invalid choice! Please enter a number from 1 to 6.")
        else:
            print("Invalid input! Please enter 'Admin', 'User' or 'Exit'.")
