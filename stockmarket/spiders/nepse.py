import scrapy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from scrapy.http import HtmlResponse
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import datetime


class NepseSpider(scrapy.Spider):
    name = "nepse"
    allowed_domains = ["www.sharesansar.com"]
    # start_urls = ["https://www.sharesansar.com/today-share-price"]
    def start_requests(self):        
        url = "https://www.sharesansar.com/today-share-price"
        yield scrapy.Request(url=url, callback=self.parse) 

    def parse(self, response):
        driver = webdriver.Edge(executable_path=r"stockmarket\msedgedriver.exe")
        driver.get("https://www.sharesansar.com/today-share-price")
        time.sleep(5)
        #get todays date only
        date_field = datetime.date.today()
        # date_field = "2023-01-04"
        # date_field = datetime.datetime.strptime(date_field, '%Y-%m-%d').date()
        for i in range(0,365):
            yield from self.scraper(driver,date_field)      
            date_field = date_field - datetime.timedelta(days=1)
        driver.close()
        driver.quit()
        
    def scraper(self,driver,date_field):
        search = driver.find_element(By.CSS_SELECTOR,"div.form-group>input#fromdate")
        ##clear the date field
        search.clear()
        ##fill the date field
        search.send_keys(date_field.strftime('%Y/%m/%d'))
        search.send_keys(Keys.ENTER)
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "dow")))      
        ##click on search button
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "btn_todayshareprice_submit")))
        search_button = driver.find_element(By.ID,"btn_todayshareprice_submit")
        search_button.click()
        
        time.sleep(5)
        response = HtmlResponse(url=driver.current_url, body=driver.page_source, encoding='utf-8')
        #wait for the reposne to load
        wait = WebDriverWait(driver, 15)
        try:
            for data in response.css("tbody tr"):
                if data.css("td:nth-child(20)::text").get() is not None:    
                    yield {
                        "company_name": data.css("td:nth-child(2) a::text").get(),
                        "date": date_field.strftime('%Y/%m/%d'),
                        "confidence": data.css("td:nth-child(3)::text").get(),
                        "open_price": data.css("td:nth-child(4)::text").get(),
                        "lowest_price": data.css("td:nth-child(5)::text").get(),
                        "highest_price": data.css("td:nth-child(6)::text").get(),
                        "closing_price": data.css("td:nth-child(7)::text").get(),
                        "VWAP": data.css("td:nth-child(8)::text").get(),
                        "total_traded_quantity": data.css("td:nth-child(9)::text").get(),
                        "Previous_closing": data.css("td:nth-child(10)::text").get(),
                        "total_traded_value": data.css("td:nth-child(11)::text").get(),
                        "total_trades": data.css("td:nth-child(12)::text").get(),
                        "difference": data.css("td:nth-child(13)::text").get(),
                        "range": data.css("td:nth-child(14)::text").get(),
                        "difference_percentage": data.css("td:nth-child(15)::text").get(),
                        "range_percentage": data.css("td:nth-child(16)::text").get(),
                        "VWAP_percentage": data.css("td:nth-child(17)::text").get(),
                        # "120_days": data.css("td:nth-child(18)::text").get(),
                        # "180_days": data.css("td:nth-child(19)::text").get(),
                        "52_weeks_high": data.css("td:nth-child(20)::text").get(),
                        "52_weeks_low": data.css("td:nth-child(21)::text").get(),
                        
                    }
                else:
                    yield{
                            "company_name": data.css("td:nth-child(2) a::text").get(),
                            "date": date_field.strftime('%Y/%m/%d'),
                            "confidence": data.css("td:nth-child(3)::text").get(),
                            "open_price": data.css("td:nth-child(4)::text").get(),
                            "lowest_price": data.css("td:nth-child(5)::text").get(),
                            "highest_price": data.css("td:nth-child(6)::text").get(),
                            "closing_price": data.css("td:nth-child(7)::text").get(),
                            "VWAP": data.css("td:nth-child(8)::text").get(),
                            "total_traded_quantity": data.css("td:nth-child(9)::text").get(),
                            "Previous_closing": data.css("td:nth-child(10)::text").get(),
                            "total_traded_value": data.css("td:nth-child(11)::text").get(),
                            "total_trades": data.css("td:nth-child(12)::text").get(),
                            "difference": data.css("td:nth-child(13)::text").get(),
                            "range": data.css("td:nth-child(14)::text").get(),
                            "difference_percentage": data.css("td:nth-child(15)::text").get(),
                            "range_percentage": data.css("td:nth-child(16)::text").get(),
                            "VWAP_percentage": data.css("td:nth-child(17)::text").get(),
                            # "120_days": data.css("td:nth-child(18)::text").get(),
                            # "180_days": data.css("td:nth-child(19)::text").get(),
                            "52_weeks_high": data.css("td:nth-child(18)::text").get(),
                            "52_weeks_low": data.css("td:nth-child(19)::text").get(),
                        
                    }                    
        except:
            print("nothing found")
            pass
        
            
            
