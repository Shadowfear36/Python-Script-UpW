from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

import os
from twilio.rest import Client

userEmail = os.environ["UPWORK_USER"]
userPass = os.environ["UPWORK_PASS"]
account_sid = os.environ["TWILIO_ACC_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]

#Twilio
client = Client(account_sid, auth_token)

#Selenium
options = Options()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 10)

#Load Upwork
driver.get("https://www.upwork.com/ab/account-security/login?redir=%2Fnx%2Ffind-work%2F")
driver.maximize_window()


#Login
emailInput = driver.find_element(By.ID, "login_username")
emailInput.send_keys(userEmail)

signupBtnNxt = driver.find_element(By.ID, "login_password_continue")
signupBtnNxt.click()

#Wait until page has loaded to search for Input
passInput = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input#login_password.up-input")))
passInput.send_keys(userPass)

loginBtn = driver.find_element(By.ID, "login_control_continue")
loginBtn.click()

jobsPage = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="caret-btn-findWorkHome"]/span[1]')))
jobsPage.click()

#navigate to most recent jobs
driver.get('https://www.upwork.com/nx/find-work/most-recent')

#Grab Search Input
searchInput = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Search for job"]')))
searchButton = wait.until(EC.presence_of_element_located((By.XPATH, '//button[@data-test="job-search-button"]')))
def search(search_input, search_term, search_button ):
    search_input.send_keys(search_term)
    search_button.click()

search(searchInput, "shopify", searchButton)

scrapedJobs=[]
def scrapeContent():
    jobPostsContainer = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@data-test="job-tile-list"]')))
    sections = jobPostsContainer.find_elements(By.XPATH, '//section[@data-test="JobTile"]')
    for section in sections:
        title = section.find_element(By.XPATH, './/a[@data-test="UpLink"]')
        link = title.get_attribute('href')
        # link = link.replace('http://', 'hxxp://').replace('https://', 'hxxps://')
        scrapedJobs.append([title, link])



    print(scrapedJobs[0][0])

    message = client.messages.create(
        to="+15597599410",
        from_="+18776189646",
        body=scrapedJobs[0][0],
        media_url=[scrapedJobs]
    )

    print(message.sid)

scrapeContent()




# def scrapeContent():
#     jobPostsContainer = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@data-test="job-tile-list"]')))
#     sections = jobPostsContainer.find_elements(By.XPATH, './/section[@class="up-card-section up-card-list-section up-card-hover"]')
#     for section in sections:
#         # budget = section.find_element(By.XPATH, './/span[@data-test="budget"]')
#         titleTag = section.find_element(By.XPATH, './/div[@class="row my-10"]/div[@class="col"]/h3')
#         title = titleTag.text
#         print(title)
#
#         budgetTag = section.find_element(By.XPATH, './/div[@class="mb-10"]/div/small[@class="text-muted display-inline-block text-muted"]/span/span[@data-test="budget"]')
#         # budgetSecParent = budgetParent.find_element(By.CLASS_NAME, 'row')
#         print(budgetTag)
#
#
# scrapeContent()



