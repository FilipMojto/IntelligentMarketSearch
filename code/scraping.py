
import bs4, requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ProductScraper:

    def __init__(self) -> None:
        pass


    def get_soup_from_browser(self, link: str, sleep_: float = 5) -> bs4.BeautifulSoup:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        
        driver = webdriver.Chrome(options=chrome_options)
        
        try:
            driver.get(link)
            # Wait for some time to let the initial content load
            time.sleep(sleep_)
            
            # Get the fully rendered HTML content
            page_source = driver.page_source
            return bs4.BeautifulSoup(page_source, 'html.parser')
        finally:
            driver.quit()
    
    def scrape_static_html(self, link: str) -> bs4.BeautifulSoup:
        response = requests.get(link)

        if response.status_code == 200:
            return bs4.BeautifulSoup(response.content, 'html.parser')
        else:
            raise Exception(f"Failed to fetch the page. Status code: {response.status_code}")


    def scrape_dynamic_html(self, link: str) -> bs4.BeautifulSoup:
        soup: bs4.BeautifulSoup = self.get_soup_from_browser(link=link)

        if soup == None:
            raise ValueError("No HTML downloaded!")
        
        return soup

class HTML_Processor:

    def __init__(self, output_file: str = './resources/output.csv', delimiter = ',', market_ID: int = -1, overwrite = False) -> None:
        self.__output_file = output_file
        self.__delimiter = delimiter
        self.__market_ID = market_ID
        self.__overwrite = overwrite
        pass

    def process_html(self, link: str, sleep_: float = 3):
        if self.__overwrite:
            open(self.__output_file, 'w')

        chrome_options = Options()
        chrome_options.add_argument("--headless")

        driver = webdriver.Chrome(options=chrome_options)

        try:
            driver.get(link)

            # Initial wait for some time to let the initial content load
            time.sleep(sleep_)

            max_attempts = 10  # Adjust this based on your needs
            current_attempt = 0

            time.sleep(sleep_)
            page_source = driver.page_source
            soup = bs4.BeautifulSoup(page_source, 'html.parser')
            
            cur = soup.find('h2', class_='sc-1c276b2a-6 hLDXoc').get_text()


            while current_attempt < max_attempts:
                # Scroll down a little (adjust the pixel value based on your needs)
                

                # Wait for a short time (adjust sleep duration based on your needs)
                time.sleep(sleep_)

                # Get the fully rendered HTML content after scrolling
                page_source = driver.page_source

                # Create a new soup object with the updated HTML content
                soup = bs4.BeautifulSoup(page_source, 'html.parser')

                subsections = soup.find('div', class_="sc-b27603a9-0 gVLwyA").find_all('div', recursive=False)

                for index, subsection in enumerate(subsections):
                    print("\nANOTHER SUBSECTION!\n")
                    products = subsection.find_all('div', recursive=False)

                    for index, product in enumerate(products):
                        
                        print(index + 1)

                        csv_record = product.find('h3', {'data-test-id': 'ImageCentricProductCard.Title'}).get_text().replace(',', '')
                        
                        # Your processing logic...

                        csv_record += self.__delimiter
                        price = product.find('div', {'data-test-id': 'ImageCentricProductCardPrice'}).get_text().replace(',', '.').split('€')
                        approximation = 0

                        if price[0][0] == '~':
                            approximation = 1
                            price[0] = price[0][1:]

                        csv_record += price[0] + '€'

                        csv_record += self.__delimiter
                        csv_record += str(approximation)
                        
                        if (self.__market_ID > -1):

                            csv_record += self.__delimiter
                            csv_record += str(self.__market_ID)
                        
                        csv_record += '\n'

                        with open(file=self.__output_file, mode='a', encoding='utf-8') as file:
                            file.write(csv_record)

                        print(csv_record)

                with open(file=self.__output_file, mode='a', encoding='utf-8') as file:
                    file.write('\n')

                # Check if the target class is present
                h2_element = soup.find('h2', class_='sc-1c276b2a-6 hLDXoc')
                
                if h2_element and (not cur or h2_element.get_text() != cur):
                    break  # Exit the loop if the class is found

                current_attempt += 1
                driver.execute_script("window.scrollBy(0, 10000);")
                

        finally:
            driver.quit()

        # if self.__overwrite:
        #     open(self.__output_file, 'w')

        # sections = soup.find('div', {'data-test-id': 'productCatalog.productCategoryScreen'}).find_all('div', recursive=False)

        # #processed_categories = []

        # for section in sections:

        #     print("\nANOTHER SECTION!\n")
        #     subsections = section.find('div', class_="sc-b27603a9-0 gVLwyA").find_all('div', recursive=False)

        #     for index, subsection in enumerate(subsections):
        #         print("\nANOTHER SUBSECTION!\n")
        #         products = subsection.find_all('div', recursive=False)

        #         for index, product in enumerate(products):
                    
        #             print(index + 1)

        #             csv_record = product.find('h3', {'data-test-id': 'ImageCentricProductCard.Title'}).get_text().replace(',', '')
                    
        #             # if index == 0:
        #             #     present = False

        #                 # for el in processed_categories:
        #                 #     if el == csv_record:
        #                 #         present = True
        #                 #         print("PRESENT!")

        #                 #         print(csv_record)
        #                 #         print(el)
        #                 #         break

        #                 #     if exit_event.is_set():
        #                 #         exit(1)

        #                 # else:
        #                 #     print("NOT PRESENT!  Adding...")
        #                 #     print(csv_record)
        #                 #     processed_categories.append(csv_record)
                        
        #                 # if present:
        #                 #     break

        #             csv_record += self.__delimiter
        #             price = product.find('div', {'data-test-id': 'ImageCentricProductCardPrice'}).get_text().replace(',', '.').split('€')
        #             approximation = 0

        #             if price[0][0] == '~':
        #                 approximation = 1
        #                 price[0] = price[0][1:]

        #             csv_record += price[0] + '€'

        #             csv_record += self.__delimiter
        #             csv_record += str(approximation)
                    
        #             if (self.__market_ID > -1):

        #                 csv_record += self.__delimiter
        #                 csv_record += str(self.__market_ID)
                    
        #             csv_record += '\n'

        #             with open(file=self.__output_file, mode='a', encoding='utf-8') as file:
        #                 file.write(csv_record)

                    

        #             print(csv_record)

            #         if exit_event.is_set():
            #             exit(1)
                
            #     if exit_event.is_set():
            #         exit(1)

            # if exit_event.is_set():
            #     exit(1)

if __name__ == "__main__":

    # url = 'https://wolt.com/sk/svk/bratislava/venue/tesco-kamenne-namestie/items/sladke-22'
    # response = requests.get(url)

    # if response.status_code == 200:
    #     soup = bs4.BeautifulSoup(response.content, 'html.parser')
    #     sections = soup.find('div', {'data-test-id': 'productCatalog.productCategoryScreen'}).find_all('div', recursive=False)
    #     # Rest of your code here
    # else:
    #     print(f"Failed to fetch the page. Status code: {response.status_code}")

    scraper = ProductScraper()
    processor = HTML_Processor(overwrite=True)

    soup = scraper.scrape_dynamic_html(link='https://wolt.com/sk/svk/bratislava/venue/tesco-kamenne-namestie/items/sladke-22')
    
    processor.process_html(link='https://wolt.com/sk/svk/bratislava/venue/tesco-kamenne-namestie/items/sladke-22')





