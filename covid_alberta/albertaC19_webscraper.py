'''module for scraping the updated covid-19 data from the alberta website'''
import json
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import pandas as pd


class albertaC19_webscraper():
    def __init__(self, covid_url:str='https://covid19stats.alberta.ca/', outputfolder:str='data',
                 html_update_ids:dict=None, totals_update_fig_order:dict=None):
        '''
        using requests and BeautfulSoup4 scrape updated covid data from the ablerta website
        save the outputs into a outputfolder

        Parameters:
            covid_url:str
                the url for the alberta covid website
            outputfolder:str
                the folder to save the scraped data to. Will create the folder if it can't find it
            html_update_ids:dict
                if the alberta covid html changes the html id where the specified data is stored you
                can update to the new id here. This is used in the scrapers. current keys are
                `totals`, `regions`, `testing`
        '''
        self.covid_url = covid_url
        self.outputfolder = Path(outputfolder)
        if not self.outputfolder.is_dir(): self.outputfolder.mkdir()

        self.page = requests.get(self.covid_url)
        self.soup = BeautifulSoup(self.page.content, 'html.parser')
        self.html_ids = {'totals':'cases', 'regions':'geospatial', 'testing': 'laboratory-testing'}
        if html_update_ids:
            self.html_ids.update(html_update_ids)
        self.totals_figure_order = {'cum_cases':0, 'daily_cases':3, 'case_status':1}
        if totals_update_fig_order:
            self.totals_figure_order.update(totals_update_fig_order)

    def print_html_class_ids(self, html_class_attr:str='level2', print_self:bool=True):
        '''
        websites change so use this if you need to figure out what to use to update the `html_update_class_ids`
        dictionary. Right now the covid alberta site is using `level 2` as one of the id attributes for
        the tabs containing the covid data. The scrapers in this are searching for the `id` string.

        this function will find all `div` `class` sections in the soup with

        Parameters:
            html_class_attr:str
                will search through the soup find all class names that include this attribute string
            print_self:bool
                will also print the current python class parameters `html_class_ids` which are used
                by the scraper functions to find the data

        '''
        find_results = False
        for tag in self.soup.find_all('div', {'class': html_class_attr}):
            if tag.attrs: find_results = True
            print(tag.attrs)
        if not find_results:
            print(f'unable to find tag: {html_class_attr}')
        if print_self:
            print("Here are the class id's we are currently using for this scraper:")
            print(self.html_ids)
        return find_results

    def update_html_ids(self, html_update_ids:dict=None):
        '''
        update the ids used to search for the data in the alberta covid html
        current keys are `totals`, `regions`, `testing`
        '''
        if html_update_ids:
            self.html_ids.update(html_update_ids)

    def _clean_cumulative_data(self, ab_cumulative_dict:dict):
        '''
        utility function used to clean up the cumulative data
        '''
        dates = ab_cumulative_dict['x']['data'][0]['x']
        cum_cases = ab_cumulative_dict['x']['data'][0]['y']
        # Convert to DataFrame
        df_ab_cumulative = pd.DataFrame(data=cum_cases,
                                        index=dates,
                                        columns=['cum_cases'])
        # Clean up formatting of df
        df_ab_cumulative.index = pd.to_datetime(df_ab_cumulative.index)

        return df_ab_cumulative

    def _clean_daily_case_data(self, ab_daily_cases:dict):
        '''
        utility function used to clean up the daily case data
        '''
        daily_data = dict()
        for data in ab_daily_cases['x']['data']:
            daily_data[data['name']] = {'date': data['x'], '{0}_count'.format(data['name']): data['y']}
        if len(daily_data) != 2:
            raise Warning("expecting only 2 daily case categories. Website likely changed. Check the results")
        df_confirmed = pd.DataFrame(data=daily_data['Confirmed']['Confirmed_count'],
                                    index=daily_data['Confirmed']['date'],
                                    columns=['Confirmed_count'])
        df_confirmed.index = pd.to_datetime(df_confirmed.index)
        df_probable = pd.DataFrame(data=daily_data['Probable']['Probable_count'],
                                   index=daily_data['Probable']['date'],
                                   columns=['Probable_count'])
        df_probable.index = pd.to_datetime(df_probable.index)

        df_daily_cases = df_confirmed.join(df_probable)
        df_daily_cases['Daily_count'] = df_daily_cases.sum(axis=1)

        return df_daily_cases

    def _clean_case_status_data(self, ab_case_status:dict):
        '''
        utility function used to clean up the case status data
        '''
        status_data = dict()
        for data in ab_case_status['x']['data']:
            status_data[data['name']] = {'date': data['x'], '{0}_cum'.format(data['name']): data['y']}
        if len(status_data) != 3:
            raise Warning("expecting only 3 status case categories. Website likely changed. Check the results")

        df_active = pd.DataFrame(data=status_data['Active']['Active_cum'],
                                 index=status_data['Active']['date'],
                                 columns=['Active_cum'])
        df_active.index = pd.to_datetime(df_active.index)
        df_died = pd.DataFrame(data=status_data['Died']['Died_cum'],
                               index=status_data['Died']['date'],
                               columns=['Died_cum'])
        df_died.index = pd.to_datetime(df_died.index)
        df_recovered = pd.DataFrame(data=status_data['Recovered']['Recovered_cum'],
                                    index=status_data['Recovered']['date'],
                                    columns=['Recovered_cum'])
        df_recovered.index = pd.to_datetime(df_recovered.index)

        df_case_status = df_active.join([df_died, df_recovered])

        return df_case_status

    def scrape_albertaTotals(self, output_filename:str='alberta_total_data', fltypes=('csv', 'json'),
                             update_figure_order=None, return_dataframe:bool=False):
        '''scrape the total case counts in alberta and save the data to the output folder

        Parameters:
            output_filename:str
                filename without the file ending
            fltypes:[list or str]
                will save out either csv, json or both filetypes. use `None` to not write anything
            update_figure_order:dict
                the order the figures are displayed on the website using python 0 index. This is important
                because the associated tags use a randomly generated id name so I am accessing them by order
                `self.totals_figure_order` will print out the default order expected
            return_dataframe:bool
                will return either the dataframes or a true/false on write success
        '''
        results = self.soup.find(id=self.html_ids['totals'])
        totals_results = results.find_all('script')
        fig_order = self.totals_figure_order.copy()
        if update_figure_order:
            fig_order.update(update_figure_order)

        # Scrape the data
        ab_cumulative = json.loads(totals_results[fig_order['cum_cases']].string)
        ab_daily_cases = json.loads(totals_results[fig_order['daily_cases']].string)
        ab_case_status = json.loads(totals_results[fig_order['case_status']].string)

        df_ab_cumulative = self._clean_cumulative_data(ab_cumulative)
        df_ab_daily_cases = self._clean_daily_case_data(ab_daily_cases)
        df_ab_case_status = self._clean_case_status_data(ab_case_status)

        df_ab_all = df_ab_cumulative.join([df_ab_daily_cases, df_ab_case_status])
        # clean up df formatting
        df_ab_all.fillna(0, inplace=True)
        df_ab_all = df_ab_all.astype(int)

        # Write out the data. If fltypes = None the function will return False
        write_success = self._write_dataframe(df_ab_all, output_filename, fltypes)
        if return_dataframe:
            return df_ab_all
        return write_success

    def scrape_albertaRegions(self, output_filename:str='alberta_region_data', fltypes=('csv', 'json'),
                              return_dataframe:bool=False):
        '''scrape the total case counts in alberta by region and save the data
        to the output folder

        Parameters:
            output_filename:str
                filename without the file ending
            fltypes:[list or str]
                will save out either csv, json or both filetypes
            return_dataframe:bool
                will return either the dataframes or a true/false on write success
        '''
        results = self.soup.find(id=self.html_ids['regions'])

        region_results = results.find_all('script')
        results_as_dict = json.loads(region_results[0].string)['x']

        zone_len = len(results_as_dict['data'])
        region_data_dict = dict()
        for idx in range (zone_len):
            zone_name = results_as_dict['data'][idx]['name']
            region_data_dict[zone_name] = {'date':results_as_dict['data'][idx]['x'],
                                           'cumulative':results_as_dict['data'][idx]['y']}

        list_ab_regions = list()
        for idx, key in enumerate(region_data_dict.keys()):
            if 'Zone' in key:
                zone = key.strip(' Zone')
            else:
                zone = key
            column = f'{zone}_cumulative'
            list_ab_regions.append(pd.DataFrame(data=region_data_dict[key]['cumulative'],
                                                index=region_data_dict[key]['date'],
                                                columns=[column]))

        df_ab_regions = list_ab_regions[0].join(list_ab_regions[1:])
        df_ab_regions.index = pd.to_datetime(df_ab_regions.index)
        df_ab_regions.fillna(0, inplace=True)
        df_ab_regions = df_ab_regions.astype(int)

        # Write out the data. If fltypes = None the function will return False
        write_success = self._write_dataframe(df_ab_regions, output_filename, fltypes)
        if return_dataframe:
            return df_ab_regions
        return write_success

    def scrape_albertaTesting(self, output_filename:str='alberta_testing_data', fltypes=('csv', 'json'),
                              return_dataframe:bool=False):
        '''scrape the testing counts by date in alberta and save the data
        to the output folder

        Parameters:
            output_filename:str
                filename without the file ending
            fltypes:[list or str]
                will save out either csv, json or both filetypes
            return_dataframe:bool
                will return either the dataframes or a true/false on write success
        '''
        results = self.soup.find(id=self.html_ids['testing'])
        testing_results = results.find_all('script')
        if len(testing_results) != 1:
            raise Warning("expecting only 1 test case categories. Website likely changed. Check the results")
        # Scrape the data
        tests_as_dict = json.loads(testing_results[0].string)['x']
        dates = tests_as_dict['data'][0]['x']
        test_count = tests_as_dict['data'][0]['y']
        # Convert to DataFrame
        df_ab_tests = pd.DataFrame(data=test_count,
                                        index=dates,
                                        columns=['test_count'])
        df_ab_tests.index = pd.to_datetime(df_ab_tests.index)
        df_ab_tests = df_ab_tests.astype(int)

        # Write out the data. If fltypes = None the function will return False
        write_success = self._write_dataframe(df_ab_tests, output_filename, fltypes)
        if return_dataframe:
            return df_ab_tests
        return write_success

    def _write_dataframe(self, dataframe:pd.DataFrame, output_filename:str, fltypes):
        ''''
        utility function to write the dataframe scraped. This way we can easily add different
        write functions to all the scraping functions.

        Parameters:
            dataframe:pd.DataFrame
                pd.DataFrame to write out
            output_filename:str
                filename without the file ending
            fltypes:[list or str]
                will save out either csv, json or both filetypes
        Returns:
            write_success:bool
                whether it wrote anything out or not. If `None` for fltypes is passed
                will return `False`

        '''
        write_success = False
        # Write out the data
        if fltypes:
            if 'json' in fltypes:
                flpath = self.outputfolder.joinpath(output_filename).with_suffix('.json')
                dataframe.to_json(flpath)
                write_success = True
            if 'csv' in fltypes:
                flpath = self.outputfolder.joinpath(output_filename).with_suffix('.csv')
                dataframe.to_csv(flpath)
                write_success = True
        return write_success

    def scrape_all(self, totalfl:str='alberta_total_data', regionsfl:str='alberta_region_data',
                   testfl:str='alberta_testing_data', fltypes=('csv', 'json'),
                   combine_dataframes:bool=False, return_dataframes:bool=False):
        '''scrape the total alberta covid-19 case counts, the covid-19 case counts by
        region and the testing data from the alberta covid-19 website

        Parameters:
            output_filename:str
                filename without the file ending
            fltypes:[list or str]
                will save out either csv, json or both filetypes
            return_dataframe:bool
                will return either the dataframes or a true/false on write success
        Returns:
            all_data
                if combine_dataframes = True
            totals, regions, testing
                if combine_dataframes = False

        '''
        totals = self.scrape_albertaTotals(output_filename=totalfl, fltypes=fltypes, return_dataframe=return_dataframes)
        regions = self.scrape_albertaRegions(output_filename=regionsfl, fltypes=fltypes, return_dataframe=return_dataframes)
        testing = self.scrape_albertaTesting(output_filename=testfl, fltypes=fltypes, return_dataframe=return_dataframes)
        if combine_dataframes:
            all_data = totals.join([regions, testing])
            return all_data
        return totals, regions, testing
