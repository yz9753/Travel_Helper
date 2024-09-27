import requests
from bs4 import BeautifulSoup
import pandas as pd

# Take user inputs for city, currency, and hotel search preferences and store them as strings 
city = str(input("Please enter a city that you want to visit: ").capitalize())
currency = str(input("Please enter the currency that you want to see in: (in abbreviation, i.e. USD) ").upper())
checkin_date = str(input("Please enter your estimated check in date: (use the following format: 2024-09-24) "))
checkout_date = str(input("Please enter your estimated check out date: (use the following format: 2024-09-24) "))
order_by = str(input("How do you like to order the hotels, by popularity or price? (Type out popularity or price only) "))
adults_number = str(input("How many people are travelling? "))
room_number = str(input("How many rooms do you need in total? "))

#Construct the URL for Numbeo cost of living page for the chosen city and currency
countryPage = f"https://www.numbeo.com/cost-of-living/in/{city}?displayCurrency={currency}"

# Send a GET request to the URL 
response = requests.get(countryPage)
    
# Check if the response is successful (status code 200). If not, print the error message 
if response.status_code != 200:
    print(f"Failed to get the webpage: {response.status_code}")

# Parse the HTML content using BeautifulSoup           
soup = BeautifulSoup(response.text, 'html.parser')

 
# Create a function that extracts the item, price, and price range from a specific cost of living category
def extract_category_data(category_name):
    #Initialize an empty string for each category 
    category_data = [] 
 
    # Find the header for the specified category
    category_header = soup.find('th', class_='highlighted_th prices')
    
    if category_header:
        # Find all rows with the tag 'tr' within this category 
        rows = category_header.find_all_next('tr')
        
        # Loop through each row (tr tag) found in the current category 
        for row in rows:
            # Check if the row contains a <td> element (to skip header rows)
            columns = row.find_all('td')
            
            # Ensure there are at least 3 columns (item, price, price range)
            if len(columns) >= 3:  
                # Extract the item name from the first column 
                item = columns[0].text.strip()
                
                # Extract the price from the second column's span element with the specific class name 
                price_span = columns[1].find('span', class_='first_currency')
                
                 # If price_span exists, store that in the price variable. If not, 'N/A' wil be stored instead to handle missing price 
                if price_span:
                    price = price_span.text.strip()
                else:
                    price = 'N/A'  

                # Perform similar analysis and storing for the min and max prices 
                min_price_span = columns[2].find('span', class_='barTextLeft')
                
                if min_price_span: 
                    min_price = min_price_span.text.strip()
                else: 
                    min_price = 'N/A'
                
                max_price_span = columns[2].find('span', class_='barTextRight')
                
                if max_price_span: 
                    max_price = max_price_span.text.strip()
                else: 
                    max_price = 'N/A'
                
                # Append the extracted data to the list
                category_data.append({
                    'Category': category_name,
                    'Item': item,
                    'Price': price,
                    'Min Price': min_price,
                    'Max Price': max_price
                })
    # return the finalized list for the specific category 
    return category_data

# Extract data for all cost of living categories
restaurant_data = extract_category_data('Restaurants')
market_data = extract_category_data('Markets')
transportation_data=extract_category_data('Transportation')
utilities_data=extract_category_data(' Utilities (Monthly)')
sports_data=extract_category_data('Sports And Leisure')
childcare_data= extract_category_data('Childcare')
clothing_data= extract_category_data('Clothing And Shoes')
rent_data= extract_category_data('Rent Per Month')
apartment_data=extract_category_data('Buy Apartment Price')
salaries_data=extract_category_data('Salaries And Financing')

# Combine the extracted data into a single list
cost_of_living_data = restaurant_data + market_data + transportation_data + utilities_data + sports_data + childcare_data + clothing_data + rent_data + apartment_data + salaries_data 

'''
Now, We will use the Booking com API from rapidapi.com to gather information about the hotels (name and price) of the inputted city and hotel search preferences. 
(link to the api documentation: https://rapidapi.com/tipsters/api/booking-com)

'''

# Create a function that returns the associated id for the city that later will be used to fetch hotel informations 
def get_location_id(city): 
    
    # Extract the URL for the city 
    id_URL = "https://booking-com.p.rapidapi.com/v1/hotels/locations"

    # Set query parameters with user-inputted city (provided in the API documentation)
    querystring = {f"locale":"en-us","name":{city}}

    # Set required API headers for authentication (Note: Please insert the API key provided in lytespace and be mindful of the amount of requests sending to the API (hard limit of 500 requests per month)) 
    headers = {
	    "x-rapidapi-key": "INSERT_API_KEY",
	    "x-rapidapi-host": "booking-com.p.rapidapi.com"
    }
    
    # Send a GET request to the URL
    response = requests.get(id_URL, headers=headers, params=querystring)

    # If the response is successful, extract the location ID and stored as a string variable. If not, error message will be printed and None will be stored for error handling. 
    if response.status_code == 200: 
        data = response.json()
        if data and 'dest_id' in data[0]:
            id = str(data[0]['dest_id'])
        else:
            print(f"No destination ID found for the city: {response.status_code}")
            id = None 
    else: 
        print(f"Error in fetching city location: {response.status_code}")
        id = None

    return id 

location_id = get_location_id(city)

# Create another function that gathers hotel names and prices based on the location ID that we extracted from the get_location_id function 
def get_hotel_price(location_id):
    
    # Extract the URL for the hotel search 
    hotel_url = "https://booking-com.p.rapidapi.com/v2/hotels/search"
    
    # Parameters for the hotel search, including the fetched location_id as well as user inputs for check-in/out dates, currency, number of adults, and room number. 
    querystring = {
    "dest_id": location_id,
    "order_by": order_by,
    "checkout_date": checkout_date,
    "filter_by_currency": currency,
    "locale": "en-us",
    "dest_type": "city",
    "checkin_date": checkin_date,
    "adults_number": adults_number,
    "room_number": room_number,
    "units": "metric"
}
    # Set required API headers for authentication (Note: Please insert the API key provided in lytespace and be mindful of the amount of requests sending to the API (hard limit of 500 requests per month)) 
    headers = {
	    "x-rapidapi-key": "INSERT_API_KEY",
	    "x-rapidapi-host": "booking-com.p.rapidapi.com"
    }
    # Send a GET request to the URL
    response = requests.get(hotel_url, headers=headers, params=querystring)

    # Initialize an empty dictionary to store hotel names as keys and their corresponding prices as values
    hotels_info = {}
    
    # If the request is successful, extract hotel names and prices. If not, print out the error message 
    if response.status_code == 200: 
        hotel_data = response.json()
        
        if 'results' in hotel_data and hotel_data['results']:
            # Loop through each hotel in the results
            for hotel in hotel_data['results']:
                # Extract hotel name and handle missing names
                hotel_name = hotel.get('name')
                if not hotel_name:
                    print("Warning: No hotel name found for one of the results. Skipping.")
                    continue  
        
                # Extract the gross price per night
                price_info = hotel.get('priceBreakdown', {}).get('grossPrice', {})
                price = price_info.get('value')
                if not price:
                    print(f"Warning: No price found for hotel '{hotel_name}'. Setting price to 'N/A'.")
                    price = "N/A"  # Assign default value if no price is found
        
                # Store the information in the dictionary
                hotels_info[hotel_name] = price
        else:
            print("No hotels found in the search results. (There might not be any avaliability for this period. Try entering a different date)")
    else:
        print(f"Error fetching hotel data: {response.status_code}")
        
     # return the finalized dictionary
    return hotels_info

# Initialize a list to store hotel data
hotel_data= [] 

# If a valid location ID was found, search for hotel prices by calling the get_hotel_price function. If not, print out the error message 
if location_id:
    hotel_prices = get_hotel_price(location_id)
    if hotel_prices:
        # If hotel prices were found, append the category, hotel name (item), and formatted price to the hotel_data list. If not, print out the error message 
        for hotel, price in hotel_prices.items():
            hotel_data.append({
                'Category': 'Hotels', 
                'Item': hotel,
                # Format price to 2 decimal places
                'Price': f"${price:.2f}",  
    })
    else:
        print("No hotels found (There might not be any avaliability for this period. Try entering a different date)")
else:
    print("Cannot search for hotels without a valid location ID.")
    
    
# Combine the hotel data with the cost of living data into a single list 
combined_data = cost_of_living_data + hotel_data  
# Convert the data into a pandas DataFrame
combined_df = pd.DataFrame(combined_data)

# set the order for the DataFrame 
cols = ['Category', 'Item', 'Price', 'Min Price', 'Max Price'] + [col for col in combined_df.columns if col not in ['Category', 'Item', 'Price', 'Min Price', 'Max Price']]
combined_df = combined_df[cols]
 

# Clean CSV file: make the column names lowercase and replace spaces with underscores
combined_df.columns = combined_df.columns.str.lower().str.replace(' ', '_')

# Clean CSV file: unknown is filled for parts with no data 
combined_df = combined_df.apply(lambda col: col.fillna(0) if col.dtype in ['int64', 'float64'] else col.fillna('Unknown'))

# Export the final DataFrame to a CSV file, named after the inputted city name 
combined_df.to_csv(f'{city}_combined_data.csv', index=False)
