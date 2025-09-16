import tkinter as tk
from tkinter import messagebox
from tkinter import font
import requests
import webbrowser


def book_flight(flight_number):
    # Open the respective flight's website
    url = f"https://www.google.com/travel/flights"
    webbrowser.open(url)

def search_flights():
    departure = departure_entry.get()
    arrival = arrival_entry.get()

    if departure and arrival:
        api_key = "b0f4658b5bb7691e73e1632a5d0e5323"
        url = f"http://api.aviationstack.com/v1/flights?access_key={api_key}&dep_iata={departure}&arr_iata={arrival}"

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            if data["pagination"]["total"] > 0:
                flight_details_window = tk.Toplevel(home_window)
                flight_details_window.title("Flight Details")
                flight_details_window.geometry("1920x1080")
                flight_details_window.configure(bg="white")

                title_font = font.Font(family="Helvetica", size=24, weight="bold")
                label_font = font.Font(family="Helvetica", size=16)
                button_font = font.Font(family="Helvetica", size=16, weight="bold")

                title_label = tk.Label(flight_details_window, text="Flight Details", font=title_font, fg="black", bg="white")
                title_label.pack(pady=20)

                scroll_frame = tk.Frame(flight_details_window, bg="white")
                scroll_frame.pack(fill=tk.BOTH, expand=True)

                canvas = tk.Canvas(scroll_frame, bg="white")
                canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

                scrollbar = tk.Scrollbar(scroll_frame, orient=tk.VERTICAL, command=canvas.yview)
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

                canvas.configure(yscrollcommand=scrollbar.set)
                canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

                inner_frame = tk.Frame(canvas, bg="white")
                canvas.create_window((0, 0), window=inner_frame, anchor=tk.NW)

                for flight in data["data"]:
                    flight_number = flight["flight"]["iata"]
                    departure_airport = flight["departure"]["airport"]
                    arrival_airport = flight["arrival"]["airport"]

                    flight_frame = tk.Frame(inner_frame, bg="white", bd=1, relief=tk.RAISED, padx=10, pady=5)
                    flight_frame.pack(pady=10)

                    flight_label = tk.Label(flight_frame, text=f"Flight: {flight_number}", font=label_font, fg="black", bg="white")
                    flight_label.pack()

                    departure_label = tk.Label(flight_frame, text=f"Departure: {departure_airport}", font=label_font, fg="black", bg="white")
                    departure_label.pack()

                    arrival_label = tk.Label(flight_frame, text=f"Arrival: {arrival_airport}", font=label_font, fg="black", bg="white")
                    arrival_label.pack()

                    book_button = tk.Button(flight_frame, text="Book Flight", font=button_font, bg="gray", fg="black", command=lambda flight_number=flight_number: book_flight(flight_number))
                    book_button.pack(pady=5)

                canvas.update_idletasks()
                canvas.configure(scrollregion=canvas.bbox("all"))

            else:
                messagebox.showinfo("Search Flights", "No flights found.")
        else:
            messagebox.showerror("API Error", "Failed to fetch flight data.")
    else:
        messagebox.showerror("Search Flights", "Please enter both departure and arrival airports.")

def register():
    username = username_entry.get()
    password = password_entry.get()

    if username and password:
        credentials[username] = password
        messagebox.showinfo("Registration", "Registration successful! You can now login.")
        clear_login_fields()
    else:
        messagebox.showerror("Registration", "Please enter both username and password!")

def login():
    username = username_entry.get()
    password = password_entry.get()

    if username in credentials and credentials[username] == password:
        messagebox.showinfo("Login", "Login successful!")
        clear_login_fields()
        show_home_screen()
    else:
        messagebox.showerror("Login", "Invalid username or password!")

def clear_login_fields():
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

def show_home_screen():
    login_window.withdraw()

    global home_window
    home_window = tk.Tk()
    home_window.title("Flight Booking")
    home_window.geometry("1920x1080")
    home_window.configure(bg="white")

    title_font = font.Font(family="Helvetica", size=24, weight="bold")
    label_font = font.Font(family="Helvetica", size=16)
    button_font = font.Font(family="Helvetica", size=16, weight="bold")

    title_label = tk.Label(home_window, text="Flight Booking", font=title_font, fg="black", bg="white")
    title_label.pack(pady=20)

    global departure_entry
    departure_label = tk.Label(home_window, text="Departure Airport:", font=label_font, fg="black", bg="white")
    departure_label.pack()

    departure_entry = tk.Entry(home_window, font=label_font, bg="white", fg="black", width=15)
    departure_entry.pack()

    global arrival_entry
    arrival_label = tk.Label(home_window, text="Arrival Airport:", font=label_font, fg="black", bg="white")
    arrival_label.pack()

    arrival_entry = tk.Entry(home_window, font=label_font, bg="white", fg="black", width=15)
    arrival_entry.pack()

    search_button = tk.Button(home_window, text="Search Flights", font=button_font, bg="gray", fg="black", command=search_flights)
    search_button.pack(pady=10)

    # Start the Tkinter event loop
    home_window.mainloop()

# Create the login window
login_window = tk.Tk()
login_window.title("Login")
login_window.geometry("1920x1080")
login_window.configure(bg="white")

title_font = font.Font(family="Helvetica", size=24, weight="bold")
label_font = font.Font(family="Helvetica", size=16)
button_font = font.Font(family="Helvetica", size=16, weight="bold")

title_label = tk.Label(login_window, text="Login", font=title_font, fg="black", bg="white")
title_label.pack(pady=20)

username_label = tk.Label(login_window, text="Username:", font=label_font, fg="black", bg="white")
username_label.pack()

username_entry = tk.Entry(login_window, font=label_font, bg="white", fg="black", width=15)
username_entry.pack()

password_label = tk.Label(login_window, text="Password:", font=label_font, fg="black", bg="white")
password_label.pack()

password_entry = tk.Entry(login_window, font=label_font, bg="white", fg="black", width=15, show="*")
password_entry.pack()

login_button = tk.Button(login_window, text="Login", font=button_font, bg="gray", fg="black", command=login)
login_button.pack(pady=10)

register_button = tk.Button(login_window, text="Register", font=button_font, bg="gray", fg="black", command=register)
register_button.pack()

# Create a dictionary to store user credentials
credentials = {}

# Start the Tkinter event loop
login_window.mainloop()

