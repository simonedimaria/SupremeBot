from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from threading import Thread    
import time
import sys

class BotsFactory(Thread):

    def __init__(self, system, baseurl, n_workers):
        # setting up the webdriver
        self.baseurl = baseurl
        
        # set printing function
        self.system = system
        if 'windows' in system.lower():
            self.print = print
        else:
            self.print = self.pprint
        
        # setting up the threading
        self.n_workers = n_workers
        self.workers = []
        Thread.__init__(self)         

    def pprint(self, text):  print(f'\033[96m {text}\033[00m')

    def startWorkers(self):
        # start the workers (threads)
        for n in range(self.n_workers):
            worker = Thread(target=self.cop)
            worker.start()
            self.workers.append(worker)
            self.print(f'Worker {n} started with name {worker.name}')
    
    def waitAndClick(self, driver, xpath):
        # wait for the element to be clickable and then click it
        btn = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, xpath)) and EC.element_to_be_clickable((By.XPATH, xpath)))
        btn.click()

    def cop(self):
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        driver.maximize_window()        
        driver.get(self.baseurl)

        addToChart_btn = '//*[@id="product-root"]/div/div[2]/div[2]/form/div[2]/div/div[4]/div[3]/div[2]/div[3]/div[2]/input'
        self.waitAndClick(driver, addToChart_btn)
        
        checkout_btn = '//*[@id="product-root"]/div/div[1]/div/div/div/a[2]'
        self.waitAndClick(driver, checkout_btn)
        
        acceptTos_btn = '//*[@id="accept_tos"]'
        self.waitAndClick(driver, acceptTos_btn)

        # @todo : add functionality to autofill the form

        processPayment_btn = '//*[@id="Form0"]/div/div[3]/div/div/div[2]/div/div/div/div[2]/div/div/button'
        self.waitAndClick(driver, processPayment_btn)

        time.sleep(10)

if __name__ == '__main__':

    SYSTEM = sys.platform
    n_workers = int(input('How many workers do you want to start? '))
    product_url = input('Enter the product url: ')

    botsfactory = BotsFactory(SYSTEM, product_url, n_workers)    
    botsfactory.startWorkers()