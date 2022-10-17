import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

#TODO : Create test.db and replace expected values 

#tentative -- to change when test.db is setup.
expected_titles= ['Skill Category', "Skill Desc", "Skill Id", "Skill Name", "Skill Status"] 
expected_values= ['Engineering Design Management', 'Generate 3D models using a variety of modelling software to represent characteristics of a real-world system', "3", "3D Modelling", "true"] 

class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome('/Applications/chromedriver2')


    def test_search_in_python_org(self):
        driver = self.driver

        #Navigate to skill.html
        driver.get("http://127.0.0.1:5500/frontend/users/hr/skills.html")
        
        #Click Show Details Button
        elem = driver.find_element(By.NAME, "show_details")
        elem.click()
            
        #check single skill detail of the first skill    
        totalRows = driver.find_elements(By.XPATH,"//*[@id= 'single_skill_table']/tr")
        rows_count = len(totalRows)
        for i in range(1,rows_count+1):
            actual_title= driver.find_element(By.XPATH,"//*[@id='single_skill_table']/tbody/tr["+ str(i) +"]/td[1]") 
            actual_value= driver.find_element(By.XPATH,"//*[@id='single_skill_table']/tbody/tr["+ str(i) +"]/td[2]") 
            assert actual_title.text == expected_titles[i-1]
            assert actual_value.text == expected_values[i-1]

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
