# Page Objects
from pageobjects.seleniumwrapper import SeleniumWrapper

SE = SeleniumWrapper()

locators = {
    "login.username": lambda : SE.find_element_by_name("username"),
    "login.password": lambda : SE.find_element_by_name("password"),
    "login.submit": lambda : SE.find_element_by_name("commit"),
    "login.logout": lambda : SE.find_element_by_link_text("logout")
}

