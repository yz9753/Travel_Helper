# PPDS - Activity 02 - Vacation Helper (ETL with Pandas + Data Cleaning)

## Description 

This project combines cost of living data scraped from the website Numbeo.com and hotel data from the booking com API to create a unique and valuable dataset for individuals planning trips. The data pipeline provide insights into the affordability of different travel destinations. The goal is to help users make informed decisions by offering a detailed breakdown of costs in their chosen location.


## Key Features

- Asks user to input their destination city and associated information regarding their travel (currency, check-in/check-out dates, how they want to sort the hotel information by, amount of traveller, number of rooms)
- Scrapes Numbero.com to retrieve data on the cost of living for the inputted city and preferred currency. Then returns the data grouped by categories (restaurant, groceries, transportation, dining, etc) 
- converts the inputted city name into its associated location ID using the booking com API 
- searches for related hotels via the location ID and other inputted hotel preferences and then returns all hotel names and prices 
- combines, cleans and structures the collected data into a comprehensive, readable dataset for users

## Chosen Data Sources 

1. **Website:** Numbeo.com is selected as it provides accurate and up-to-date data regarding cost of living and its suitability for web scraping practices 
2. **API** The booking com API is used due to its accessibility(one of the few free API that offers an wide range of data regarding hotel prices), user-friendly interface, and its ability to gathering real-time hotel prices. 

## How to Run  

To run this scraper, you need to:

1. Clone the repository by typing git clone, and then paste the URL for the repository from GitHub in Terminal(more detailed instructions can be found here https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository#cloning-a-repository). 
3. Install the dependencies from the requirements.txt file by typing pip install -r requirements.txt in the VSCode Terminal. 
4. Click to Run the python script main.py. 
4. When prompted, enter the name of the city, preferred currency abbreviation, check-in/check-out dates, the type to order the hotel data by, number of travellers and rooms. 
