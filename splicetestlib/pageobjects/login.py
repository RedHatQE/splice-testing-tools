import pageobjects
from pageobjects import locators
from pageobjects import SE
from pageobjects.basepageelement import InputPageElement
from pageobjects.basepageelement import ButtonPageElement
from pageobjects.basepageobject import BasePageObject
from selenium.common.exceptions import NoSuchElementException

class UsernameElement(InputPageElement):
    locator = staticmethod(locators["login.username"])

class PasswordElement(InputPageElement):
    locator = staticmethod(locators["login.password"])

class SubmitButton(ButtonPageElement):
    locator = staticmethod(locators["login.submit"])

class LoginPageObject(BasePageObject):
    username = UsernameElement()
    password = PasswordElement()
    submit_button = SubmitButton()

    def __init__(self):
        try:
            # are we already there?
            self.assertEqual("Signo", SE.title)
        except AssertionError as e:
            SE.get(SE.current_url + u"/signo")
            self.assertEqual("Signo", SE.title)

    def submit(self):
        # assumes successful log-in by the Sign "Out link" presence
        self.submit_button.click()
        SE.refresh()
        self.assertIn(locators['login.logout'], SE)
