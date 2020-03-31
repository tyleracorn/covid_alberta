import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
from pathlib import Path


class albertaC19_webscraper():
    def __init__(self, covid_url:str='https://covid19stats.alberta.ca/', outputfolder:str='data'):
        '''
        using requests and BeautfulSoup4 scrape updated covid data from the ablerta website
        save the outputs into a outputfolder
        '''
        self.covid_url = covid_url
        self.outputfolder = Path(outputfolder)
        if not self.outputfolder.is_dir(): self.outputfolder.mkdir()

        self.page = requests.get(self.covid_url)
        self.soup = BeautifulSoup(self.page.content, 'html.parser')

    def scrape_albertaTotals(self, output_filename:str='albertaTotalData', fltypes=['csv', 'json'],
                             return_dataframe:bool=False):
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

    def scrape_albertaRegions(self, output_filename:str='albertaRegionData', fltypes=['csv', 'json'],
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

    def scrape_albertaTesting(self, output_filename:str='albertaTestingData', fltypes=['csv', 'json'],
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
                   testfl:str='albertaTestingData', fltypes=['csv', 'json'],
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
