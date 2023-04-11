import os
import pandas as pd
import re

from datetime import datetime, timedelta


# from Widgets.Sentiment import Sentiment

class data_manager:

    def __init__(self):
        self.data: pd.core.frame.DataFrame = None
        self.last: pd.core.frame.DataFrame = None
        self.last_entry_id: int = 0
        self.date_list: list = self.get_date_list()

    def set_df(self, date: str) -> None:
        # set dataframe
        self.date_list = self.get_date_list()   # Get date_list
        if len(self.date_list) == 0:
            return "Not have any date.csv files"
        elif date == "data":
            path = "./backup/data.csv"
            if os.path.isfile(path):
                self.data.pd.read_csv(path)
            else:
                return "Not have data.csv file"
        else:
            path = "./backup/file_date/{}.csv".format(date)
            if os.path.isfile(path):
                self.data.pd.read_csv(path)
            else:
                return "Not have {}.csv file".format(date)

    def reset_df(self) -> None:
        self.data = None

    def new_entries(self, jdata: dict) -> pd.core.frame.DataFrame:
        """
        Made Entries JSON to Data Frame

        Parameters:
        --------------------
        jdata : dict
            dict form requested
        """
        datetime = self.get_datetime(jdata)

        data = [
            datetime[0],        # date
            datetime[1],        # time
            jdata['field1'],    # light value
            jdata['field2'],    # temperature
            jdata['field3'],    # humidity
            jdata['field3']     # PM2.5
        ]

        df = pd.DataFrame(data, columns=[
            'date',
            'time',
            'Light Value',
            'Temperature',
            'Humidity',
            'PM2.5'
        ])

        return df

    def datefile(self):

        return

    def convent_csv(self, date: str) -> None:
        """
        Covvent DataFrame to CSV flie

        Parameters:
        --------------------
        date : str
            title of the file to be CSV file
        """
        self.data.to_csv(
            'backup/{}.csv'.format(date), index=False, encoding='utf-8')

    def union_date_csv(self, date: str, data: pd.core.frame.DataFrame) -> None:
        """
        Union DataFrame and Convent to CSV file

        Parameters:
        --------------------
        date: str
            title of the file to be CSV file
        data: DataFrame
            DataFrame that will be unioned into CSV file
        """
        self.data = pd.concat([self.data, data])
        self.convent_csv(date)

    def union_all_csv(self) -> None:
        """
        Union All DateFile and Convent to CSV file
        """
        path = "././backup/data.csv"
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
        date_list = [name for name in os.listdir(
            folder) if os.path.isdir(os.path.join(folder, name))]

        return date_list

    def get_datetime(self, jdata: dict) -> list:
        """
        Get list datetime in dict
        """
        datetime = []
        # Get date ['YYYY', 'MM', 'DD']
        date = jdata['created_at'][0:10].split("-")
        date_str = "{}/{}/{}".format(date[2], date[1], date[0])
        datetime.append(date_str)
        # Get time
        time = jdata['created_at'][11:-1]
        time_str = (datetime.strptime(time, "%H:%M:%S") +
                    timedelta(hours=7)).strftime("%X")
        datetime.append(time_str)

        return datetime
