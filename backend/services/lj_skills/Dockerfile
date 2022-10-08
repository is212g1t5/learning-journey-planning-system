FROM python:3-slim
WORKDIR /usr/src/app
COPY ../http.reqs.txt ./
RUN python -m pip install --no-cache-dir -r http.reqs.txt
COPY ./lj_skills/lj_skills.py .
CMD [ "python", "./lj_skills.py" ]
