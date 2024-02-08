from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
import json
# from time import sleep



def scanData(URL, GAMES):
    driver = webdriver.Chrome('/Users/NoahM/-1Downloads/chromedriver')
    driver.get(URL)

    #above 18 and TOS, enter site
    for element in driver.find_elements(By.XPATH, "//*[@type='checkbox']"):
        element.click()

    driver.find_element(By.XPATH, "//*[@*='enter-button pointer']").click()

    #reenter url after cookies because site reduces url
    driver.get(URL)

    # steam_id = URL[30 : URL.find("/history/")]
    # WebDriverWait(driver, 5).until_not(expected_conditions.text_to_be_present_in_element_value((By.XPATH, f"//*[@href='https://steamcommunity.com/profiles/{steam_id}']/steam-id[text()]"), "Loading..."))
    # USERNAME = driver.find_element(By.XPATH, "//*[@href='https://steamcommunity.com/profiles/{steam_id}']/steam-id[text()]").get_attribute("textContent").strip()
    

    found = 0
    winnings = []
    while (found < GAMES or GAMES < 0):
        #selects all rows and takes prices
        for price_element in driver.find_elements(By.XPATH, "//*[@*='xd-row' and @tabindex]/*[last()]/*[text()]"):
            winnings.append(price_element.get_attribute("textContent").strip())
            found += 1
            if (found >= GAMES and GAMES > 0):
                break
        else:
            try:
                driver.find_element(By.XPATH, "//*[@class='page-item']/*[@href and @class='page-link' and @aria-label='Next']").click()
                #waits until last element of data to go stale meaning next page is loaded
                try:
                    WebDriverWait(driver, 5).until(expected_conditions.staleness_of(price_element))
                except Exception as e:
                    print (f"there was an issue loading the page: \n {e}")
                    driver.close()
                    return
            except NoSuchElementException:
                print ("not enough games on record for requested report, all games are included in report")
                break

    driver.close()

    i = 0
    while (True):
        try:
            out_file = open("winnings_report" + f"_{i}", "x")
            # out_file = open(USERNAME + "_report_" + f"_{i}", "x")
            break
        except FileExistsError:
            i += 1

    json.dump(winnings, out_file)
    out_file.close()

if (__name__ == "__main__"):
    # GAMES = 52
    GAMES = int(input("how many games to search?(negative for all games): "))
    URL = 'https://www.wtfskins.com/user/76561198401513516/history/crash/1'
    scanData(URL, GAMES)