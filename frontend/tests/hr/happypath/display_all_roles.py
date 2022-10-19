import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

#TODO: Run sql test file
expected_roles= ["Chief Executive Officer/Managing Director/General Manager/Presid","Designer"]
expected_sectors= ["Engineering Services", "Engineering Services"]
expected_track=["General Management", "Engineering Design",]


class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome('/Applications/chromedriver2')


    def test_search_in_python_org(self):
        driver = self.driver

        driver.get("http://127.0.0.1:5500/frontend/users/hr/roles.html")
        
        for i in range(len(expected_roles),1):
            actual_role= driver.find_element(By.XPATH,"//*[@id='display_roles_table']/tbody/tr[" +str(i+1) + "]/td[1]")
            actual_sector= driver.find_element(By.XPATH,"//*[@id='display_roles_table']/tbody/tr[" +str(i+1) + "]/td[2]")
            actual_track=  driver.find_element(By.XPATH,"//*[@id='display_roles_table']/tbody/tr[" +str(i+1) + "]/td[3]") 

            assert actual_role.text == expected_roles[i]
            assert actual_sector.text == expected_sectors[i]
            assert actual_track.text == expected_track[i]

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
