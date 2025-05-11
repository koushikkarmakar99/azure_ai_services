FROM python:alpine
WORKDIR /app/azure-ai-services
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD [ "python", "src/app.py" ]
