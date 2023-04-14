import sys
import time
from tqdm import tqdm

from Widgets.DataManager import DataManager
from Widgets.RequestTS import RequestTS

if __name__ == "__main__":

    dm = DataManager()
    rts = RequestTS()

    try:
        print("\nit's working...")

        i = 18
        # print("Use Ctrl-C to quit")

        while True:

            if i == 18:
                print("\n\nThingSpeak is running\n")
                getdata = rts.get_data()
                all_data = getdata["feeds"]

                # Each entry
                for j in tqdm(range(len(all_data))):
                    data = all_data[-j]
                    date = dm.get_date(data)
                    date_str = "{}-{}-{}".format(date[0], date[1], date[2])

                    dm.datefile(date_str, data)

                # Convert all data
                dm.union_all_csv()

                i = 1
                dm.entry_list = []
                print("\nThingSpeak Scraping is finished\n")
                print("Use Ctrl-C to quit")

            print(".", end=' ')
            i += 1
            time.sleep(1)

    except KeyboardInterrupt:
        print('\n\nStop!!')
