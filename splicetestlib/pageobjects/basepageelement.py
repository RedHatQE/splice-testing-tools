# Base Page Element
import splicetestlib.pageobjects
from splicetestlib.pageobjects import SE

class BasePageElement(object):
    locator = staticmethod(lambda : None)

    def __get__(self, obj, cls=None):
        return self.locator()

    def __delete__(self, obj):
        pass

class InputPageElement(BasePageElement):
    def __set__(self, obj, value):
        self.__get__(obj).send_keys(value)

class ButtonPageElement(BasePageElement):
    def click(self):
        self.__get__(obj).click()
