import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

#TODO: Run sql test file

#tentative -- to change when test.db is setup.
expected_titles= ['Role Desc', "Role Id", "Role Name", "Role Sector", "Roles Status", "Role Track"] 
expected_values= ['The Chief Executive Officer/Chief Operating Officer/Managing Director/General Manager/President defines the long-term strategic direction to grow the business in line with the organisation’s overall vision, mission and values. He/She translates broad goals into achievable steps, anticipates and stays ahead of trends, and takes advantage of business opportunities. He represents the organisation with customers, investors, and business partners, and holds responsibility for fostering a culture of workplace saf',
 '2', 
 "Chief Executive Officer/Managing Director/General Manager/Presid", 
 "Engineering Services",
 "true",
 "General Management"] 

class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome('/Applications/chromedriver2')


    def test_search_in_python_org(self):
        driver = self.driver

        #Navigate to skill.html
        driver.get("http://127.0.0.1:5500/frontend/users/hr/roles.html")

        #Click Show Details Button
        elem = driver.find_element(By.NAME, "show_details")
        elem.click()

        #check single skill detail of the first skill    
        totalRows = driver.find_elements(By.XPATH,"//*[@id= 'single_role_table']/tr")
        rows_count = len(totalRows)
        for i in range(1,rows_count+1):
            actual_title= driver.find_element(By.XPATH,"//*[@id='single_role_table']/tbody/tr["+ str(i) +"]/td[1]") 
            actual_value= driver.find_element(By.XPATH,"//*[@id='single_role_table']/tbody/tr["+ str(i) +"]/td[2]") 
            assert actual_title.text == expected_titles[i-1]
            assert actual_value.text == expected_values[i-1]

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()