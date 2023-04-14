import os
import pandas as pd
import re

from datetime import datetime, timedelta


class DataManager:

    def __init__(self):
        self.dataframe: pd.DataFrame = None
        self.last: pd.DataFrame = None
        self.date_list: list = self.get_date_list()
        self.already_entry: set = set()
        self.entry_list: list = []
        self.date: str = None   # YYYY-MM-DD

    def set_df(self, date: str) -> None:
        """
        Set up DataFrame

        Parameters:
        --------------------
        date : str
            date that needed to set up DataFrame
        """
        self.reset_df()
        self.date_list = self.get_date_list()   # Get date_list
        # print(self.date_list)

        if len(self.date_list) == 0:
            return  # "Not have any date.csv files"
        elif self.check_file(date):
            if date == "data":
                path = "./backup/data.csv"
            else:
                path = "./backup/file_date/{}.csv".format(date)
            self.dataframe = pd.read_csv(path)

    def reset_df(self) -> None:
        self.dataframe = None

    def sort_df(self) -> None:
        self.dataframe.sort_values(by=['Entry_id'])

    def check_file(self, date: str) -> bool:
        """
        Set up DataFrame

        Parameters:
        --------------------
        date : str
            date that needed to set up DataFrame

        Returns
        -------
        bool
            Is File created
        """
        if date == "data":
            path = "./backup/data.csv"
            if os.path.isfile(path):
                return True
            else:
                # print("Not have data.csv file")
                return False
        else:
            path = "./backup/file_date/{}.csv".format(date)
            if os.path.isfile(path):
                return True
            else:
                # print("Not have {}.csv file".format(date))
                return False

    def check_entry(self, entry_id: str) -> bool:
        return entry_id in self.dataframe['Entry_id'].values

    def new_entries(self, jdata: dict) -> pd.DataFrame:
        """
        Made Entries JSON to Data Frame

        Parameters:
        --------------------
        jdata : dict
            dict form requested

        Returns
        -------
        DataFrame
            DataFrame that contains from a the entries
        """
        datetime = self.get_datetime(jdata)

        data = [[
            jdata['entry_id'],   # entry_id
            datetime[0],         # date
            datetime[1],         # time
            jdata['field1'],     # light value
            jdata['field2'],     # temperature
            jdata['field3'],     # humidity
            jdata['field4']      # PM2.5
        ]]

        df = pd.DataFrame(data, columns=[
            'Entry_id',
            'Date',
            'Time',
            'Light Value',
            'Temperature',
            'RH',
            'PM'
        ])

        return df

    def datefile(self, date: str, jdata: dict) -> None:
        """
        Create a date file from a entry

        Parameters:
        --------------------
        date : str
            date that needed to made DataFrame
        jdata : dict
            dict form requested
        """
        temp_df = self.new_entries(jdata)

        if self.check_file(date):

            self.set_df(date)

            if self.check_entry(jdata['entry_id']):
                self.entry_list.append(jdata['entry_id'])
                # print('\nEntry_id {} already had.\n\n'.format(
                #     jdata['entry_id']))
                # print(self.dataframe, '\n')
            else:
                self.union_date_csv(date, temp_df)
                # print('\nNow!! Entry_id {} is added.\n\n'.format(
                #     jdata['entry_id']))
                # print(self.dataframe, '\n')
            if self.entry_list:
                self.already_entry.update(self.entry_list)

        else:
            self.reset_df()
            self.union_date_csv(date, temp_df)

    def convent_csv(self, date: str) -> None:
        """
        Convent DataFrame to CSV flie

        Parameters:
        --------------------
        date : str
            title of the file to be CSV file
        """
        if date == "data":
            path = "./backup/data.csv"
        else:
            path = "./backup/file_date/{}.csv".format(date)
        self.sort_df()
        self.dataframe.to_csv(path, index=False, encoding='utf-8')
        # print('done')

    def union_date_csv(self, date: str, data: pd.DataFrame) -> None:
        """
        Union DataFrame and Convent to CSV file

        Parameters:
        --------------------
        date: str
            title of the file to be CSV file
        data: DataFrame
            DataFrame that will be unioned into CSV file
        """
        self.dataframe = pd.concat([self.dataframe, data])
        self.convent_csv(date)

    def union_all_csv(self) -> None:
        """
        Union All DateFile and Convent to CSV file
        """
        path = "./backup/data.csv"
        if os.path.isfile(path):
            all_data = pd.read_csv(path, encoding='utf8')
        else:
            all_data = pd.DataFrame()

        # get date list
        date_list = self.get_date_list()

        # Union all date file
        for date in date_list:
            union_data = pd.read_csv(
                './backup/file_date/{}.csv'.format(date))
            all_data = pd.concat([all_data, union_data], ignore_index=True)

        # Convert union data to CSV
        self.convent_csv("data")

    def get_date_list(self) -> list:
        """
        Get list datelist in directory
        """
        folder = './backup/file_date'
        date_list = ['.'.join(x.split('.')[:-1]) for x in os.listdir(folder)
                     if os.path.isfile(os.path.join(folder, x))]

        return date_list

    def get_datetime(self, jdata: dict) -> list:
        """
        Get list datetime in dict

        Returns
        -------
        List
            List = ['DD/MM/YYYY', HH:MM:SS]
        """
        datetime = []
        # Get date ['YYYY', 'MM', 'DD']
        date = self.get_date(jdata)
        date_str = "{}/{}/{}".format(date[2], date[1], date[0])
        datetime.append(date_str)
        # Get time
        time_str = self.get_time(jdata)
        datetime.append(time_str)

        return datetime

    def get_date(self, jdata: dict) -> list:
        return jdata['created_at'][0:10].split("-")

    def get_time(self, jdata: dict) -> str:
        time = jdata['created_at'][11:-1]
        time_str = (datetime.strptime(time, "%H:%M:%S") +
                    timedelta(hours=7)).strftime("%X")

        return time_str

    def get_entity_id(self, jdata: dict) -> int:
        return int(jdata['entry_id'])
