# Page Objects
from selenium_wrapper import SE

locators = {
    "login.username": lambda : SE.find_element_by_name("username"),
    "login.password": lambda : SE.find_element_by_name("password"),
    "login.submit": lambda : SE.find_element_by_name("commit"),
    "login.logout": lambda : SE.find_element_by_link_text("logout")
    "login.logout_notice": lambda: SE.find_element_by_xpath("//li[text()='You have been logged out']")
}

