import argparse
import pymongo
from dotenv import dotenv_values
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import ChromeOptions, Keys
from selenium.webdriver.common.by import By


from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

config = dotenv_values(".env")
post_xpath = "//*[starts-with(@class, 'post_content')]"
post_text_xpath = "//*[starts-with(@class, 'wall_post_text')]"

if __name__ == '__main__':

    # get the path to chrome session to avoid auth in vk, all windows needs
    # to be closed
    # -------------------------------------------------------------------------
    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('-p', '--profile_path', help='path to chrome session '
                                                     'folder', required=True)
    args = parser.parse_args()

    # setting up options for selenium
    # -------------------------------------------------------------------------
    options = ChromeOptions()
    options.add_argument(f'--user-data-dir={args.profile_path}')
    driver = webdriver.Chrome(options=options)

    # setting up our DataBase
    # -------------------------------------------------------------------------
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")

    mydb = myclient["vk_group_parser"]
    mycol = mydb["wall_data"]

    # getting posts data from the wall of group
    # -------------------------------------------------------------------------

    # get the group's wall
    driver.get(config['GROUP_LINK'])

    # get posts data
    post = driver.find_element(By.CLASS_NAME, 'wall_post_text')
    post.click()

    for _ in range(10):
        try:
            post_content = driver.find_element(By.XPATH, '//*[@id="wl_post"]')
            post_text = post_content.find_element(By.CLASS_NAME, 'wall_post_text').text
            print(post_text)
            driver.implicitly_wait(50)
            try:
                element = WebDriverWait(driver, 50).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="wk_right_arrow"]'))
                )

                next_button = driver.find_element(By.XPATH, '//*[@id="wk_right_arrow"]')
                next_button.click()
            finally:
                pass


        except NoSuchElementException:
            post_text = 'No text founded'
            print(post_text)

    # for post in driver.find_elements(By.XPATH, post_xpath):
    #     post_text = post.find_element(By.CLASS_NAME, "wall_post_text").text
    #     replies = dict()
    #
    #     for post_reply in post.find_elements(By.CLASS_NAME, "reply_content"):
    #         try:
    #             reply_author = post_reply.find_element(By.CLASS_NAME,
    #                                                    'reply_author').text
    #         except NoSuchElementException:
    #             reply_author = 'None'
    #
    #         try:
    #             reply_text = post_reply.find_element(By.CLASS_NAME,
    #                                              'reply_text').text
    #         except NoSuchElementException:
    #             reply_text = 'None'
    #         replies.update({reply_author: reply_text})

        # mydict = {"post_text": post_text, "post_replies": replies}
        # print(post_text)
        # print('-------------------------------------------------------')
        # print(replies, end='\n\n')
        # x = mycol.insert_one(mydict)

    # XPath for every post on a downloaded wall
    # //*[starts-with(@class, 'post_content')]
    # XPath for wall of group
    # //*[@id="page_wall_posts"]
    # driver.quit()
