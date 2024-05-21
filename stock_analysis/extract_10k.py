import os
import pandas as pd

# Load Api keys
from dotenv import load_dotenv
load_dotenv()

# Pulls 10K data
from sec_api import ExtractorApi

# fixes character encoding
from bs4 import BeautifulSoup

class Preprocess10K():
    """
    data_fmt_list - True if you want the data stored internally as a list, false
    if you want it stored as a dict
    
    A wrapper around the 'sec_api' ExtractorApi which manages the extracted data,
    cleans/changes the encoding via bs4. Can save/load data to disk.
    """

    @staticmethod
    def capture_data(data: str, file_out: str):
        """
        This is a debug function that can just be called as a one-liner to 
        capture or save data to a location during processing for debugging
        """
        dir_name, file_name = os.path.split(file_out)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        with open(file_out, 'w') as file:
            file.write(data)


    def __init__(self, data_fmt_list: bool):
        self.api_key = os.getenv('SEC_API_API_KEY')
        self.extractor_api = ExtractorApi(self.api_key)
        self.extracted_data = {}
        self.extracted_data_list = []
        self.is_list = data_fmt_list

    def extract(self, url: str, sections: list):
        """
        Utilizes 'sec-api' class ExtractorApi to get sections of a 10K.
        Expects the url in the format from the df['linkToFilingDetails'] key.
        """

        for s in sections:
            if self.is_list == True:
                self.extracted_data_list.append(self.extractor_api.get_section(url, s, 'text'))
            else:
                self.extracted_data[s] = self.extractor_api.get_section(url, s, 'text')

    def clean_encoding(self):
        """
        Sometimes data extracted from 10K's through the ExtractorApi contains
        special HTML characters formatted like '&#8704'. This optional method removes
        them using BeautifulSoup
        """
        if self.is_list == True:
            if self.extracted_data_list == []:
                print('Extracted data is empty!')
                return
            
            for idx in range(len(self.extracted_data_list)):
                self.extracted_data_list[idx] = BeautifulSoup(
                    self.extracted_data_list[idx],
                    features='lxml'
                ).contents[0]

                self.extracted_data_list[idx] = BeautifulSoup(
                    self.extracted_data_list[idx], 'html.parser'
                ).contents[0]
        else:
            if self.extracted_data == {}:
                print('Extracted data is empty!')
                return

            for key in self.extracted_data.keys():
                self.extracted_data[key] = BeautifulSoup(
                    self.extracted_data[key],
                    features='lxml'
                ).contents[0]

                self.extracted_data_list[key] = BeautifulSoup(
                    self.extracted_data_list[key], 'html.parser'
                ).contents[0]



    def dump(self):
        """
        Dumps the extracted contents into a json file 
        in the given directory. use format '/your/path/<file>.json'.
        Useful for reducing API usage.
        """

    def load(self):
        """
        Loads a json file containing sections of a 10K 
        fetched already by sec-api's ExtractorApi. 
        Useful for reducing API usage.
        """

    def clear(self):
        """
        Clears the contents of the extracted data stored in memory. Useful
        if the data has already been written to disk and another batch needs
        fetched, or if the contents are no longer useful
        """
        self.extracted_data = {}