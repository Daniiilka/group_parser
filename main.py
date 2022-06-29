import argparse
import json

import pymongo
from dotenv import dotenv_values
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import ChromeOptions, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

config = dotenv_values()


if __name__ == "__main__":

    # get the path to chrome session to avoid auth in vk, all windows need
    # to be closed
    # -------------------------------------------------------------------------
    parser = argparse.ArgumentParser(description="Description of your program")
    parser.add_argument(
        "-p",
        "--profile_path",
        help="path to chrome session " "folder",
        required=True,
    )
    # we can also save data in MongoDB or in json file if required
    parser.add_argument(
        "-m",
        "--storage",
        help="arg to save data in nongo database or in json file",
        required=True,
        choices=["mongo", "json"],
    )
    args = parser.parse_args()

    # setting up options for selenium
    # -------------------------------------------------------------------------
    options = ChromeOptions()
    options.add_argument(f"--user-data-dir={args.profile_path}")
    # options.headless = True
    driver = webdriver.Chrome(options=options)

    # setting up our DataBase if we use MongoDB
    # -------------------------------------------------------------------------
    if args.storage == "mongo":
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["vk_group_parser"]
        mycol = mydb["wall_data"]

    # getting posts data from the wall of group
    # -------------------------------------------------------------------------

    # get the group's wall
    driver.get(config["GROUP_LINK"])

    # get posts data
    post = driver.find_element(By.CLASS_NAME, "wall_post_text")
    post.click()

    while True:
        # try to upload single post and get text
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="wl_post"]')
                )
            )
            post_content = driver.find_element(By.XPATH, '//*[@id="wl_post"]')
        except NoSuchElementException:
            driver.quit()
            print("done!")
            break
        post_text = []

        try:
            post_text.append(
                post_content.find_element(By.CLASS_NAME, "wall_post_text").text
            )
        except NoSuchElementException:
            try:
                post_text.append(
                    post_content.find_element(
                        By.XPATH,
                        "//*[starts-with(@id, 'post_media_lnk')]/a[2]",
                    ).get_attribute("href")
                )
            except NoSuchElementException:
                try:
                    post_text.append(
                        post.find_element(
                            By.XPATH,
                            '//*[starts-with(@class, "article_snippet")]',
                        ).get_attribute("href")
                    )
                except NoSuchElementException:
                    post_text = None

        # if photo exists -> click on it and get a link ->
        # -> pressing ESC button to continue scrolling of posts
        try:
            driver.find_element(
                By.XPATH, '//*[starts-with(@id, "wpt")]/div[2]/div/a'
            ).click()
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//*[@id='pv_photo']")
                )
            )

            post_photo = driver.find_element(
                By.XPATH, '//*[@id="pv_photo"]/img'
            ).get_attribute("src")
            webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

        except NoSuchElementException:
            post_photo = None

        # getting the list of replies and parse {author: text_of_reply}
        replies = dict()
        if post_content.find_elements(By.CLASS_NAME, "reply_content"):

            for reply in post_content.find_elements(
                By.CLASS_NAME, "reply_content"
            ):
                reply_author = reply.find_element(
                    By.CLASS_NAME, "reply_author"
                ).text
                reply_text = reply.find_element(
                    By.CLASS_NAME, "reply_text"
                ).text
                replies.update({reply_author: reply_text})

        # filling row in the dictionary
        mydict = {
            "post_text": post_text,
            "post_photo": post_photo,
            "post_replies": replies,
        }

        # insert data into database if we're using MongoDB or
        # dump data into JSON file
        if args.storage == "mongo":
            mycol.insert_one(mydict)
        else:
            with open("sample.json", "a+", encoding="utf-8") as outfile:
                json.dump(mydict, outfile, ensure_ascii=False)

        # setting up waiting for a changes in the URL link
        old_url = driver.current_url
        driver.find_element(By.XPATH, '//*[@id="wk_right_arrow"]').click()
        WebDriverWait(driver, 10).until(
            lambda driver: driver.current_url != old_url
        )
