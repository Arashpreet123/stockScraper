import requests
from bs4 import BeautifulSoup
import csv

def scrape_uci_datasets():
    base_url = "https://www.tradingview.com/symbols/SPX/"

    headers = [
        "Stock Name", "live Price", "Day Change",
        "PE Ratio", "Forward Dividend & Yield", "ROI", "EPS"
    ]


    # List to store the scraped data
    data = []


    def scrape_dataset_details(dataset_url):
        response = requests.get(dataset_url)
        soup = BeautifulSoup(response.text, 'html.parser')


        dataset_name = soup.find(
            'h1', class_='yf-xxbei9')
        dataset_name = dataset_name.text.strip() if dataset_name else "N/A"

        live_price = soup.find('fin-streamer', class_='livePrice yf-1tejb6')
        # description = soup.find('p', class_='svelte-17wf9gp')
        live_price = live_price.text.strip() if live_price else "N/A"


        day_change = soup.find('fin-streamer', class_='priceChange yf-1tejb6')
        day_change = day_change.text.strip() if day_change else "N/A"

        # pe_ratio = soup.find_all('fin-streamer', class_='yf-mrt107')
        # print(pe_ratio[0].text)
        
        pe_ratio = soup.find('fin-streamer', {'class': 'yf-mrt107', 'data-field': 'trailingPE'})
        pe_ratio = pe_ratio.text
        
        dividend_yield = soup.findAll('span', {'class': 'value yf-mrt107'})
        # dividend_yield = dividend_yield.text

        dividend_yield = dividend_yield[13].text
        
        eps = soup.findAll('fin-streamer', {'class' : 'yf-mrt107', 'data-field' : 'trailingPE'})
        # print(eps[1].text.strip())
        eps = eps[1].text.strip()
        list_of_roi = soup.findAll('p', {'class' : 'value yf-lc8fp0'})

        roi = list_of_roi[1].text
        
        # for x in list_of_roi:
        #     print(x, "\n")
        print (pe_ratio)
        if pe_ratio == '-- ':
            pe_ratio = round((float(live_price))/(float(eps)),2)
            print("None")

        return [
            dataset_name, live_price, day_change, pe_ratio, dividend_yield, roi, eps
        ]


    def scrape_datasets(page_url):
        response = requests.get(page_url)
        soup = BeautifulSoup(response.text, 'html.parser')


        dataset_list = soup.find_all(
                        'a', class_='ticker medium hover stacked yf-138ga19')

        # print(dataset_list)
        
        # print(dataset_list)
        # if not dataset_list:
        #     print("No dataset links found")
        #     return
        
        # dataset_link = "https://finance.yahoo.com/quote/SOFI/"
        
        dataset_link = "https://finance.yahoo.com/markets/stocks/most-active/"

        # dataset_details = scrape_dataset_details(dataset_link)
        # data.append(dataset_details)
        
        # print(f"Scraping details for {dataset.text.strip()}...")

        for dataset in dataset_list:
            # print(dataset.text)
            dataset_link = "https://finance.yahoo.com/"+dataset['href']
            print(f"Scraping details for {dataset.text.strip()}...")
            dataset_details = scrape_dataset_details(dataset_link)
            data.append(dataset_details)
            


    # Loop through the pages using the pagination parameters
    skip = 0
    take = 10
    while True:
        page_url = f"https://finance.yahoo.com/markets/stocks/most-active/"
        # page_url = f"https://finance.yahoo.com/quote/SOFI/"

        print(f"Scraping page: {page_url}")
        initial_data_count = len(data)
        scrape_datasets(page_url)
        break
        if len(
                data
        ) == initial_data_count: 
            break
        skip += take


    with open('uci_datasets.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(data)
    


    print("Scraping complete. Data saved to 'uci_datasets.csv'.")


scrape_uci_datasets()
