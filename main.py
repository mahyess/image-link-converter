import csv, requests, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from helpers.user_agent import random_user_agent

from pyvirtualdisplay import Display


with open("__all__.csv") as reader, open("__all__ updated.csv", "w") as writer:
    reader = csv.DictReader(reader)
    writer = csv.DictWriter(writer, fieldnames=reader.fieldnames)
    writer.writeheader()
    for count, row in enumerate(reader):
        while True:
            try:
                display = Display(visible=0, size=(1300, 700))
                display.start()
                print(f"count: {count} starting")
                options = Options()
                options.add_argument("--no-sandbox")
                options.add_argument(f"user-agent={random_user_agent()}")
                options.add_argument("window-size=1300x700")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--headless")
                driver = webdriver.Chrome(options=options)
                driver.implicitly_wait(2)
                driver.get("https://im.ge/upload")
                driver.find_element_by_css_selector(
                    f"a[data-target='anywhere-upload-paste-url']"
                ).click()

                ActionChains(driver).move_to_element(
                    driver.find_element_by_tag_name("form")
                ).click(
                    driver.find_element_by_css_selector(f"textarea[name='urls']")
                ).send_keys(
                    row["photo"]
                ).perform()

                driver.find_element_by_class_name("btn-input").click()

                # driver.find_element_by_css_selector(
                #     f"a[class='cookie-law-close']"
                # ).click()

                # ActionChains(driver).move_to_element(
                #     driver.find_element_by_css_selector(f"button[data-action='upload']")
                # ).click(
                #     driver.find_element_by_css_selector(f"button[data-action='upload']")
                # ).perform()

                driver.find_element_by_css_selector(
                    f"button[data-action='upload']"
                ).click()

                WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located(
                        (By.CSS_SELECTOR, "textarea[id='uploaded-embed-code-0']")
                    )
                )
                new_link = driver.find_element_by_css_selector(
                    "textarea[id='uploaded-embed-code-0']"
                ).get_attribute("value")
                print(new_link)

                row["photo"] = new_link
                writer.writerow(row)
                break
            except Exception as e:
                print(e)
            finally:
                driver.quit()
                display.stop()
