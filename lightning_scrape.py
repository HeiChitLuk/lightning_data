import json
import requests
from datetime import datetime

def scrape_lightning_data(url, output_file="lightning_data.json"):
    try:
        # Make the API request
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        json_data = response.json()  # Parse the JSON response
        
        # Extract last update time and strikes from new data
        
        new_strikes = json_data["lightning_strikes"]
        
        # Load existing data if file exists
        try:
            with open(output_file, 'r') as f:
                existing_data = json.load(f)
        except FileNotFoundError:
            # If file doesn't exist, start with empty data
            existing_data = {
                "lightning_strikes": [],
                "total_strikes": 0
            }
        
        # Extract existing strikes
        existing_strikes = existing_data["lightning_strikes"]
        
        # Check for new unique strikes (based on strike_time and coordinates)
        unique_new_strikes = []
        for new_strike in new_strikes:
            is_duplicate = False
            for existing_strike in existing_strikes:
                if (new_strike["strike_time"] == existing_strike["strike_time"] and 
                    new_strike["coordinates"] == existing_strike["coordinates"]):
                    is_duplicate = True
                    break
            if not is_duplicate:
                unique_new_strikes.append(new_strike)
        
        # Combine strikes
        updated_strikes = existing_strikes + unique_new_strikes
        total_strikes = len(updated_strikes)
        
        # Update last_update only if newer
        
        # Print the results
        print("\nNew Lightning Strikes Added:")
        if unique_new_strikes:
            for strike in unique_new_strikes:
                strike_time = strike["strike_time"]
                coords = strike["coordinates"]
                print(f"Time: {strike_time}")
                print(f"Coordinates: Latitude {coords[1]}, Longitude {coords[0]}")
                print("---")
        else:
            print("No new strikes to add.")
        
        print(f"\nTotal number of strikes in file: {total_strikes}")
        
        # Prepare updated data to save
        data_to_save = {
            "lightning_strikes": updated_strikes,
            "total_strikes": total_strikes
        }
        
        # Save to JSON file
        with open(output_file, 'w') as f:
            json.dump(data_to_save, f, indent=4)
        print(f"\nData updated in {output_file}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {str(e)}")
    except KeyError as e:
        print(f"Data format error: {str(e)}")
    except Exception as e:
        print(f"Error occurred: {str(e)}")

# URL provided
url = "https://data.consumer-digital.api.metoffice.gov.uk/v1/lightning"

# Call the function
scrape_lightning_data(url)