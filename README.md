# Advanced Spotify Data Analyzer

Advanced Spotify Data Analyzer is a web-based tool that analyzes your Spotify data on an advanced level. It uses Docker, Flask, Redis, and Celery to provide fast and scalable data processing.

## 🚀 Technologies Used

- **Python**
- **Flask**
- **Docker**
- **Redis** + **Celery**

## 📦 Installation & Setup

Follow these steps to get the project up and running:

### 1. Clone the Repository

Clone this repository using Git and navigate into the project directory.

```bash
git clone https://github.com/Zancmok/AdvancedSpotifyDataAnalyzer.git
cd AdvancedSpotifyDataAnalyzer
```

### 2. Install Docker

Make sure Docker and Docker Compose are installed on your machine.  
You can find installation instructions at: https://docs.docker.com/get-docker/

### 3. Get Spotify Developer Credentials

- Go to the Spotify Developer Dashboard: https://developer.spotify.com/dashboard/
- Create an app to obtain your Client ID and Client Secret

### 4. Create a `.env` File

In the root of the project, create a `.env` file with the following content:

```dotenv
CLIENT_ID=my_spotify_client_id
CLIENT_SECRET=my_spotify_client_secret
```

### 5. Build and Run the Project

Use Docker Compose to build and start the application.

```bash
docker-compose build
docker-compose up
```
