import tkinter as tk
from tkinter import messagebox
import mysql.connector

class RailwayReservationSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Railway Reservation System")

        self.menu_label = tk.Label(self.root, text="WELCOME TO RAILWAY RESERVATION SYSTEM", font=("Arial", 16))
        self.menu_label.pack(pady=20)

        # Buttons for various functionalities
        self.book_ticket_btn = tk.Button(self.root, text="Book a Ticket", command=self.booking_form)
        self.book_ticket_btn.pack(pady=10)

        self.cancel_booking_btn = tk.Button(self.root, text="Cancel a Booking", command=self.cancel_booking)
        self.cancel_booking_btn.pack(pady=10)

        self.check_fare_btn = tk.Button(self.root, text="Check Fares", command=self.check_fare)
        self.check_fare_btn.pack(pady=10)

        self.show_bookings_btn = tk.Button(self.root, text="Show my Bookings", command=self.show_bookings)
        self.show_bookings_btn.pack(pady=10)

        self.available_trains_btn = tk.Button(self.root, text="Show Available Trains", command=self.available_trains)
        self.available_trains_btn.pack(pady=10)

        self.clear_screen_btn = tk.Button(self.root, text="Clear Screen", command=self.clear_screen)
        self.clear_screen_btn.pack(pady=10)

        self.about_btn = tk.Button(self.root, text="About", command=self.about)
        self.about_btn.pack(pady=10)

        self.exit_btn = tk.Button(self.root, text="Exit", command=root.quit)
        self.exit_btn.pack(pady=10)

        self.db_connection()

    def db_connection(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="railway"
            )
            self.cursor = self.conn.cursor()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def booking_form(self):
        booking_window = tk.Toplevel(self.root)
        booking_window.title("Book a Ticket")

        tk.Label(booking_window, text="Train Number:").grid(row=0, column=0)
        self.train_entry = tk.Entry(booking_window)
        self.train_entry.grid(row=0, column=1)

        tk.Label(booking_window, text="Name:").grid(row=1, column=0)
        self.name_entry = tk.Entry(booking_window)
        self.name_entry.grid(row=1, column=1)

        tk.Label(booking_window, text="Age:").grid(row=2, column=0)
        self.age_entry = tk.Entry(booking_window)
        self.age_entry.grid(row=2, column=1)

        tk.Label(booking_window, text="Class:").grid(row=3, column=0)
        self.class_var = tk.StringVar(value="Sleeper")
        tk.OptionMenu(booking_window, self.class_var, "Sleeper", "AC-1", "AC-2", "AC-3").grid(row=3, column=1)

        tk.Label(booking_window, text="Source:").grid(row=4, column=0)
        self.source_entry = tk.Entry(booking_window)
        self.source_entry.grid(row=4, column=1)

        tk.Label(booking_window, text="Destination:").grid(row=5, column=0)
        self.destination_entry = tk.Entry(booking_window)
        self.destination_entry.grid(row=5, column=1)

        tk.Button(booking_window, text="Book Ticket", command=self.book_train).grid(row=6, columnspan=2)

    def book_train(self):
        train_number = self.train_entry.get()
        name = self.name_entry.get()
        age = self.age_entry.get()
        train_class = self.class_var.get()
        source = self.source_entry.get()
        destination = self.destination_entry.get()

        # Check if all fields are filled
        if not all([train_number, name, age, train_class, source, destination]):
            messagebox.showwarning("Incomplete Data", "Please fill out all fields.")
            return

        try:
            # Query to verify that the train number, source, and destination match in the train_info table
            verify_query = """
                SELECT COUNT(*) FROM train_info
                WHERE Train_No = %s AND Source_Station_Code = %s AND Destination_Station_Name = %s
            """
            self.cursor.execute(verify_query, (train_number, source, destination))
            result = self.cursor.fetchone()

            if result[0] == 0:
                # No matching train info entry found
                messagebox.showerror("Invalid Route", "The source and destination do not match any train route.")
                return

            # Proceed with booking if the train info is valid
            insert_query = """
                INSERT INTO booking (train_number, name, age, train_class, source, destination) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            self.cursor.execute(insert_query, (train_number, name, age, train_class, source, destination))
            self.conn.commit()
            messagebox.showinfo("Success", "Ticket booked successfully!")

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to book ticket: {err}")
        except Exception as e:
            messagebox.showerror("Unknown Error", f"An unexpected error occurred: {e}")

    def cancel_booking(self):
        cancel_window = tk.Toplevel(self.root)
        cancel_window.title("Cancel Booking")

        tk.Label(cancel_window, text="Booking ID:").grid(row=0, column=0)
        self.booking_id_entry = tk.Entry(cancel_window)
        self.booking_id_entry.grid(row=0, column=1)

        tk.Button(cancel_window, text="Cancel Booking", command=self.perform_cancellation).grid(row=1, columnspan=2)

    def perform_cancellation(self):
        booking_id = self.booking_id_entry.get()
        try:
            query = "DELETE FROM booking WHERE id = %s"
            self.cursor.execute(query, (booking_id,))
            self.conn.commit()
            if self.cursor.rowcount > 0:
                messagebox.showinfo("Success", "Booking cancelled successfully!")
            else:
                messagebox.showwarning("Not Found", "Booking ID not found.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to cancel booking: {err}")

    def check_fare(self):
        fare_window = tk.Toplevel(self.root)
        fare_window.title("Check Fare")

        tk.Label(fare_window, text="Source Station:").grid(row=0, column=0)
        self.source_fare_entry = tk.Entry(fare_window)
        self.source_fare_entry.grid(row=0, column=1)

        tk.Label(fare_window, text="Destination Station:").grid(row=1, column=0)
        self.destination_fare_entry = tk.Entry(fare_window)
        self.destination_fare_entry.grid(row=1, column=1)

        tk.Label(fare_window, text="Class:").grid(row=2, column=0)
        self.fare_class_var = tk.StringVar(value="Sleeper")
        tk.OptionMenu(fare_window, self.fare_class_var, "Sleeper", "AC-1", "AC-2", "AC-3").grid(row=2, column=1)

        tk.Button(fare_window, text="Check Fare", command=lambda: self.display_fare(self.source_fare_entry.get(), self.destination_fare_entry.get(), self.fare_class_var.get())).grid(row=3, columnspan=2)

    def display_fare(self, source, destination, train_class):
        fare = 2000  # Placeholder fare logic
        messagebox.showinfo("Fare", f"The fare from {source} to {destination} in {train_class} class is {fare}.")

    def show_bookings(self):
        bookings_window = tk.Toplevel(self.root)
        bookings_window.title("My Booking")

        try:
            self.cursor.execute("SELECT * FROM booking")
            bookings = self.cursor.fetchall()

            for i, booking in enumerate(bookings):
                tk.Label(bookings_window, text=f"ID: {booking[0]}, Train: {booking[1]}, Name: {booking[2]}, Age: {booking[3]}, Class: {booking[4]}, Source: {booking[5]}, Destination: {booking[6]}").grid(row=i, column=0, sticky="w")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to retrieve booking: {err}")

    def available_trains(self):
        trains_window = tk.Toplevel(self.root)
        trains_window.title("Available Trains")

        tk.Label(trains_window, text="Source:").grid(row=0, column=0)
        self.source_trains_entry = tk.Entry(trains_window)
        self.source_trains_entry.grid(row=0, column=1)

        tk.Label(trains_window, text="Destination:").grid(row=1, column=0)
        self.destination_trains_entry = tk.Entry(trains_window)
        self.destination_trains_entry.grid(row=1, column=1)

        tk.Button(trains_window, text="Show Available Trains", command=lambda: self.display_available_trains(self.source_trains_entry.get(), self.destination_trains_entry.get())).grid(row=2, columnspan=2)

    def display_available_trains(self, source, destination):
        trains = [("12345", "Train A", source, destination), ("67890", "Train B", source, destination)]
        trains_window = tk.Toplevel(self.root)
        trains_window.title("Available Trains List")
        for i, train in enumerate(trains):
            tk.Label(trains_window, text=f"Train No: {train[0]}, Name: {train[1]}, Source: {train[2]}, Destination: {train[3]}").grid(row=i, column=0, sticky="w")

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.pack_forget()
        self.__init__(self.root)

    def about(self):
        messagebox.showinfo("About", "Railway Reservation System v1.0\nDeveloped using Python and Tkinter.")

if __name__ == "__main__":
    root = tk.Tk()
    app = RailwayReservationSystem(root)
    root.mainloop()
