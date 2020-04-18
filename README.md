# Covid Alberta
> This is a small package that I have developed to look at some of the alberta specific covid data.


This file will become your README and also the index of your documentation.

## Install

`pip install covid_alberta`

## Web Scraper

The `albertaC19` is a class that scrapes the updated stats off of the [alberta Covid-19 website](https://covid19stats.alberta.ca/).

example of using the webscraper


```
abC19scaper = covid_alberta.albertaC19(outputfolder="")
# I don't plan on writing out the data in this example thus the keywords
ab_totals, ab_regions, ab_testing = abC19scaper.scrape_all(fltypes=None, return_dataframes=True)
```


    ---------------------------------------------------------------------------

    IndexError                                Traceback (most recent call last)

    <ipython-input-3-cea1377c44fe> in <module>
          1 abC19scaper = covid_alberta.albertaC19(outputfolder="")
          2 # I don't plan on writing out the data in this example thus the keywords
    ----> 3 ab_totals, ab_regions, ab_testing = abC19scaper.scrape_all(fltypes=None, return_dataframes=True)
    

    c:\Repositories_C\covid_alberta\covid_alberta\webscraper.py in scrape_all(self, totalfl, regionsfl, testfl, fltypes, combine_dataframes, return_dataframes)
        335 
        336         '''
    --> 337         totals = self.scrape_albertaTotals(output_filename=totalfl, fltypes=fltypes, return_dataframe=return_dataframes)
        338         regions = self.scrape_albertaRegions(output_filename=regionsfl, fltypes=fltypes, return_dataframe=return_dataframes)
        339         testing = self.scrape_albertaTesting(output_filename=testfl, fltypes=fltypes, return_dataframe=return_dataframes)
    

    c:\Repositories_C\covid_alberta\covid_alberta\webscraper.py in scrape_albertaTotals(self, output_filename, fltypes, update_figure_order, return_dataframe)
        177         # Scrape the data
        178         ab_cumulative = json.loads(totals_results[fig_order['cum_cases']].string)
    --> 179         ab_daily_cases = json.loads(totals_results[fig_order['daily_cases']].string)
        180         ab_case_status = json.loads(totals_results[fig_order['case_status']].string)
        181 
    

    IndexError: list index out of range


Now we can show the dataframes

```
ab_totals.tail()
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
      <th>2020-04-04</th>
      <td>1250</td>
      <td>38</td>
      <td>19</td>
      <td>57</td>
      <td>618</td>
      <td>23</td>
      <td>322</td>
    </tr>
    <tr>
      <th>2020-04-05</th>
      <td>1308</td>
      <td>35</td>
      <td>23</td>
      <td>58</td>
      <td>676</td>
      <td>24</td>
      <td>382</td>
    </tr>
    <tr>
      <th>2020-04-06</th>
      <td>1344</td>
      <td>20</td>
      <td>16</td>
      <td>36</td>
      <td>712</td>
      <td>27</td>
      <td>449</td>
    </tr>
    <tr>
      <th>2020-04-07</th>
      <td>1409</td>
      <td>39</td>
      <td>26</td>
      <td>65</td>
      <td>776</td>
      <td>27</td>
      <td>518</td>
    </tr>
    <tr>
      <th>2020-04-08</th>
      <td>1423</td>
      <td>9</td>
      <td>5</td>
      <td>14</td>
      <td>876</td>
      <td>29</td>
      <td>518</td>
    </tr>
  </tbody>
</table>
</div>



```
ab_regions.tail()
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
      <th>Calgary_cumulative</th>
      <th>Central_cumulative</th>
      <th>Edmont_cumulative</th>
      <th>North_cumulative</th>
      <th>South_cumulative</th>
      <th>Unknown_cumulative</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2020-04-04</th>
      <td>778</td>
      <td>61</td>
      <td>315</td>
      <td>75</td>
      <td>19</td>
      <td>2</td>
    </tr>
    <tr>
      <th>2020-04-05</th>
      <td>801</td>
      <td>65</td>
      <td>340</td>
      <td>79</td>
      <td>21</td>
      <td>2</td>
    </tr>
    <tr>
      <th>2020-04-06</th>
      <td>821</td>
      <td>65</td>
      <td>348</td>
      <td>86</td>
      <td>22</td>
      <td>2</td>
    </tr>
    <tr>
      <th>2020-04-07</th>
      <td>854</td>
      <td>72</td>
      <td>364</td>
      <td>94</td>
      <td>23</td>
      <td>2</td>
    </tr>
    <tr>
      <th>2020-04-08</th>
      <td>860</td>
      <td>72</td>
      <td>368</td>
      <td>95</td>
      <td>26</td>
      <td>2</td>
    </tr>
  </tbody>
</table>
</div>



```
ab_testing.tail()
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
      <th>test_count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2020-04-04</th>
      <td>1737</td>
    </tr>
    <tr>
      <th>2020-04-05</th>
      <td>1112</td>
    </tr>
    <tr>
      <th>2020-04-06</th>
      <td>1129</td>
    </tr>
    <tr>
      <th>2020-04-07</th>
      <td>1319</td>
    </tr>
    <tr>
      <th>2020-04-08</th>
      <td>459</td>
    </tr>
  </tbody>
</table>
</div>



These are all pandas DataFrames. For more info on using pandas check out the pandas [cookbook](https://pandas.pydata.org/pandas-docs/stable/user_guide/cookbook.html).

## analysis

> these are functions that I have started working on for some quick analyses of the data. The main one being doubling rates

### Doubling times

the `calculate_doublingtimes` function returns 2 columns.

> `dtime` is how many days our count has been doubling from the first reported case to get to todays case count

> `dtime_rw` is a rolling window calcualtion. So if you window is 6 days it looks at what our doubling rate, starting from the case count 6 days ago, would have to be to get to todays case count.

I started off looking at the rolling window calculation. However the more I look into it the more I'm not happy with using the rolling window. Our information about Covid-19 cases are changing so rapidly, that the rolling window calculation tends to be too noisy and too optimistic to be useful. We can calculate both below and see what they look like

```
totals_dt = covid_alberta.calculate_doublingtimes(ab_totals, col_suffix="cum_cases", combine_df=False)
regions_dt = covid_alberta.calculate_doublingtimes(ab_regions, col_suffix="cumulative", combine_df=False)
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
      <th>2020-04-04</th>
      <td>2.818897</td>
      <td>7.119992</td>
    </tr>
    <tr>
      <th>2020-04-05</th>
      <td>2.897670</td>
      <td>7.353586</td>
    </tr>
    <tr>
      <th>2020-04-06</th>
      <td>2.982973</td>
      <td>9.613334</td>
    </tr>
    <tr>
      <th>2020-04-07</th>
      <td>3.059140</td>
      <td>11.617191</td>
    </tr>
    <tr>
      <th>2020-04-08</th>
      <td>3.150442</td>
      <td>17.176893</td>
    </tr>
  </tbody>
</table>
</div>



```
regions_dt.tail()
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
      <th>Calgary_dtime</th>
      <th>Calgary_dtime_rw</th>
      <th>Central_dtime</th>
      <th>Central_dtime_rw</th>
      <th>Edmont_dtime</th>
      <th>Edmont_dtime_rw</th>
      <th>North_dtime</th>
      <th>North_dtime_rw</th>
      <th>South_dtime</th>
      <th>South_dtime_rw</th>
      <th>Unknown_dtime</th>
      <th>Unknown_dtime_rw</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2020-04-04</th>
      <td>3.019693</td>
      <td>7.296903</td>
      <td>4.046714</td>
      <td>14.735665</td>
      <td>3.872364</td>
      <td>5.864623</td>
      <td>3.692514</td>
      <td>8.141493</td>
      <td>4.472769</td>
      <td>7.609425</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2020-04-05</th>
      <td>3.110208</td>
      <td>7.587349</td>
      <td>4.151191</td>
      <td>12.826571</td>
      <td>3.956375</td>
      <td>6.261873</td>
      <td>3.807239</td>
      <td>8.008629</td>
      <td>4.553405</td>
      <td>6.431655</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2020-04-06</th>
      <td>3.202070</td>
      <td>9.970858</td>
      <td>4.317239</td>
      <td>18.637702</td>
      <td>4.082834</td>
      <td>8.636192</td>
      <td>3.890285</td>
      <td>7.959255</td>
      <td>4.709120</td>
      <td>6.000000</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2020-04-07</th>
      <td>3.286065</td>
      <td>12.181763</td>
      <td>4.376066</td>
      <td>15.441420</td>
      <td>4.189037</td>
      <td>11.309771</td>
      <td>3.966687</td>
      <td>8.029614</td>
      <td>4.863424</td>
      <td>7.289318</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2020-04-08</th>
      <td>3.385243</td>
      <td>19.656061</td>
      <td>4.538143</td>
      <td>20.885405</td>
      <td>4.323639</td>
      <td>15.835158</td>
      <td>4.109679</td>
      <td>9.387934</td>
      <td>4.893159</td>
      <td>8.566048</td>
      <td>0</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>



## Plots

Here is some of the plots I've used for looking at the data. For this example I'm using matplotlib. Plotly creates nice plots but is a little harder to include in this documentation since it's hosted on github pages. If you head over to [my website](www.tyleracorn.com) I'll post the plotly code and example of the interactive plots there.

```
import matplotlib.pyplot as plt

# Set defaults and settings
days_to_trim = 1
date_fmt = "%B %d"

# Grab the data we want for the plots and trim the last day off
plt_totals = ab_totals[:-days_to_trim]
plt_total_dt = totals_dt[:-days_to_trim]
plt_regions = ab_regions[:-days_to_trim]
plt_regions_dt = regions_dt[:-days_to_trim]

# use a format dictionary so I only have to set them in one location

fmt = {'alb': {'x_data': plt_totals['cum_cases'],
               'y_data': plt_total_dt['dtime'],
               'last_date': plt_totals.index.strftime(date_fmt)[-1],
               'annot_x': plt_totals['cum_cases'][-1],
               'annot_y': plt_total_dt['dtime'][-1],
               'color': 'green',
               'label': 'Alberta'},
       'cal': {'x_data': plt_regions['Calgary_cumulative'],
               'y_data': plt_regions_dt['Calgary_dtime'],
               'last_date': plt_regions.index.strftime(date_fmt)[-1],
               'annot_x': plt_regions['Calgary_cumulative'][-1],
               'annot_y': plt_regions_dt['Calgary_dtime'][-1],
               'color': 'orange',
               'label': 'Calgary'},
       'edm': {'x_data': plt_regions['Edmont_cumulative'],
               'y_data': plt_regions_dt['Edmont_dtime'],
               'last_date': plt_regions.index.strftime(date_fmt)[-1],
               'annot_x': plt_regions['Edmont_cumulative'][-1],
               'annot_y': plt_regions_dt['Edmont_dtime'][-1],
               'color': 'blue', 
               'label': 'Edmonton'},
      }

# Setup the plot
fig, ax = plt.subplots(figsize=(8,6))

# Create the scatter plots using a loop and the dictionary above
for rgn in ['alb', 'cal', 'edm']:
    ax.plot(fmt[rgn]['x_data'], fmt[rgn]['y_data'], 
            c=fmt[rgn]['color'], label=fmt[rgn]['label'])

# add an annotation to the last point
for rgn in ['alb', 'cal', 'edm']:
    ax.plot(fmt[rgn]['annot_x'], fmt[rgn]['annot_y'], 'o', c=fmt[rgn]['color'])
    ax.text(fmt[rgn]['annot_x'] - 60, fmt[rgn]['annot_y'] + 0.08, fmt[rgn]['last_date'], 
            fontdict={'color': fmt[rgn]['color'], 'size': 8, 'weight': 'bold'})
# fancy up the plot
ax.grid(which='both', linestyle=(0, (5, 3)), lw=0.5)
ax.legend(frameon=True, fancybox=True, shadow=True)
ax.set_ylabel('Doubling Time (Days)', fontdict={'size': 9, 'family': 'sans-serif', 'style':'italic'})
ax.set_xlabel('Cumulative Case Count', fontdict={'size': 9, 'family': 'sans-serif', 'style':'italic'})
title = ax.set_title("Alberta: Doubling Time by Cumulative Cases",
                     fontdict={'fontsize': 10, 'family': 'sans-serif', 'fontweight': 'bold'})
```


![png](docs/images/output_14_0.png)

