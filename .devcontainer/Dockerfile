FROM python:3.12-slim
WORKDIR /workspaces
# Install Git inside DevContainer
RUN apt-get update && apt-get install -y git
#RUN apk add --no-cache git bash openssh
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD [ "python", "src/app.py" ]
