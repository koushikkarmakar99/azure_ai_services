FROM python:3.12-slim
WORKDIR /app/azure-ai-services
COPY . .
# Ensure the hostname is added to /etc/hosts
#RUN sudo echo "127.0.0.1 azureai.homelab.dev" >> /etc/hosts
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD [ "python", "src/app.py" ]
