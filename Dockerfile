FROM python:3.10-slim

WORKDIR /app
COPY . .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP=app.chatbot_api:app
EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
