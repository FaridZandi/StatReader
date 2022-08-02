# StatReader

Provides easy access to my favorite numbers. The project is currently deployed with [Heruko](https://statreader.herokuapp.com/dashboard/).

For each stat, a url and a CSS query selector is required. A separete crawler, reads the URLs and the selectors at 1-hour intervals. The results are pushed back to the database on the webserver. 

Due to exteremely limited space on the database, the results are summarised in hourly (for the last 24 hours) and daily (for the last 30 days) digests. 
