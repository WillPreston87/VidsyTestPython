import unittest
import logging
from Locators import *
from Credentials import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Functions

def CheckPage(Page):
    # This is a function to detect which page to check is correct
    print("Checking page: '{}'...".format(Page))
    if Page == "Log In":
        CheckLogInPage()
    elif Page == "Brand Select":
        CheckBrandSelectPage()
    elif Page == "Brief":
        CheckBriefPage()

def CheckLogInPage():
    # This is a function to check that the Log In page appears correctly
    try:
        validatePresent(LogInPage.EMAIL_FORM)
        validatePresent(LogInPage.PASSWORD_FORM)
        validatePresent(LogInPage.LOG_IN_BUTTON)
        validatePresent(LogInPage.LOGO)
        return True
    except:
        logging.ERROR("Log In Page does not appear correctly")
        return False

def CheckBrandSelectPage():
    # This is a function to check that the Brand Select page appears correctly
    try:
        validatePresent(BrandSelectPage.CLOSE_BUTTON)
        validatePresent(BrandSelectPage.BRAND_BUTTON)
    except:
        logging.ERROR("Brand Select Page does not appear correctly")


def  CheckBriefPage():
    # This is a function to check that the Brief page appears correctly
    try:
        validatePresent(BriefPage.VIDSY_LOGO_BUTTON)
        validatePresent(BriefPage.ACCOUNT_BUTTON)
        validatePresent(BriefPage.LOG_OUT_BUTTON)
        validatePresent(BriefPage.CREATE_BRIEF_BUTTON)
        validatePresent(BriefPage.CREATE_BRIEF_CARD)
    except:
        logging.ERROR("Brief Page does not appear correctly")

def LogInAccount(Username, Password):
    # This is a function to attempt a log in
    CheckPage("Log In")
    logging.INFO("Attempting to log into" + Username + " account with " + Password + " password...")
    if Username == "Registered":
        driver.findElement(By.name("email")).sendKeys(login_creds["username"])
    elif Username == "Unregistered":
        driver.findElement(By.name("email")).sendKeys(login_creds["wrong_username"])
    elif Username == "Invalid":
        driver.findElement(By.name("email")).sendKeys(login_creds["invalid_username"])
    if Password == "Correct":
        driver.findElement(By.name("password")).sendKeys(login_creds["password"])
    elif Password == "Incorrect":
        driver.findElement(By.name("password")).sendKeys(login_creds["wrong_password"])
        click(LogInPage.LOG_IN_BUTTON)
    if CheckLoggedIn():
        logging.INFO("Successfully logged in with account")
        return True
    else:
        logging.ERROR("Log in failed")
        return False

def SelectBrand(Brand):
    # This is a function to select a brand and check that is selected correctly
    CheckPage("Brand Select")
    logging.INFO("Selecting brand: {}".format(Brand))
    driver.findElement(By.xpath("//button[@class='brand-card' and contains(.,'{}')]".format(Brand))).click()
    brandname = getText.BriefPage.BRAND_NAME
    if Brand == getText.BriefPage.BRAND_NAME:
        logging.INFO(Brand + "selected successfully")
    else:
        logging.ERROR("Wrong brand selected. {} selected instead of {}".format(brandname, Brand))

def CheckLoggedIn():
    # This is a function to check that a log in attempt as been successful
    try:
        CheckLogInPage()
        return False
    except:
        return True

def CountBriefs():
    # This is a function that counts the amount of briefs on the brief page
    driver.manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS)
    List<WebElement> Briefs = driver.findElements(By.className("brief-card"))
    return len(Briefs)

def CheckBriefs():
    # This is a function that prints back the text in the briefs as a way of verifying they exist
    BriefCount = CountBriefs()
    logging.INFO("Number of Briefs: {}".format(BriefCount))
    if BriefCount != 0:
        BriefText = getText(By.className("container-fluid"))
        logging.INFO(BriefText)
        return True
    else:
        return False

class VidsyTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://app.staging.vidsy.co/login")

    def tearDown(self):
        self.driver.quit()

    def test_1_Log_Into_Vidsy_Brand(self):
        # Scenario: This test is to see if i can log into the Vidsy platform with valid user credentials and select the Vidsy brand
        # GIVEN I have a registered account on the Vidsy platform
        # WHEN I enter valid user credentials on the log in page
        # AND I select Vidsy as my chosen brand
        # THEN the brief page for Vidsy is displayed correctly
        # AND a list of briefs are displayed
        logging.INFO("********** RUNNING TEST 1: LogIntoVidsyBrand **********")
        LogInAccount("Registered", "Correct")
        SelectBrand("Vidsy")
        if CheckBriefs():
            logging.INFO("********** TEST 1 PASSED: LogIntoVidsyBrand **********")
        else:
            logging.ERROR("********** TEST 1 FAILED: LogIntoVidsyBrand **********")

    def Test_2_Log_Into_Listerine_Brand(self):
        # Scenario: This test is to see if i can log into the Vidsy platform with valid user credentials and select the Listerine brand
        # GIVEN I have a registered account on the Listerine platform
        # WHEN I enter valid user credentials on the log in page
        # AND I select Listerine as my chosen brand
        # THEN the brief page for Listerine is displayed correctly
        # AND a list of briefs are displayed
        logging.INFO("********** RUNNING TEST 2: LogIntoListerineBrand **********")
        LogInAccount("Registered", "Correct")
        SelectBrand("Listerine")
        if CheckBriefs():
            logging.INFO("********** TEST 2 PASSED: LogIntoListerineBrand **********")
        else:
            logging.ERROR("********** TEST 2 FAILED: LogIntoListerineBrand **********")

    def Test_3_Unable_To_Login_With_Unregistered_Email(self):
        # Scenario: This test is to see that I am unable to log into Vidsy with an unregistered email
        # GIVEN I don't have a registered account on the Vidsy platform
        # WHEN I enter unregistered user credentials on the log in page
        # THEN I am unable to log in
        logging.INFO("********** RUNNING TEST 3: UnableToLoginWithUnregisteredEmail **********")
        if LogInAccount("Unregistered", "Correct"):
            logging.ERROR("********** TEST FAILED: UnableToLoginWithInvalidEmail **********")
        else:
            logging.INFO("********** TEST 3 PASSED: UnableToLoginWithUnregisteredEmail **********")

    def Test_4_Unable_To_Login_With_Incorrect_Password(self):
        # Scenario: This test is to see that I am unable to log into Vidsy with an invalid email
        # GIVEN I have a registered account on the Vidsy platform
        # WHEN I enter a registered email on the log in page
        # AND I enter the incorrect password for that registered email
        # THEN I am unable to log in
        logging.INFO("********** RUNNING TEST 4: UnableToLoginWithUnregisteredEmail **********")
        if LogInAccount("Registered", "Incorrect"):
            logging.ERROR("********** TEST 4 FAILED: UnableToLoginWithInvalidEmail **********")
        else:
            logging.INFO("********** TEST 4 PASSED: UnableToLoginWithUnregisteredEmail **********")

    def Test5UnableToLoginWithInvalid(self):
        # Scenario: This test is to see that I am unable to log into Vidsy with an unregistered email
        # GIVEN I don't have a registered account on the Vidsy platform
        # WHEN I enter an invalid email on the log in page
        # AND a valid password
        # THEN I am unable to log in
        # AND a message appears saying the email is invalid
        logging.INFO("********** RUNNING TEST 5: UnableToLoginWithUnregisteredEmail **********")
        if LogInAccount("Invalid", "Incorrect"):
            logging.ERROR("********** TEST 5 FAILED: UnableToLoginWithInvalidEmail **********")
        else:
            logging.INFO("********** TEST 5 PASSED: UnableToLoginWithUnregisteredEmail **********")

if __name__ == "__main__":
    unittest.main()
