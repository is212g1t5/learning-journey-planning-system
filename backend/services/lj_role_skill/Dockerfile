FROM python:3-slim
WORKDIR /usr/src/app
COPY ../http.reqs.txt ./
RUN python -m pip install --no-cache-dir -r http.reqs.txt
COPY ./lj_role_skill/lj_role_skill.py .
CMD [ "python", "./lj_role_skill.py" ]
