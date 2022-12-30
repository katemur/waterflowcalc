# WaterFlowCalc
#### Video Demo:  <https://www.youtube.com/watch?v=1y66ROAN5B4>
#### Description:
**Required libraries:** cs50, numpy, pandas, pdfkit, os, sys
my goal was to create a **command-line program** that calculates water flow for different consumers and returns the results as a pdf table
There could be many different water consumers in 1 building, so, the program repeatedly asks to input the info about a consumer until stopped by **EOFError**. The user should input 4-5 arguments such as:
- Item _(tells the program a type of consumer)_
- Ntot _(total number of devices that need any kind of water used by a consumer)_
- Nhot _(total number of devices that need hot water used by a consumer)_
- U _(number of people)_ 
- Shifts _(how many shifts a day, normally 1, if not inputted)_

Here is a list of items we could use for this program:
 - 1.1 apart without bath
 - 1.2 apart with water heater
 - 1.3 apart with gas water heater
 - 1.4 apart with centalised hot water no bath
 - 1.5 apart with small bath
 - 1.6 apart with bath over 1500 mm
 - 2.1 dorm with shared shower
 - 2.2 dorm with showers in every room
 - 2.3 dorm with shared kitchen and shower for every block
 - 3.1 hotel with shared bathroom
 - 3.2 hotel with bathroom in every room
 - 3.3 hotel with bathroom in 25% of rooms
 - 3.4 hotel with bathroom in 75% of rooms
 - 3.5 hotel with bathroom in up to 100% of rooms
 - 4.1 hospital with shared bathrooms
 - 4.2 hospital with bathrooms near wards
 - 4.3 infective hospital
 - 5.1 health resort with shared showers
 - 5.2 health resort with shower in every room
 - 5.3 health resort with bath in every room
 - 6 day hospital
 - 7.1 day nursery with canteen with premade food
 - 7.2 day nursery with canteen and laundry
 - 7.3 24-hour nursery with canteen with premade food
 - 7.4 24-hour nursery with canteen and laundry
 - 8.1 mechanized laundry
 - 8.2 non-mechanical laundry;
 - 9 administration building
 - 10 university or college with showers and cafe
 - 11 university lab
 - 12.1 university or college with gym showers and canteen with premade food
 - 12.2 the same as 12.1 but with longer day
 - 13.1 boarding school
 - 13.2 boarding school with bedrooms
 - 14.1 pharmacy
 - 14.2 pharmacy with a lab
 - 15.1 canteen with a dinnin area
 - 15.2 canteen without dinin area
 - 16.1 grocery store
 - 16.2 department store
 - 17 hairdressing saloon
 - 18 cinema
 - 19 club
 - 20.1 theatre. audience
 - 20.2 theatre. artist
 - 21.1 Stadium and gym. audience
 - 21.2 stadium and gym. exercisers
 - 21.3 stadium and gym. sportsmen
 - 22.1 recharching the swimming pool
 - 22.2 swimming pool. audience
 - 22.3 swmming pool. sportsmen
 - 23.1 Sauna with wash-basins and showers
 - 23.2 sauna with wellness tecniques and showers
 - 23.3 sauna with showers
 - 23.4 sauna with baths
 - 24 industrial plants with showers
 - 25.1 production facility with heat radiation above 84 kJ
 - 25.2 other production facilities
 - 26.1 watering the grass
 - 26.2 watering the football field
 - 26.3 watering pavements
 - 26.4 watering the lawn
 - 27 fillng the ice rink

##### tables.db
I used an sqlite database to store source tables. For this purposes, I imported csv tables into the database.
Program refers to it while making calculations to get needed values.

##### Consumer 
When the object of this class is initialized it gets all the needed info from the tables.db and automatically calculates all the waterflows for 1 consumer.
For initialization it needs item, Ntot, Nhot, U, Shifts - exactly what the proram is asking the user to input.

##### interpolation function
For my calculations inside of Consumer class, I needed to interpolate values from a database according to the one calculated. 
The SQL statement used to get 2 closest values from SQL database:
`SELECT np, alpha FROM b2 ORDER BY ABS(? - np) LIMIT 2;` 
after that it just uses the interpolation formula and gives back the result.

##### custom_split function
Expects a string as an input. Splits input into separate variables and returns it as a dict. I created it to check for the correct number of arguments (if the split is unsuccesful - number of arguments is not right) and pass input to the Consumer class.

##### table_pdf function
expects a pandas Dataframe and tot/cold/hot string as an input. First, it exports the dataframe as a html table and them, using pdfkit, turns the html file into a pdf file.

##### df_tot, df_hot, df_cold
I used dataframes to collect output data because it is much easier to display big tables with pandas and it's easily can be exported to any format and styled differently. 


