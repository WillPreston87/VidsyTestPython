import unittest
from Locators import * # Todo later
import time
from Credentials import *
from selenium import webdriver

driver = webdriver.Chrome()

# Functions

def CheckPage(self, Page):
    # This is a function to detect which page to check is correct
    print("Checking page: '{}'...".format(Page))
    if Page == "Log In":
        CheckLogInPage(self)
    elif Page == "Brand Select":
        CheckBrandSelectPage(self)
    elif Page == "Brief":
        CheckBriefPage(self)

def CheckLogInPage(self):
    # This is a function to check that the Log In page appears correctly
    try:
        self.driver.find_element_by_class_name("avatar__thumbnail")
        self.driver.find_element_by_name("email")
        self.driver.find_element_by_name("password")
        return True
    except:
        print("Log In Page does not appear correctly")
        return False

def CheckBrandSelectPage(self):
    # This is a function to check that the Brand Select page appears correctly
    try:
        self.driver.find_element_by_class_name("brand-selector__close-button")
        self.driver.find_element_by_class_name("brand-card")
    except:
        print("Brand Select Page does not appear correctly")


def  CheckBriefPage(self):
    # This is a function to check that the Brief page appears correctly
    try:
        self.driver.find_element_by_class_name("avatar__thumbnail")
        self.driver.find_element_by_partial_link_text("/settings")
        self.driver.find_element_by_xpath("//button[contains(.,'Log out']")
        self.driver.find_element_by_class_name("sub-navigation__button ui-link is-interactive")
        self.driver.find_element_by_class_name("create-campaign-card")
    except:
        print("Brief Page does not appear correctly")

def LogInAccount(self, Username, Password):
    # This is a function to attempt a log in
    CheckPage(self, "Log In")
    EMAIL_FORM = self.driver.find_element_by_name("email")
    PASSWORD_FORM = self.driver.find_element_by_name("password")
    print("Attempting to log into {} account with {} password...".format(Username, Password))
    if Username == "Registered":
        EMAIL_FORM.send_keys(login_creds["username"])
    elif Username == "Unregistered":
        EMAIL_FORM.send_keys(login_creds["wrong_username"])
    elif Username == "Invalid":
        EMAIL_FORM.send_keys(login_creds["invalid_username"])
    if Password == "Correct":
        PASSWORD_FORM.send_keys(login_creds["password"])
    elif Password == "Incorrect":
        PASSWORD_FORM.send_keys(login_creds["wrong_password"])
    LOG_IN_BUTTON = self.driver.find_element_by_class_name("login__button")
    LOG_IN_BUTTON.click()
    time.sleep(3)
    if CheckLoggedIn(self):
        print("Successfully logged in with account")
        return True
    else:
        print("Log in failed")
        return False

def SelectBrand(self, Brand):
    # This is a function to select a brand and check that is selected correctly
    CheckPage(self, "Brand Select")
    print("Selecting brand: {}".format(Brand))
    self.driver.find_element_by_xpath("//button[@class='brand-card' and contains(.,'{}')]".format(Brand)).click()
    BRAND_NAME = self.driver.find_element_by_class_name("navigation__current-info")
    brandname = BRAND_NAME.text
    if Brand == brandname:
        print("{} selected successfully".format(Brand))
    else:
        print("Wrong brand selected. {} selected instead of {}".format(brandname, Brand))

def CheckLoggedIn(self):
    # This is a function to check that a log in attempt as been successful
    try:
        CheckLogInPage(self)
        return False
    except:
        return True

def CountBriefs(self):
    # This is a function that counts the amount of briefs on the brief page
    time.sleep(5)
    Briefs = self.driver.find_elements_by_class_name("brief-card")
    return len(Briefs)

def CheckBriefs(self):
    # This is a function that prints back the text in the briefs as a way of verifying they exist
    BriefCount = CountBriefs(self)
    print("Number of Briefs: {}".format(BriefCount))
    if BriefCount != 0:
        BriefText = self.driver.find_element_by_class_name("container-fluid").text
        print(BriefText)
        return True
    else:
        return False

class VidsyTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://app.staging.vidsy.co/login")

    def tearDown(self):
        self.driver.close()

    def test_1_Log_Into_Vidsy_Brand(self):
        # Scenario: This test is to see if i can log into the Vidsy platform with valid user credentials and select the Vidsy brand
        # GIVEN I have a registered account on the Vidsy platform
        # WHEN I enter valid user credentials on the log in page
        # AND I select Vidsy as my chosen brand
        # THEN the brief page for Vidsy is displayed correctly
        # AND a list of briefs are displayed
        print("********** RUNNING TEST 1: LogIntoVidsyBrand **********")
        LogInAccount(self, "Registered", "Correct")
        SelectBrand(self, "Vidsy")
        if CheckBriefs(self):
            print("********** TEST 1 PASSED: LogIntoVidsyBrand **********")
        else:
            print("********** TEST 1 FAILED: LogIntoVidsyBrand **********")

    def Test_2_Log_Into_Listerine_Brand(self):
        # Scenario: This test is to see if i can log into the Vidsy platform with valid user credentials and select the Listerine brand
        # GIVEN I have a registered account on the Listerine platform
        # WHEN I enter valid user credentials on the log in page
        # AND I select Listerine as my chosen brand
        # THEN the brief page for Listerine is displayed correctly
        # AND a list of briefs are displayed
        print("********** RUNNING TEST 2: LogIntoListerineBrand **********")
        LogInAccount(self, "Registered", "Correct")
        SelectBrand(self, "Listerine")
        if CheckBriefs(self):
            print("********** TEST 2 PASSED: LogIntoListerineBrand **********")
        else:
            print("********** TEST 2 FAILED: LogIntoListerineBrand **********")

    def Test_3_Unable_To_Login_With_Unregistered_Email(self):
        # Scenario: This test is to see that I am unable to log into Vidsy with an unregistered email
        # GIVEN I don't have a registered account on the Vidsy platform
        # WHEN I enter unregistered user credentials on the log in page
        # THEN I am unable to log in
        print("********** RUNNING TEST 3: UnableToLoginWithUnregisteredEmail **********")
        if LogInAccount(self,"Unregistered", "Correct"):
            print("********** TEST FAILED: UnableToLoginWithInvalidEmail **********")
        else:
            print("********** TEST 3 PASSED: UnableToLoginWithUnregisteredEmail **********")

    def Test_4_Unable_To_Login_With_Incorrect_Password(self):
        # Scenario: This test is to see that I am unable to log into Vidsy with an invalid email
        # GIVEN I have a registered account on the Vidsy platform
        # WHEN I enter a registered email on the log in page
        # AND I enter the incorrect password for that registered email
        # THEN I am unable to log in
        print("********** RUNNING TEST 4: UnableToLoginWithUnregisteredEmail **********")
        if LogInAccount(self, "Registered", "Incorrect"):
            print("********** TEST 4 FAILED: UnableToLoginWithInvalidEmail **********")
        else:
            print("********** TEST 4 PASSED: UnableToLoginWithUnregisteredEmail **********")

    def Test_5_Unable_To_Login_With_Invalid_Email(self):
        # Scenario: This test is to see that I am unable to log into Vidsy with an unregistered email
        # GIVEN I don't have a registered account on the Vidsy platform
        # WHEN I enter an invalid email on the log in page
        # AND a valid password
        # THEN I am unable to log in
        # AND a message appears saying the email is invalid
        print("********** RUNNING TEST 5: UnableToLoginWithUnregisteredEmail **********")
        if LogInAccount(self, "Invalid", "Incorrect"):
            print("********** TEST 5 FAILED: UnableToLoginWithInvalidEmail **********")
        else:
            print("********** TEST 5 PASSED: UnableToLoginWithUnregisteredEmail **********")

if __name__ == "__main__":
    test_loader = unittest.TestLoader()

    test_names = test_loader.getTestCaseNames(VidsyTest)
    # ****************************************************
    # Enter test name below to run
    test_names = ["test_1_Log_Into_Vidsy_Brand"]

    # test_names = [
    # test_1_Log_Into_Vidsy_Brand
    # Test_2_Log_Into_Listerine_Brand
    # Test_3_Unable_To_Login_With_Unregistered_Email
    # Test_4_Unable_To_Login_With_Incorrect_Password
    # Test_5_Unable_To_Login_With_Invalid_Email
    suite = unittest.TestSuite()
    for test_name in test_names:
        suite.addTest(VidsyTest(test_name))

    result = unittest.TextTestRunner().run(suite)
