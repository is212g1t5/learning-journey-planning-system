# learning-journey-planning-system

This is a project aimed to allow its users to plan their career progression. The system is aimed to allow user to gain skills in accordance to courses offered by the internal company's Learning Management System.

## Project / API Documentation
- https://walnut-breeze-9a3.notion.site/IS212-Software-Project-management-e737406fca444cdc8f9f2cd92a0c0d60

## Development Approach
We will be using Scrum approach where weekly sprints and daily stand ups will be conducted.

## Application Start Up
### Pre-Requisite Installations before running the application
- WAMP/MAMP 
- Docker
- Selenium (For system test only)
- Ensure that ports 5001-5012 (for LJPS Services) & 8080 (for PhpMyAdmin) & 9906 (for MySQL) to be open

### Steps to run all services and view LJPS
1. Change directory to where the docker-compose.yml file is.
```sh
cd backend\services
```
2. Ensure your docker is running

3. Build all docker images and run containers
```sh
docker compose up
```

4. Start WAMP/MAMP with folder in web root directory (www) and open in browser for HR staff
```sh
http://localhost/learning-journey-planning-system/frontend/users/hr/
```

5. Start WAMP/MAMP with folder in web root directory (www) and open in browser for Learners
```sh
http://localhost/learning-journey-planning-system/frontend/users/learners/
```

6. Done!

## Tech Stack

- Vue.js
- Python
- Docker
- MySQL
- Bootstrap

## Testing Integrations
**Testing Tools**
- Selenium (For automated frontend system testing)
- Unittest (For both automated unit and integration testing)
- Flake8 (For Python Syntax checks)

## Contact

Vasilis - vasilis.ng.2020@scis.smu.edu.sg</br>
Shya - swquah.2020@scis.smu.edu.sg</br>
Jacky- jacky.teo.2020@scis.smu.edu.sg</br>
Erlynne - erlynneong.2020@scis.smu.edu.sg</br>
Yuki - yuki.han.2020@scis.smu.edu.sg</br>
Pearlyn - pearlyn.loh.2019@scis.smu.edu.sg</br>

Project Link: [https://github.com/is212g1t5/learning-journey-planning-system](https://github.com/is212g1t5/learning-journey-planning-system)
