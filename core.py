from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import time

from data_handler import DataHandler
from searcher import WebSearcher






if __name__ == "__main__":

    sel_driver = webdriver.Firefox()
    try:
        sel_driver.get("https://www.peogrenada.org/ElectorialListing/Method2")

        searcher = WebSearcher(sel_driver)

        start = time.time()

        searcher.main_search()
        search_end = time.time()
        print(f'Search Time: {search_end - start:.2f} seconds')

        csv_start = time.time()
        csv_conv = DataHandler(searcher.get_data())
        csv_conv.to_csv()
        csv_end = time.time()
        print(f'Conversion Time: {csv_end - csv_start:.2f} seconds')

        print(f'Total Time: {csv_end - start:.2f} seconds')


    except TimeoutException:
        print("Timed out waiting for results")
    finally:
        sel_driver.quit()