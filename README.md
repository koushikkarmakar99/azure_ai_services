# azure_ai_services
# Azure AI Services

This repository provides a Flask-based REST API for interacting with various Azure AI services, including Computer Vision, Natural Language Processing (NLP), and Text Translation. The API is designed for real-time data processing and can be run securely with HTTPS support.

## Features

- **Computer Vision**
  - Analyze images for tags, captions, objects, and more
  - Optical Character Recognition (OCR) for extracting text from images

- **Natural Language Processing (NLP)**
  - Sentiment analysis, key phrase extraction, and other text analytics

- **Text Translation**
  - Detect language and translate text between languages using Azure Translator

- **Logging**
  - Structured logging using [loguru](https://github.com/Delgan/loguru)

- **Dev Container Support**
  - Ready-to-use development environment with VS Code Dev Containers

## Project Structure

```
.
├── src/
│   ├── app.py                        # Main Flask application
│   ├── azure_image_analysis.py       # Azure Computer Vision API integration
│   ├── azure_text_analysis_nlp.py    # Azure NLP API integration
│   ├── azure_translate_text.py       # Azure Translator API integration
│   ├── optical_character_recognition.py # OCR using Azure Vision
│   └── setup_logger.py               # Logging setup
├── certificates/                     # SSL certificates for HTTPS (not tracked by git)
├── images/                           # Sample images (not tracked by git)
├── logs/                             # Log files (not tracked by git)
├── requirements.txt                  # Python dependencies
├── Dockerfile                        # Production Dockerfile
├── .devcontainer/                    # Dev Container configuration
│   ├── devcontainer.json
│   └── Dockerfile
└── README.md                         # Project documentation
```

## Getting Started

### Prerequisites

- Docker (recommended) or Python 3.11+
- Azure Cognitive Services subscription (API keys required)

### Running with Docker

Build and run the container:

```sh
docker build -t azure-ai-services .
docker run -p 5000:5000 --rm azure-ai-services
```

### Running in Dev Container (VS Code)

1. Open the project in VS Code.
2. Use the "Reopen in Container" command.
3. The environment will be ready with all dependencies installed.

### Running Locally

```sh
pip install -r requirements.txt
python src/app.py --debug
```

#### With HTTPS

Place your `cert.pem` and `key.pem` in the `certificates/` directory and run:

```sh
python src/app.py --ssl
```

## API Endpoints

### Health Check

- `GET /`  
  Returns: `"Api is up and running"`

### Computer Vision

- `POST /computer-vision/analyze-image/<features>`
  - JSON: `{ "service_name": "...", "subscription_key": "...", "image_url": "..." }`
  - Or as `multipart/form-data` with an image file

- `POST /computer-vision/optical-character-recognition`
  - JSON: `{ "service_name": "...", "subscription_key": "...", "image_url": "..." }`
  - Or as `multipart/form-data` with an image file

### NLP

- `POST /nlp/analyze-text/<functionality>`
  - JSON: `{ "service_name": "...", "subscription_key": "...", "text": "..." }`

### Translation

- `POST /nlp/detect-language`
  - JSON: `{ "subscription_key": "...", "region": "...", "text": "..." }`

## Configuration

- **API Keys:** Obtain from Azure Portal for each service.
- **SSL Certificates:** Place in `certificates/` for HTTPS support.

## Logging

Logs are output to the console in structured format using loguru. You can customize logging in [`src/setup_logger.py`](src/setup_logger.py).

## Contributing

Pull requests are welcome! Please open issues for suggestions or bugs.

## License

This project is licensed under the MIT License.

---

**Author:** Koushik Karmakar (karmakar.2007@gmail.com)  
**Changelog:** See [CHANGELOG.md](CHANGELOG.md)
