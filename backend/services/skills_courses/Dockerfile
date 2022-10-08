FROM python:3-slim
WORKDIR /usr/src/app
COPY ../http.reqs.txt ./
RUN python -m pip install --no-cache-dir -r http.reqs.txt
COPY ./skills_courses/skills_courses.py .
CMD [ "python", "./skills_courses.py" ]
