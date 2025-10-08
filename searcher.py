import bs4
from bs4 import BeautifulSoup
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from generator import Generator

import threading
def get_records(tag: bs4.element.Tag):
    """returns all the tr tags inside the table that have style=color:#333333;background-color:#FFFBD6; or style=color:#333333;background-color:White;height:45px; """
    target_styles = {
        "color:#333333;background-color:White;height:45px;",
        "color:#333333;background-color:#FFFBD6;"
    }
    return tag.name == "tr" and tag.get("style") in target_styles


class WebSearcher:
    def __init__(self, webdriver):
        self.webdriver = webdriver
        self.data = []
        self.data_lock = threading.Lock()

    def get_data(self):
        return self.data

    def search_site(self,firstname_substring, surname_substring):
        firstname_input =  WebDriverWait(driver=self.webdriver,timeout=10).until(
            EC.visibility_of_element_located((By.ID, "MainContent_TextBoxName"))
        )
        surname_input =  WebDriverWait(driver=self.webdriver,timeout=10).until(
            EC.visibility_of_element_located((By.ID, "MainContent_TextBoxSurname"))
        )

        firstname_input.clear()
        surname_input.clear()
        firstname_input.send_keys(firstname_substring)
        surname_input.send_keys(surname_substring)

        submit_button =  WebDriverWait(driver=self.webdriver,timeout=10).until(
            EC.visibility_of_element_located((By.ID, "MainContent_cmdSearch"))
        )
        # interact with site
        submit_button.click()
        # wait for site to load table, if no table exit
        try:
            WebDriverWait(self.webdriver,15).until(EC.presence_of_element_located((By.ID, "MainContent_GridView1")))
        except TimeoutException:
            print("No results table appeared — continuing without parsing.")
            return

        # get page source
        page_src = BeautifulSoup(self.webdriver.page_source,"html.parser")

        # get the table
        table = page_src.find("table", {"id":"MainContent_GridView1"})

        records_to_add = []
        table_records = table.find_all(get_records) #list of <tr> and children
        for record in table_records: # iterating over each <tr>
            record_content = record.contents

            records_to_add.append({
                "RegNo" : record_content[2].text,
                "Given Names": record_content[3].text,
                "Surname": record_content[4].text,
                "Sex" : record_content[5].text,
                "Address" : record_content[6].text,
                "Occupation" : record_content[7].text,
                "PD" : record_content[8].text,

            })
        # Thread-safe data append
        with self.data_lock:
            self.data.extend(records_to_add)

    def main_search(self):
        gen = Generator()
        vowel_patterns = gen.get_patterns(2)
        for vowel_pattern in vowel_patterns.values():
            for consonant_combos in vowel_pattern:
                for combo in consonant_combos:
                    self.search_site(*combo)

    def process_vowel_pattern(self, pattern_data, webdriver_factory):
        """Process all searches for a specific vowel pattern in a separate thread"""
        # Create a new webdriver instance for this thread
        thread_driver = webdriver_factory()
        thread_searcher = WebSearcher(thread_driver)

        try:
            for consonant_combos in pattern_data:
                for combo in consonant_combos:
                    thread_searcher.search_site(*combo)

            # Merge thread results into main data (thread-safe)
            with self.data_lock:
                self.data.extend(thread_searcher.data)
        finally:
            # Clean up the webdriver
            thread_driver.quit()

    def true_search(self, webdriver):
        """
        Main search with multithreading

        Args:
            webdriver_factory: A callable that returns a new WebDriver instance
                              Example: lambda: webdriver.Chrome()
                              :param webdriver:
        """
        gen = Generator()
        vowel_patterns = gen.get_patterns(0)

        threads = []
        for vowel, pattern_data in vowel_patterns.items():
            thread = threading.Thread(
                target=self.process_vowel_pattern,
                args=(pattern_data, webdriver)
            )
            thread.start()
            threads.append(thread)

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        print(f"Search complete. Total records collected: {len(self.data)}")