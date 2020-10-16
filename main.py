import argparse
import multiprocessing
import random
import time


from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class ViewBot(multiprocessing.Process):
    def __init__(self, pro, only_view, runtime_views, runtime, url):
        self.pro = pro
        self.only_view = only_view
        self.runtime_views = runtime_views
        self.runtime = runtime
        self.url = url

    def runBot(self):


        #TODO Proxy aufsetzten
        #PROXY = "91.205.174.26:80"
        #webdriver.DesiredCapabilities.FIREFOX['proxy'] = {
        #    "httpProxy": PROXY,
        #    "ftpProxy": PROXY,
        #    "sslProxy": PROXY,
        #    "proxyType": "MANUAL",
        #}

        #with webdriver.Firefox() as driver:
        #    # Open URL
        #    driver.get(url)


        driver = webdriver.Firefox()
        driver.get(self.url)

        # Get video duration for refresh time
        duration_element = driver.find_element_by_class_name('ytp-time-duration')
        runtime_full = duration_element.text
        runtime_calc = runtime_full.split(":")
        runtime_max_sec = (((int(runtime_calc[0]) * 60) / 100) * int(self.runtime))
        print(runtime_max_sec)

        # Signin popup for sponsoered videos
        if self.pro is not None:
            try:
                sponsored_login = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, "//div[@id='dismiss-button']")))
                print(sponsored_login.__dict__)
                for sponsored_element in sponsored_login.find_elements_by_xpath("//div[@id='dismiss-button']"):
                    print(sponsored_element.text)
                    print(sponsored_element.id)
                    print(sponsored_element.get_attribute("class"))
                    # sleep timer to imitaed a "real" person
                    time.sleep(random.uniform(1, 2.5))
                    ActionChains(driver).click(sponsored_element).perform()
            except:
                print("No Login Button")

        # Cookie popup
        WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "iframe")))
        cookieFrame = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@id='introAgreeButton']")))
        print(cookieFrame.__dict__)
        # print(driver.page_source) #html code
        for cookie_element in cookieFrame.find_elements_by_xpath("//div[@id='introAgreeButton']"):
            print(cookie_element.text)
            print(cookie_element.id)
            print(cookie_element.get_attribute("class"))
            # sleep timer to imitated a "real" person
            time.sleep(random.uniform(1, 2.5))
            ActionChains(driver).click(cookie_element).perform()

        # Wait for video container
        time.sleep(5)
        driver.switch_to.default_content()

        # Skip ads
        if self.pro is not None:
            try:
                # wait 5 sec till skip button is available
                time.sleep(5)

                ads_element = driver.find_element_by_class_name('ytp-ad-skip-button-container')
                print(ads_element.__dict__)
                print(ads_element.text)
                ActionChains(driver).click(ads_element).perform()
            except:
                print("No Ads")
        # Min runtime 10 sec
        # Max runtime 70% of video runtime
        print(self.only_view)
        if self.only_view is None:
            time.sleep(random.uniform(10, runtime_max_sec))
            driver.close()
        else:
            driver.close()

        # recursion for test
        self.runBot()


if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(description="Youtube Bot",
                                         prog='pqa',
                                         usage='%(prog)s [-h] [-v,--version]',
                                         )
        parser.add_argument('--threads',
                            default=1,
                            type=int,
                            nargs='?', help='Number of threads. Arg must be an int')

        parser.add_argument('--pro',
                            default=None,
                            nargs='?',
                            metavar='',
                            help='Chanel is a payed from youtube')

        parser.add_argument('--only_view',
                            default=None,
                            nargs='?',
                            metavar='',
                            help='Views without video runtime')

        parser.add_argument('--runtime_views',
                            default=None,
                            nargs='?',
                            metavar='',
                            help='Views with video runtime')

        parser.add_argument('--runtime',
                            default=70,
                            type=int,
                            nargs='?',
                            metavar='',
                            help='Max runtime for video views in percent')

        parser.add_argument('--url',
                            default=None,
                            nargs='?',
                            metavar='',
                            help='Video url')

        args = parser.parse_args()

        pro = args.pro
        only_view = args.only_view
        runtime_views = args.runtime_views
        runtime = args.runtime
        url = args.url
        workers = []

        YoutubeBot = ViewBot(pro=pro, only_view=only_view, runtime_views=runtime_views, runtime=runtime, url=url)
        YoutubeBot.runBot()

        for i in range(0,args.threads):
            YoutubeBot = ViewBot(pro=pro, only_view=only_view, runtime_views=runtime_views, runtime=runtime, url=url)
            YoutubeBot.start()
            workers.append(YoutubeBot)

        for worker in workers:
            worker.join()

        print("Done!")

    except KeyboardInterrupt:
        for worker in workers:
            worker.shutdown()