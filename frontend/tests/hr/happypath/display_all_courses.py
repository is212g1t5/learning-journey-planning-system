import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

#TODO : Create test.db and replace expected values 

#tentative -- to change when test.db is setup.
expected_course= ["Business Continuity Planning", "Risk and Compliance Reporting", "Systems Thinking and Design"]
expected_category= ["Finance", "Finance", "Core"]


class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome('Applications/chromedriver2')


    def test_search_in_python_org(self):
        driver = self.driver

        #Navigate to course.html
        driver.get("http://127.0.0.1:8000/users/hr/courses.html")

        #check  
        for i in range(len(expected_course)):
            actual_course= driver.find_element(By.XPATH,"//*[@id='display_courses_table']/tbody/tr[" +str(i+1) + "]/td[1]/div")
            actual_category= driver.find_element(By.XPATH,"//*[@id='display_courses_table']/tbody/tr[" + str(i+1)+ "]/td[2]/div") 
            assert actual_course.text == expected_course[i]
            assert actual_category.text == expected_category[i]

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
