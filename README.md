# Covid Alberta
> This is a small package that I have developed to look at some of the alberta specific covid data.


This file will become your README and also the index of your documentation.

## Install

`pip install covid_alberta`

## Web Scraper

The `albertaC19` is a class that scrapes the updated stats off of the [alberta Covid-19 website](https://covid19stats.alberta.ca/).

example of using the webscraper


```
abC19scaper = albertaC19()
```

```
abTotal, abRegion, abTesting = abC19scaper.scrape_all(return_dataframes=True)
abTotal.tail()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>cum_cases</th>
      <th>Confirmed_count</th>
      <th>Probable_count</th>
      <th>Daily_count</th>
      <th>Active_cum</th>
      <th>Died_cum</th>
      <th>Recovered_cum</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2020-04-03</th>
      <td>1200</td>
      <td>38</td>
      <td>36</td>
      <td>74</td>
      <td>650</td>
      <td>19</td>
      <td>267</td>
    </tr>
    <tr>
      <th>2020-04-04</th>
      <td>1258</td>
      <td>38</td>
      <td>20</td>
      <td>58</td>
      <td>704</td>
      <td>24</td>
      <td>319</td>
    </tr>
    <tr>
      <th>2020-04-05</th>
      <td>1316</td>
      <td>35</td>
      <td>23</td>
      <td>58</td>
      <td>762</td>
      <td>24</td>
      <td>380</td>
    </tr>
    <tr>
      <th>2020-04-06</th>
      <td>1351</td>
      <td>20</td>
      <td>15</td>
      <td>35</td>
      <td>797</td>
      <td>26</td>
      <td>447</td>
    </tr>
    <tr>
      <th>2020-04-07</th>
      <td>1373</td>
      <td>9</td>
      <td>13</td>
      <td>22</td>
      <td>900</td>
      <td>26</td>
      <td>447</td>
    </tr>
  </tbody>
</table>
</div>



## Data analysis

Currently I am developing the stats and plotting packages in the CovidAlberta.ipynb
I will convert it over into a more formal package with functions as I finish it up. Some of the stats I am looking at are the cumulative case increase across Alberta as well as calculating the doubling rate of the case counts. 

example for calculating the stats

```
totals_dt = calculate_doublingtimes(abTotal, col_suffix="cum_cases", combine_df=False)
totals_dt.tail()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>dtime</th>
      <th>dtime_rw</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2020-04-03</th>
      <td>2.737364</td>
      <td>7.191175</td>
    </tr>
    <tr>
      <th>2020-04-04</th>
      <td>2.816377</td>
      <td>7.129371</td>
    </tr>
    <tr>
      <th>2020-04-05</th>
      <td>2.895210</td>
      <td>7.378968</td>
    </tr>
    <tr>
      <th>2020-04-06</th>
      <td>2.980823</td>
      <td>9.701638</td>
    </tr>
    <tr>
      <th>2020-04-07</th>
      <td>3.070099</td>
      <td>12.835158</td>
    </tr>
  </tbody>
</table>
</div>



I have seen a lot of graphs showing the cumulative curve with as well as the "2, 3, and 4 day doubling rate" curves. Which made me think, why not just calculate that rate? If you calculate the actual doubling rate you can start looking at some interesting things such as how our doubling rate is changing compared to the cumulative case count? Here's an example of that image.

![doubling rate by case count](https://github.com/tyleracorn/covid_alberta/raw/master/images/AlbertaDTimeIncrease_byCaseCount.png "Doubling Rate by Case Count")
