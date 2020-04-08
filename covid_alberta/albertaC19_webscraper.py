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

    def scrape_albertaTotals(self, output_filename:str='albertaTotalData', fltypes=('csv', 'json'),
                             return_dataframe:bool=False):
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

        '''scrape the total case counts in alberta and save the data to the output folder

        Parameters:
            output_filename:str
                filename without the file ending
            fltypes:[list or str]
                will save out either csv, json or both filetypes
            return_dataframe:bool
                will return either the dataframes or a true/false on write success
        '''
        results = self.soup.find(id='case-counts')
        caseCountResults = results.find_all('script')

        # Scrape the data
        caseCountCum = json.loads(caseCountResults[0].string)
        caseCountByDat = json.loads(caseCountResults[2].string)
        albertaTotalData = {'cumulative': {'date': caseCountCum['x']['data'][0]['x'],
                                           'cum_cases': caseCountCum['x']['data'][0]['y']},
                            'byDay': {'date': caseCountByDat['x']['data'][0]['x'],
                                      'new_cases': caseCountByDat['x']['data'][0]['y']}
                            }
        # Write out or Return the data
        write_sucess = False
        if 'json' in fltypes:
            flpath = self.outputfolder.joinpath(output_filename).with_suffix('.json')
            aTotal = json.dumps(albertaTotalData)
            with open(flpath, "w") as fl:
                fl.write(aTotal)
            write_sucess = True
        if 'csv' in fltypes or return_dataframe:
            flpath = self.outputfolder.joinpath(output_filename).with_suffix('.csv')
            abTotalCum = pd.DataFrame(data=albertaTotalData['cumulative']['cum_cases'],
                                      index=albertaTotalData['cumulative']['date'],
                                      columns=['cum_cases'])
            abTotalCum.index = pd.to_datetime(abTotalCum.index)

            abTotalNCases = pd.DataFrame(data=albertaTotalData['byDay']['new_cases'],
                                         index=albertaTotalData['byDay']['date'],
                                         columns=['new_cases'])
            abTotalNCases.index = pd.to_datetime(abTotalNCases.index)
            abTotal = abTotalNCases.join(abTotalCum)

            if 'csv' in fltypes:
                abTotal.to_csv(flpath)
            if return_dataframe:
                return abTotal
            write_sucess = True
        return write_sucess

    def scrape_albertaRegions(self, output_filename:str='albertaRegionData', fltypes=('csv', 'json'),
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
        results = self.soup.find(id='geospatial')
        regionCaseCountResults = results.find_all('script')
        regionCCDict = json.loads(regionCaseCountResults[0].string)['x']

        zoneLen = len(regionCCDict['data'])
        albertaRegionData = dict()
        for idx in range (zoneLen):
            zoneName = regionCCDict['data'][idx]['name']
            albertaRegionData[zoneName] = {'date':regionCCDict['data'][idx]['x'],
                                           'new_cases':regionCCDict['data'][idx]['y']}
        write_sucess = False
        # Write out the data
        if 'json' in fltypes:
            flpath = self.outputfolder.joinpath(output_filename).with_suffix('.json')
            aRegion = json.dumps(albertaRegionData)
            with open(flpath, "w") as fl:
                fl.write(aRegion)
            write_sucess = True
        if 'csv' in fltypes or return_dataframe:
            flpath = self.outputfolder.joinpath(output_filename).with_suffix('.csv')
            abRegions = list()
            for idx, key in enumerate(albertaRegionData.keys()):
                if 'Zone' in key:
                    zone = key.strip(' Zone')
                else:
                    zone = key
                column = f'{zone}_newCases'
                abRegions.append(pd.DataFrame(data=albertaRegionData[key]['new_cases'],
                                              index=albertaRegionData[key]['date'],
                                              columns=[column]))

            abRegionsDF = abRegions[0].join(abRegions[1:])
            abRegionsDF.index = pd.to_datetime(abRegionsDF.index)
            abRegionsDF.fillna(0, inplace=True)
            abRegionsDF = abRegionsDF.astype(int)

            if 'csv' in fltypes:
                abRegionsDF.to_csv(flpath)
            if return_dataframe:
                return abRegionsDF
            write_sucess = True
        return write_sucess

    def scrape_albertaTesting(self, output_filename:str='albertaTestingData', fltypes=('csv', 'json'),
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
        results = self.soup.find(id='laboratory-testing')
        testingResults = results.find_all('script')

        # Scrape the data
        testingDict = json.loads(testingResults[0].string)['x']
        testingDict.keys()
        albertaTestingData = dict()
        for idx in range(len(testingDict['data'])):
            albertaTestingData[testingDict['data'][idx]['name']] = {'date': testingDict['data'][idx]['x'],
                                                                    'n_tests': testingDict['data'][idx]['y']}
        # Write out the data
        write_sucess = False
        if 'json' in fltypes:
            flpath = self.outputfolder.joinpath(output_filename).with_suffix('.json')
            aTest = json.dumps(albertaTestingData)
            with open(flpath, "w") as fl:
                fl.write(aTest)
            write_sucess = True
        if 'csv' in fltypes or return_dataframe:
            flpath = self.outputfolder.joinpath(output_filename).with_suffix('.csv')
            abTesting = list()
            for idx, key in enumerate(albertaTestingData.keys()):
                column = f'{key}_newTests'
                abTesting.append(pd.DataFrame(data=albertaTestingData[key]['n_tests'],
                                              index=albertaTestingData[key]['date'],
                                              columns=[column]))
            abTestsDF = abTesting[0].join(abTesting[1:])
            abTestsDF.index = pd.to_datetime(abTestsDF.index)
            abTestsDF.fillna(0, inplace=True)
            abTestsDF = abTestsDF.astype(int)

            if 'csv' in fltypes:
                abTestsDF.to_csv(flpath)
            if return_dataframe:
                return abTestsDF
            write_sucess = True
        return write_sucess

    def scrape_all(self, totalfl:str='albertaTotalData', regionsfl:str='albertaRegionData',
                   testfl:str='albertaTestingData', fltypes=('csv', 'json'),
                   return_dataframes:bool=False):
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
            totals, regions, testing

        '''
        totals = self.scrape_albertaTotals(totalfl, fltypes, return_dataframes)
        regions = self.scrape_albertaRegions(regionsfl, fltypes, return_dataframes)
        testing = self.scrape_albertaTesting(testfl, fltypes, return_dataframes)
        return totals, regions, testing
