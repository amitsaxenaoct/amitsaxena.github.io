import requests
import json

global api_key
api_key = 'f4c5a2b9524db2d336d293eef88b3c3f'


# Below section is to call the location by city, state api, and get the json response for lat and long-

def search_city():
    us_city = input("\nPlease enter the city name- ").upper()
    while True:
        try:
            us_state = str(input("Please enter the state code in 2 characters- ")).upper()
            if len(us_state) == 2 and "AA" < us_state < "ZZ":
                break
            else:
                print("Please try again. Enter only 2 alphabetic characters- ")
                continue
        except ValueError:
            print("Correct value not entered.")
            continue

    api_url_city = "http://api.openweathermap.org/geo/1.0/direct?q="\
                   + us_city + "," + us_state + "," + "us&limit=5&appid=" + api_key

    response = requests.get(api_url_city)
    info_weather = response.json()  # storing response as dictionary
    global lat
    global long
    lat = str((info_weather[0])['lat'])
    long = str((info_weather[0])['lon'])
    global state
    state = (info_weather[0])['state']

    temp_uom()


# Below section is to call the location by zip code, and get the json response for lat and long-

def search_zip():
    while True:
        try:
            zip_code = input("Please enter the 5 digit zip code- ")
            if 00000 < int(zip_code) < 99999:
                break
            else:
                print("Please try again. Enter a valid zip code.")
                continue
        except ValueError:
            print("Correct value not entered")
            continue

    api_url_zip = "http://api.openweathermap.org/geo/1.0/zip?zip="\
                  + zip_code + ",us&appid=" + api_key

    response = requests.get(api_url_zip)
    info_weather = response.json()  # storing response as dictionary
    global lat
    global long
    lat = str(info_weather['lat'])
    long = str(info_weather['lon'])

    # Below section is to perform reverse geocoding from zip to find the state-

    api_url_rev = "http://api.openweathermap.org/geo/1.0/reverse?lat="\
                  + lat + "&lon=" + long + "&appid=" + api_key

    response = requests.get(api_url_rev)
    loc_info = response.json()
    global state
    state = (loc_info[0])['state']

    temp_uom()


#  Below section is to define a function for temperature uom and fetch weather data-

def temp_uom():
    global temp_unit
    global temp_unit_type
    while True:
        temp_unit = input("\nSelect the unit for temperature data: F for Fahrenheit,"
                          " C for Celcius, or K to default to Kelvin: ").upper()
        if temp_unit == "F":
            temp_unit_type = "imperial"
            break
        elif temp_unit == "C":
            temp_unit_type = "metric"
            break
        elif temp_unit == "K":
            temp_unit_type = "K"
            break
        else:
            print("Only F, C or K possible as units for temperature")

    #  Below section is to fetch the weather data from the api by lat & long

    api_url_w = "https://api.openweathermap.org/data/2.5/weather?lat="\
                + lat + "&lon=" + long + "&units=" + temp_unit_type + "&appid=" + api_key

    response = requests.get(api_url_w)
    global weather_data
    weather_data = response.json()  # storing response as weather_data

    pretty_print()


#  Below section is to define print function-

def pretty_print():
    print("\n\033[1m")
    print("=" * 50)
    print("\nCurrent weather for", weather_data['name'], ",", state)
    print("\n")
    print("=" * 50, "\033[0m")
    print("\n|  Conditions Outside:", " " * 7, "|", " " * 2, weather_data['weather'][0]['main'],
          "\n\n|  Cloud:", " " * 20, "|", " " * 2, weather_data['weather'][0]['description'],
          "\n\n|  Current Temperature:", " " * 6, "|", " " * 2, weather_data['main']['temp'], "°", temp_unit,
          "\n\n|  Feels Like:", " " * 15, "|", " " * 2, weather_data['main']['feels_like'], "°", temp_unit,
          "\n\n|  Min Temperature:", " " * 10, "|", " " * 2, weather_data['main']['temp_min'], "°", temp_unit,
          "\n\n|  Max Temperature:", " " * 10, "|", " " * 2, weather_data['main']['temp_max'], "°", temp_unit,
          "\n\n|  Pressure:", " " * 17, "|", " " * 2, weather_data['main']['pressure'], "hPa",
          "\n\n|  Humidity:", " " * 17, "|", " " * 2, weather_data['main']['humidity'], "%",
          "\n\n|  Visibility:", " " * 15, "|", " " * 2, weather_data['visibility'], "m",
          "\n\n|  Wind Speed:", " " * 15, "|", " " * 2, weather_data['wind']['speed'], "mps")
    print("\n\033[1m")
    print("=" * 50, "\033[0m")


# Function to check if the location is city or zip-

def location_check():
    while True:
        try:
            option = input("\nEnter C to search the weather by 'City' or Z to search by 'zip code'- ").upper()
            if option == "C":
                search_city()
                break
            elif option == "Z":
                search_zip()
                break
            # elif option == "E":
            #     print("\nThank you for trying the program!")
            #     break
            else:
                print("\nIncorrect entry, please try again.")
        except Exception as e:
            print("Location not found, please try again.")
            break


# Define main function-

def main():
    print("Welcome to the Weather Program!")
    location_check()
    while True:  # multi call option
        try:
            continue_check = input("\nEnter Y to perform another weather lookup, or E to exit-  ").upper()
            if continue_check == "Y":
                location_check()
            elif continue_check == "E":
                print("\nThanks for trying my program!")
                break
            else:
                print("\nPlease enter either Y to search again; or E to exit- ")
        except:
            print("\nIncorrect entry, please try again.")
            break


if __name__ == "__main__":  # main method
    main()