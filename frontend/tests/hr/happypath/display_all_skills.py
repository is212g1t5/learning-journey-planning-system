import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

#TODO : Create test.db and replace expected values 

#tentative -- to change when test.db is setup.
expected_skills= ["Creative Thinking", "Front-End Engineering and Design", "3D Modelling"]
expected_category= ["Thinking Critically", "Engineering Design Management", "Engineering Design Management"]


class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome('/Applications/chromedriver2')


    def test_search_in_python_org(self):
        driver = self.driver

        #Navigate to skill.html
        driver.get("http://127.0.0.1:5500/users/hr/skills.html")

        #check  
        for i in range(len(expected_skills)):
       
            actual_skill= driver.find_element(By.XPATH,"//*[@id='display_skills_table']/tbody/tr[" +str(i+1) + "]/td[1]/div")
            actual_category= driver.find_element(By.XPATH,"//*[@id='display_skills_table']/tbody/tr[" + str(i+1)+ "]/td[2]/div") 
            assert actual_skill.text == expected_skills[i]
            assert actual_category.text == expected_category[i]
    
           

       

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
