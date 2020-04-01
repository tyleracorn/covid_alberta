# covid_alberta
This is a small package that I have developed to look at some of the alberta specific covid data.

There are two parts to the package. the webscraper and the data analysis

## Web Scraper

The `albertaC19_websraper` is a class that scrapes the updated stats off of the [alberta Covid-19 website](https://covid19stats.alberta.ca/).

example of using the webscraper
'''python
abC19scaper = albertaC19_webscraper()
abTotal, abRegion, abTesting = abC19scaper.scrape_all(return_dataframes=True)
'''

## data analysis

Currently I am developing the stats and plotting packages in the CovidAlberta.ipynb
I will convert it over into a more formal package with functions as I finish it up. Some of the stats I am looking at are the cumulative case increase across Alberta as well as calculating the doubling rate of the case counts. 

example for calculating the stats
'''python
region_cum = calculate_cumulatives(abRegion, combine_df=False)
region_dt = calculate_doublingtimes_region(region_cum, combine_df=False)
total_dt = calculate_doublingtimes_region(abTotal, col_suffix='cum_cases', combine_df=False)
'''

I have seen a lot of graphs showing the cumulative curve with as well as the "2, 3, and 4 day doubling rate" curves. Which made me think, why not just calculate that rate? If you calculate the actual doubling rate you can start looking at some interesting things such as how our doubling rate is changing compared to the cumulative case count? Here's an example of that image.

![doubling rate by case count](https://github.com/tyleracorn/covid_alberta/raw/master/images/AlbertaDTimeIncrease_byCaseCount.png "Doubling Rate by Case Count")
