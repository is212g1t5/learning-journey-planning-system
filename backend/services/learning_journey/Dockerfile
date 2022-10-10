FROM python:3-slim
WORKDIR /usr/src/app
COPY ../http.reqs.txt ./
RUN python -m pip install --no-cache-dir -r http.reqs.txt
COPY ./learning_journey/learning_journey.py .
CMD [ "python", "./learning_journey.py" ]
