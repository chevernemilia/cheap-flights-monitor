# cheap-flights-monitor

This is owner's first real project in github, primarily utilizing the data crawling capability to find the cheapest (round-trip) flight tickets to a pre-selected desired destination(s).

PURPOSE:
The purpose of this project is to help the user to find and monitor the cheapest flight tickets periodically for the next vacation spots ahead of time, and allow user to immediately take action to purchase cheap flight tickets, and help ease part of the future vacation planning and preparation.

HIGH LEVELL DESIGN:
The project should be slowly developed into different phases:

1. find and filter cheapest flight tickets to one or two destination across a larger range of time frame (eg: round trip going from United States to UK and/or France in 05/01-05/31) - This is useful for a use case when someone have desired/target places to go but can be flexible about the vacation time)

2. find and filter cheapest flight tickets to multiple destination in a particular shorter range of days (eg. round trip going from United States to countries A,B,C,X,Y,Z... in first week of Oct.) -- This is useful for a use case when someone knows ahead of time of the exact vacation time frame but is flexible about the target destination as long as it is "cheap".

3. find and filter cheapest flight tickets based on the capabilities of 1) and 2) combination above. (TBD)

DETAIL DESIGN:
1. multiple flight records from the website would be searched and save into dataframe, each records would conains information as airport, date, time, number of stops, intermediate airport(s) of those stops, flight amount, flight hours, airline.
2. information would be cleaned, filtered, merged and organized into final information
3. number of plots/charts and the dataframe for flight prices would be save into a .pdf, .xlsx and .txt files,
    3.1 .pdf stores a number of plots that show flight prices, hours, date and time, possible trip duration days distribution
    3.2 .xlsx stores the list of flight records sorted by ascending flight prices
    3.3 .txt is a info file keep track of date and time of the flight quiry, quiry records, etc.
4. The three files in 3) will be sent to user for periodic monitoring (eg. script run and send result every 3 hours)



PROJECT SOURCES INFO:
website for major data crawl: kayak
python module for data crawl: selenium
web browser: Google Chrome
website driver: chromedriver (version update almost every month, or twice per quarter according to source online)
python version: 3.7

POSSIBLE TECHNICAL ISSUES:
- if the google chrome is updated to a newer version (mostly done automatically), a chrome driver which version that's consistent with the version of google chrome need to be installed to a path where the system path can point to.
- setting the path of chrome driver as system env variable can be done in the /.bashrc or /.bash_profile
- the website (kayak) where this project collects data from, would periodically update their html/xml elements, such as the key tag, attributes, values that's needed for flight records query of the web browser's flight list page. In that case, the script might throw error because the keys are not there anymore and thus the script need to be developed continuously to accommodate for those changes. 
