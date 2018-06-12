import time
import helper
import mail
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

CHROME_PATH = "chrome_path"
BBDC_WEBSITE = 'https://www.bbdc.sg'
DEFAULT_TIMEOUT = 5

# config keys
BBDC = "bbdc"
USERNAME = "username"
PASSWORD = "password"
GMAIL = "gmail"
EMAIL = "email"
ALL_SESSIONS = "all_sessions"
WANT_SESSIONS = "want_sessions"


def init_driver(path):
    chrome_driver = webdriver.Chrome(executable_path=path)
    chrome_driver.wait = WebDriverWait(chrome_driver, DEFAULT_TIMEOUT)
    return chrome_driver


def login(driver, username, password):
    print("start login")
    driver.get(BBDC_WEBSITE)

    # switch to frame
    frame = driver.find_element_by_id("login_style").find_element_by_tag_name("iframe")
    driver.switch_to_frame(frame)

    # key in username & password to login
    form = driver.find_element_by_tag_name("form")
    nric = form.find_element_by_name("txtNRIC")
    pwd = form.find_element_by_name("txtPassword")
    login_btn = form.find_element_by_name("btnLogin")

    nric.clear()
    nric.send_keys(username)
    pwd.clear()
    pwd.send_keys(password)
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


def find_available_slots(driver, want_sessions):
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
        if session in want_sessions:
            current = helper.format_session(session, parts)
            times.append(current)

    return times


if __name__ == "__main__":
    config = helper.read_config()

    browser = init_driver(config[CHROME_PATH])

    login(browser, config[BBDC][USERNAME], config[BBDC][PASSWORD])

    to_practical_test(browser)

    agree_terms(browser)

    select_all(browser)

    slots = find_available_slots(browser, config[WANT_SESSIONS])

    browser.quit()

    if len(slots) > 0:
        subject = "Book BBDC Practical Session"
        msg = "all available sessions: \n"
        for slot in slots:
            msg += slot + "\n"

        email = config[GMAIL][EMAIL]
        pwd = config[GMAIL][PASSWORD]
        mail.send(email, pwd, email, subject, msg)
    else:
        print("no wanted session")


