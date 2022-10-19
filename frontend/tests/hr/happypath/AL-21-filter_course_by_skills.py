from fileinput import close
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


#Run AL-21-LJPS-01.sql script

expected_titles= ['Skill Category', "Skill Desc", "Skill Id", "Skill Name", "Skill Status"] 
expected_values= ['Engineering Design Management', 'Generate 3D models using a variety of modelling software to represent characteristics of a real-world system', "3", "3D Modelling", "true"] 

class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome('/Applications/chromedriver2')


    def test_search_in_python_org(self):
        driver = self.driver

        #Navigate to courses.html
        driver.get("http://127.0.0.1:5500/frontend/users/hr/courses.html")

        '''CASE 1: See a list of courses corresponding to the searched course name '''

        #Search Course Name 
        searchCourseElem = driver.find_element(By.ID, "searchCourse")
        searchCourseElem.send_keys('manage')

        #assert that all course names have "manage"
        expected_courses= ["People Management", "Stakeholder Management"]
        expected_categories= ["Management", "Sales"]

        totalRows = driver.find_elements(By.XPATH,"//*[@id= 'display_course_table']/tr")
        rows_count = len(totalRows)
        for i in range(1,rows_count+1):
            actual_course= driver.find_element(By.XPATH,"//*[@id='display_course_table']/tbody/tr["+ str(i) +"]/td[1]") 
            actual_category= driver.find_element(By.XPATH,"//*[@id='display_course_table']/tbody/tr["+ str(i) +"]/td[2]") 
            assert actual_course.text == expected_courses[i-1]
            assert actual_category.text == expected_categories[i-1]

        clearSearchQueryBtn = driver.find_element(By.ID, "clearSearchQuery")
        clearSearchQueryBtn.click()


        '''CASE 2: Given skills when filtering then show a list of courses with the corresponding skill '''

        wait = WebDriverWait(driver, 10)
        filterBtn =  driver.find_element(By.ID, "filterBtn") 
   
        #Filter By Skill- Creative Thinking
        filterBtn.click()
        
        selectNoneBtn =  wait.until(EC.element_to_be_clickable((By.ID, 'selectNoneBtn')))
        selectNoneBtn.click()
        skillCheckCreativeThinking= wait.until(EC.element_to_be_clickable((By.ID, '1')))
        skillCheckCreativeThinking.click()
        closeFilterBtn=  wait.until(EC.element_to_be_clickable((By.ID, 'closeFilterBtn'))) 
        closeFilterBtn.click()

        #assert that skill name is Creative Thinking
        expected_course="Business Continuity Planning"
        expected_skill="Creative Thinking"

        actual_course= driver.find_element(By.XPATH,"//*[@id='display_course_table']/tbody/tr[1]/td[1]") 
        actual_skill= driver.find_element(By.XPATH,"//*[@id='display_course_table']/tbody/tr[1]/td[4]") 
        assert actual_course.text == expected_course
        assert actual_skill.text == expected_skill

        
        ''' CASE 3: Given unassigned when filtering then show a list of courses with unassigned skills'''

        #Filter By Skill- Unassigned
        filterBtn.click()
        selectNoneBtn =  wait.until(EC.element_to_be_clickable((By.ID, 'selectNoneBtn')))
        selectNoneBtn.click()
        skillCheckUnassigned =  wait.until(EC.element_to_be_clickable((By.ID, 'NA')))
        skillCheckUnassigned.click()
        closeFilterBtn.click()

        #assert that all are skills are empty
        expected_courses= ["People Management", "Stakeholder Management"]
        expected_skills= [" ", " "]

        totalRows = driver.find_elements(By.XPATH,"//*[@id= 'display_course_table']/tr")
        rows_count = len(totalRows)
        for i in range(1,rows_count+1):
            actual_course= driver.find_element(By.XPATH,"//*[@id='display_course_table']/tbody/tr["+ str(i) +"]/td[1]") 
            actual_skill= driver.find_element(By.XPATH,"//*[@id='display_course_table']/tbody/tr["+ str(i) +"]/td[4]") 
            assert actual_course.text == expected_courses[i-1]
            assert actual_skill.text == expected_skills[i-1]

        

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
