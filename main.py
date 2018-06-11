import time
import helper
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


DRIVER_PATH = '/Users/weiming/PycharmProjects/chromedriver'
BBDC_WEBSITE = 'https://www.bbdc.sg'
DEFAULT_TIMEOUT = 5
WANT_SESSIONS = ['4', '5', '6']


def init_driver():
    chrome_driver = webdriver.Chrome(executable_path=DRIVER_PATH)
    chrome_driver.wait = WebDriverWait(chrome_driver, DEFAULT_TIMEOUT)
    return chrome_driver


def login(driver):
    print("start login")
    driver.get(BBDC_WEBSITE)

    # switch to frame
    frame = driver.find_element_by_id("login_style").find_element_by_tag_name("iframe")
    driver.switch_to_frame(frame)

    # key in username & password to login
    form = driver.find_element_by_tag_name("form")
    username = form.find_element_by_name("txtNRIC")
    pwd = form.find_element_by_name("txtPassword")
    login_btn = form.find_element_by_name("btnLogin")

    data = helper.read_config()
    username.clear()
    username.send_keys(data["username"])
    pwd.clear()
    pwd.send_keys(data["password"])
    login_btn.click()
    print("complete login")


def to_practical_test(driver):
    print("to practical test")
    # switch to left frame
    driver.switch_to_frame("leftFrame")

    # go to terms and conditions page
    a = driver.find_element_by_xpath("/html/body/table/tbody/tr/td/table/tbody/tr[11]/td[3]/a")
    a.click()
    driver.switch_to_default_content()


def agree_terms(driver):
    print("agree terms")
    # switch to main frame
    driver.switch_to_frame("mainFrame")

    # agree
    button = driver.find_element_by_xpath("/html/body/table/tbody/tr[7]/td[1]/center/table/tbody/tr[6]/td[1]/input")
    button.click()
    driver.switch_to_default_content()


def select_all(driver):
    print("select all")
    # switch to main frame
    driver.switch_to_frame("mainFrame")

    # select all months, all sessions, all days
    all_month_box = driver.find_element_by_name("allMonth")
    all_session_box = driver.find_element_by_name("allSes")
    all_days_box = driver.find_element_by_name("allDay")

    all_month_box.click()
    all_session_box.click()
    all_days_box.click()

    time.sleep(0.1)

    search_btn = driver.find_element_by_name("btnSearch")
    search_btn.click()
    driver.switch_to_default_content()


def find_available_slots(driver):
    print("find available slots")
    times = []

    # switch to main frame
    driver.switch_to_frame("mainFrame")

    # find slots
    radios = driver.find_elements_by_xpath("//input[@type='radio']")
    for radio in radios:
        td = radio.find_element_by_xpath('..')
        text = td.get_attribute("onmouseover")
        parts = text.split(",")
        session = parts[3]
        session = session.replace('"', '')
        if session in WANT_SESSIONS:
            current = helper.format_session(session, parts)
            times.append(current)

    return times


def send_email():
    print("send email")
    pass


if __name__ == "__main__":
    browser = init_driver()

    login(browser)

    to_practical_test(browser)

    agree_terms(browser)

    select_all(browser)

    sessions = find_available_slots(browser)

    browser.quit()

    if len(sessions) > 0:
        send_email()
    else:
        print("no wanted session")


