import time
import datetime
import json
import os
import logging
import re

#---------------------------------------------------------------------------------------
os.makedirs("intermediate_level", exist_ok=True)

logging.basicConfig(
    filename=os.path.join("intermediate_level", "logs_ride.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

#---------------------------------------------------------------------------------------
def register_user():
    user_id = 1
    users = load_users()

    if users:
        user_id = max(user["id"] for user in users) + 1
    
    user_name = input("Introduce your name: ")
    user_email = input ("Introduce your email address:")
    password = asking_password()

    new_user = {"id": user_id, "user_name": user_name, "user_email":user_email, "password": password}

    users.append(new_user)
    save_users(users)
    logging.info(f"New user has been registered.")
    print(f"Hello {user_name} you have been successfully registered under id '{user_id}'.")

#---------------------------------------------------------------------------------------
def asking_password():
    while True:
        password =input("Introduce a password with minimum 8 characters, at least one upppercase, one lowercase and one digit:")
        if validate_password(password):
            return password
        else:
            print("The password is too weak. please try another.")

#---------------------------------------------------------------------------------------
def validate_password(password):
    if (len(password) < 8 or
        not re.search(r"[A-Z]", password) or
        not re.search(r"[a-z]", password) or
        not re.search(r"[0-9]", password)):
        return False
    return True

#---------------------------------------------------------------------------------------
user_data_path = os.path.join("intermediate_level", "users.json")

def load_users():
    if not os.path.exists(user_data_path):
        return []
    with open(user_data_path, "r") as file:
        return json.load(file)
    logging.info("A REVISAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAARRRRRRRRRRRRRR")
#---------------------------------------------------------------------------------------
def save_users(users):
    with open(user_data_path, "w") as file:
        json.dump(users, file)

#---------------------------------------------------------------------------------------
def asking_credentials():
    identifier = input("Introduce your name or email address: ")
    password = input("Introduce your password: ")

    users = load_users()
    for user in users:
        if (user ['user_name'] == identifier or user ['user_email'] == identifier) and user ['password'] == password:
            return True
    print(f"Incorrect password. Try again.")
    return False

#---------------------------------------------------------------------------------------
def show_welcome():
    logging.info("Welcome/Instructions message showned.")
    print("\n--- Welcome to your taximeter!  🚕 ---")
    print("""This program calculates the fare in km of a ride in euros.
            \n let me show you how we work first 😉

            The rates used are as follows:

            ⏸️ Taxi stopped: 2 cents per second.
            ▶️ Taxi in motion: 5 cents per second.
            ⬆️ High demand level: extra 10%.
            ⬇️ Low demand level: minus 10%.""")

    print("""\nCommands are:\n

            Next when you are on a ride you must use the follow accordingly:\n

            ▶️ Start:  Press 'Enter' to begin a trip.\n
            ⏸️ Stop:   Type 'stop' when the taxi is stationary.\n
            ⏯️ Go:     Type 'go' when the taxi is in motion.\n
            ⏹️ End:    Type 'end' to end the trip.\n
            
            ❌ To exit the taximeter, please press 'Escape'.""")
#---------------------------------------------------------------------------------------

def load_rates():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    rates_file_path = os.path.join(current_dir, "rates.json")

    try:
        with open(rates_file_path, "r") as file:
            json_data = json.load(file)  
        return json_data["rates"]  
    except Exception as e:
        logging.error(f"Error loading fare rates: {e}")
        return None 

rates = load_rates()
#---------------------------------------------------------------------------------------

def demand_level():
    now = datetime.datetime.now()
    month = now.month
    weekday = now.weekday()
    hour = now.hour

    month_high_demand = [6,7,9,12]
    month_low_demand = [2,3,4,11]
    
    hour_high_demand_week = list(range(7, 10)) + list(range(18, 22))
    hour_high_demand_saturday = list(range(1, 4)) + list(range(22, 24)) 
    hour_high_demand_sunday = list(range(18,21))

    if weekday < 5: # meter variables para que el 5 sea comprensible como día de la semana
        high_demand_hour = hour_high_demand_week
    elif weekday == 5:
        high_demand_hour = hour_high_demand_saturday
    else:
        high_demand_hour = hour_high_demand_sunday 

    if month in month_high_demand and hour in high_demand_hour:
        logging.info("High demand detected")
        return "🔴 High Demand: Extra percentage will be applied during rush hours."
    elif month in month_low_demand and hour  not in high_demand_hour:
        logging.info("Low demand detected")
        return "🟢 Low Demand: Discounted rate for off-peak hours will be applied."
    else: 
        logging.info("Normal demand detected")
        return "🟡 Normal: Standard rate used during regular traffic conditions."
#---------------------------------------------------------------------------------------

def history_ride(total_ride, demand_multiplier):

    total_ride = round(total_ride, 2)

    demand_multipliers = {
        "normal": 1.0,
        "low": 0.9,
        "high": 1.1
    }

    demand_type = next((key for key, value in demand_multipliers.items() if value == demand_multiplier), "unknown")

    now = datetime.datetime.now()
    formatted_timestamp = now.strftime("%A %d %b %Y at %H:%M:%S")

    # Create history_ride entry
    history_entry = {
        "total_ride": total_ride,
        "demand": {
            "type": demand_type, 
            "multiplier": demand_multiplier  
        },
        "timestamp": formatted_timestamp  
    }


    history_folder = "intermediate_level"
    history_path = os.path.join(history_folder, "history_ride.json")
    os.makedirs(history_folder, exist_ok=True)

    try:
        with open(history_path, "a") as history_file:
            json.dump(history_entry, history_file)
            history_file.write("\n")
        logging.info(f"Ride succesfully registered.")  
    except Exception as e:
        logging.error(f"Error saving ride history: {e}")
#---------------------------------------------------------------------------------------
def logs_ride (message, level="INFO"):
    timestamp = datetime.datetime.now().isoformat()
    log_entry = f"{timestamp} - {level} - {message}"

    logs_folder = "intermediate_level"
    logs_path = os.path.join(logs_folder, "logs_ride.log")
    os.makedirs(logs_folder, exist_ok=True)

    try:
        with open(logs_path, "a") as logs_file:
            logs_file.write(log_entry) 
    except Exception as e:
        logging.error(f"Error saving ride logs: {e}")

#---------------------------------------------------------------------------------------

def ride():

    if not asking_credentials():
        return
    
    rate_stationary = rates["base"]["stationary"]
    rate_motion = rates["base"]["motion"]
    
    while True:
        input("Press ENTER to start a new ride 🚖...")
        logging.info("New ride on going.")
        print("""Let's go! 💨"
              Type the below accordingly:
              ⏸️ Stop
              ⏯️ Go
              ⏹️ End""")
        
        total_stationary = 0
        total_motion = 0
        total_ride = 0
        start_taximeter = time.time()

        while True:
            input_rider = input("Enter: ⏸️ Stop, ⏯️ Go or ⏹️ End: ").strip().lower()
            elapsed_time = time.time() - start_taximeter
            
            if input_rider == "stop":
                total_stationary += elapsed_time * rate_stationary
                print(f"Taxi stopped. Elapsed time: {elapsed_time:.2f}secs, Rate: {total_stationary:.2f}€")
                start_taximeter = time.time()
            
            elif input_rider == "go":
                total_motion += (time.time() - start_taximeter) * rate_motion
                print(f"Taxi in motion. Elapsed time: {elapsed_time:.2f}secs, Rate: {rate_motion:.2f}€")
                start_taximeter = time.time()
            
            elif input_rider == "end":
                total_ride = total_motion + total_stationary
                demand_multiplier = rates["demand_multipliers"]["normal"]  # Default multiplier
                demand_status = demand_level()
                
                if demand_status == "high":
                    demand_multiplier = rates["demand_multipliers"]["high"]
                elif demand_status == "low":
                    demand_multiplier = rates["demand_multipliers"]["low"]
                
                total_ride *= demand_multiplier
                print(f"\nRide ended. Elapsed time: {elapsed_time:.2f}secs, TOTAL RATE: {total_ride:.2f}€ (after demand adjustment)\n")
                
                history_ride(total_ride, demand_multiplier)
                break
            
            else:
                logging.warning(f"Invalid input received by user: '{input_rider}'")
                print("Invalid input. Enter: ⏸️ Stop, ⏯️ Go or ⏹️ End: ")
        
        print("Do you want to enter a new ride? ✅ Yes ❌ No : ")
        input_restart = input("Type '✅ Yes' if you want a new ride: ").strip().lower()
        if input_restart != 'yes':
            logging.info(f"User has finalized the trip sequence.")
            print("Thank you for using Taximeter! Hope to see you again 👋!")
            break
        else:
            logging.info("New ride on going under the user's session.")
            print(f"New ride in progress 🚖")
            continue
#---------------------------------------------------------------------------------------

if __name__ == "__main__":
    show_welcome()  # Show the welcome message and instructions
    rates = load_rates()  # Load the rates and store them in a variable
    register_user()
    ride()  # Start the ride process
   
