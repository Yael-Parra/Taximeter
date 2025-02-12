import time
import datetime
import json
import os
import logging
#---------------------------------------------------------------------------------------
os.makedirs("intermediate_level", exist_ok=True)

logging.basicConfig(
    filename= os.path.join("intermediate_level", "logs_ride.log"),
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logging.info("\nProgram started. Welcome message displayed.")

#---------------------------------------------------------------------------------------
def show_welcome():
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
        logging.error(f"Error loading rates: {e}")
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

    if weekday < 5:
        high_demand_hour = hour_high_demand_week
    elif weekday == 5:
        high_demand_hour = hour_high_demand_saturday
    else:
        high_demand_hour = hour_high_demand_sunday 

    if month in month_high_demand and hour in high_demand_hour:
        return "🔴 High Demand: Extra percentage will be applied during rush hours."
    elif month in month_low_demand and hour  not in high_demand_hour:
        return "🟢 Low Demand: Discounted rate for off-peak hours will be applied."
    else: 
        return "🟡 Normal: Standard rate used during regular traffic conditions."
#---------------------------------------------------------------------------------------

def ride_history(total_ride, demand_multiplier):

    total_ride = round(total_ride, 2)

    demand_multipliers = {
        "normal": 1.0,
        "low": 0.9,
        "high": 1.1
    }

    demand_type = next((key for key, value in demand_multipliers.items() if value == demand_multiplier), "unknown")

    now = datetime.datetime.now()
    formatted_timestamp = now.strftime("%A %d %b %Y at %H:%M:%S")

    # Create ride_history entry
    history_entry = {
        "total_ride": total_ride,
        "demand": {
            "type": demand_type,  # Now it shows "high", "low", or "normal"
            "multiplier": demand_multiplier  # Now it keeps the numeric value too
        },
        "timestamp": formatted_timestamp  # Human-readable timestamp
    }


    history_folder = "intermediate_level"
    history_path = os.path.join(history_folder, "ride_history.json")
    os.makedirs(history_folder, exist_ok=True)

    try:
        with open(history_path, "a") as history_file:
            json.dump(history_entry, history_file)
            history_file.write("\n")
        logging.info(f"Ride succesfully entered in 'ride_history.json' file.")  
    except Exception as e:
        logging.error("Error saving ride history: {e}")
#---------------------------------------------------------------------------------------
def ride_logs (message):
    log_entry = {
        "message": message,
        "timestamp": datetime.datetime.now().isoformat()
    }

    logs_folder = "intermediate_level"
    logs_path = os.path.join(logs_folder, "logs_ride.log")
    os.makedirs(logs_folder, exist_ok=True)
    

    try:
        with open(logs_path, "a") as logs_file:
            json.dump(log_entry, logs_file)
        logging.info(f"Log entry successfully added to 'ride_history.json'.")  
    except Exception as e:
        logging.error(f"Error saving ride logs: {e}")

#---------------------------------------------------------------------------------------

def ride():
    rate_stationary = rates["base"]["stationary"]
    rate_motion = rates["base"]["motion"]
    
    while True:
        input("Press ENTER to start a new ride 🚖...")
        logging.info("Let's go! 💨")
        print("""Type the below accordingly:
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
                logging.info(f"Taxi stopped. Elapsed time: {elapsed_time:.2f}secs, Rate: {total_stationary:.2f}€")
                start_taximeter = time.time()
            
            elif input_rider == "go":
                total_motion += (time.time() - start_taximeter) * rate_motion
                logging.info(f"Taxi in motion. Elapsed time: {elapsed_time:.2f}secs, Rate: {rate_motion:.2f}€")
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
                logging.info(f"\nRide ended. Elapsed time: {elapsed_time:.2f}secs, TOTAL RATE: {total_ride:.2f}€ (after demand adjustment)\n")
                
                ride_history(total_ride, demand_multiplier)
                break
            
            else:
                logging.warning(f"Invalid input received: {input_rider}")
                print("Invalid input. Enter: ⏸️ Stop, ⏯️ Go or ⏹️ End: ")
        
        print("Do you want to enter a new ride? ✅ Yes ❌ No : ")
        input_restart = input("Type '✅ Yes' if you want a new ride: ").strip().lower()
        if input_restart != 'yes':
            print("Thank you for using Taximeter! Hope to see you again 👋!")
            break
        else:
            print(f"New ride in progress 🚖")
            continue
#---------------------------------------------------------------------------------------

if __name__ == "__main__":
    show_welcome()  # Show the welcome message and instructions
    rates = load_rates()  # Load the rates and store them in a variable
    ride()  # Start the ride process
   
