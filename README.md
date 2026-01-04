# 🎧 Predicting Podcast Listening Time  
*A Machine Learning project to estimate how long a user will listen to a podcast episode.*

---

## 📌 Overview  
This project predicts the **number of minutes** a user will spend listening to a podcast based on:

- Podcast name  
- Genre  
- Episode length  
- Publication day & time  

The task is framed as a **regression problem**, and the project includes a full end‑to‑end workflow: data ingestion, model training, model registry, monitoring, and a Flask-based web interface for real-time predictions.

---

## 🚀 Installation  

It is recommended to install dependencies inside a **virtual environment** (e.g., `venv` or Anaconda).

This project was built using **Python 3.9**.

```bash
pip install -r requirements.txt

```
## 🧰 Tech Stack  

| Category | Tools |
|---------|-------|
| **Frontend** | Flask, HTML, CSS |
| **Backend** | Flask |
| **Language** | Python |
| **Model Registry** | MLflow (via Dagshub) |
| **Monitoring** | Evidently |
| **Feature Store** | GitHub |
| **CI/CD** | GitHub Actions |
| **Database** | SQLite |

---

## 🏗️ High‑Level Design Document  

You can view the full High‑Level Design Document here:

[📄 **ML Podcast Listening Prediction – HLD**](https://github.com/abbeymaj80/my-ml-datasets/raw/refs/heads/master/Design_Docs/ML_Podcast_Listening_Prediction_HLD.docx)

---

## 🌐 Web Application Screenshots  

The project includes a simple two‑page Flask web app for user interaction.

---

### 🏠 Landing Page  
Provides an overview of the project and navigation to the prediction interface.

![Landing Page Screenshot](https://github.com/abbeymaj80/my-ml-datasets/blob/master/screenshots/Podcast_Landing_Page.png)

---

### 🎯 Prediction Page  
Allows users to input podcast details (name, genre, episode length, publication day/time) and generate a predicted listening duration.

![Prediction Page Screenshot](https://github.com/abbeymaj80/my-ml-datasets/blob/master/screenshots/Podcast_Prediction_Page.png)