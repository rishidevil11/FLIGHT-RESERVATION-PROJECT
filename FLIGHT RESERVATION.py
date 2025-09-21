import tkinter as tk
from tkinter import messagebox
import requests
import webbrowser
from tkinter import ttk
import tkinter.font as tkFont


def book_flight(flight_number):
    # Open the respective flight's website
    url = f"https://www.google.com/travel/flights"
    webbrowser.open(url)

def search_flights():
    from tkinter import font
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
                canvas.create_window((940,240), window=inner_frame, anchor=tk.CENTER)

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
    login_window.destroy()
    global home_window
    home_window = tk.Tk()
    home_window.geometry("1920x1080")
    home_window.resizable(False,False)
    home_window.configure(bg="white")
    home_window.title("Flight Booking")

    canvas=tk.Canvas(home_window, width=600, height=600, bg="#f4f4f4")
    canvas.pack(anchor=tk.CENTER,expand=True)

    canvas.create_text((270,50),text="Book your flight",font=("Helvetica", 20,"bold"))

    global departure_entry
    canvas.create_text((110,100),text="Departure Airport",font=("Helvetica", 20,))
    departure_entry=ttk.Entry(home_window,width=30,font=('Helvetica',25))
    canvas.create_window(300,170,window=departure_entry)

    global arrival_entry
    canvas.create_text((90,245),text="Arrival Airport",font=("Helvetica", 20,))
    arrival_entry=ttk.Entry(home_window,width=30,font=('Helvetica',25))
    canvas.create_window(300,290,window=arrival_entry)

    font = tkFont.Font(size=14, weight="bold")
    style = ttk.Style()
    style.configure("Custom.TButton", font=font, padding=10)

    search_button = ttk.Button(
        home_window,
        text="Search",
        width=40,
        command=search_flights,
        style="Custom.TButton"
    )

    canvas.create_window(300, 370, window=search_button)

    home_window.mainloop()


login_window = tk.Tk()
login_window.geometry("1920x1080")
login_window.resizable(False,False)
login_window.configure(bg="white")
login_window.title("Login/Register")

canvas=tk.Canvas(login_window, width=600, height=600, bg="#f4f4f4")
canvas.pack(anchor=tk.CENTER,expand=True)

canvas.create_text((220,50),text="Login/Register into your account:",font=("Helvetica", 20,"bold"))

canvas.create_text((75,100),text="Username:",font=("Helvetica", 20,))
username_entry=ttk.Entry(login_window,width=30,font=('Helvetica',25))
canvas.create_window(300,170,window=username_entry)

canvas.create_text((75,245),text="Password:",font=("Helvetica", 20,))
password_entry=ttk.Entry(login_window,width=30,font=('Helvetica',25),show="*")
canvas.create_window(300,290,window=password_entry)

font = tkFont.Font(size=14, weight="bold")
style = ttk.Style()
style.configure("Custom.TButton", font=font, padding=10)

login_button = ttk.Button(
    login_window,
    text="Login",
    width=40,
    command=login,
    style="Custom.TButton"
)


canvas.create_window(300, 370, window=login_button)

register_button = ttk.Button(
    login_window,
    text="Register",
    width=40,
    command=register,
    style="Custom.TButton"
)
canvas.create_window(300, 460, window=register_button)

credentials = {}


login_window.mainloop()

