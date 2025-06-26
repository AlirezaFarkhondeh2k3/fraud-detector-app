
# 🚨 Fraud Detector App

A Dockerized Flask web application for detecting fraudulent transactions using a PyTorch model trained on anonymized credit card data.

## 📦 Features

- Upload CSV files for batch fraud prediction
- Manual form entry for real-time single prediction
- Torch-based neural network inference
- Scaler support for preprocessing
- Docker-ready deployment

## 🖼️ Project Structure

```

├── app.py                # Flask app
├── Dockerfile            # Docker build configuration 
├── .dockerignore         # Ignore unnecessary files during docker build
├── model/
│   ├── fraud\_model.pth   # Trained PyTorch model
│   └── scaler.save       # Scaler object for 'Time' and 'Amount'
├── templates/
│   ├── index.html        # Upload and input UI
│   └── results.html      # CSV output results

````

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/AlirezaFarkhondeh2k3/fraud-detector-app.git
cd fraud-detector-app
````

### 2. Build Docker Image

```bash
docker build -t fraud-detector .
```

### 3. Run the App

```bash
docker run -p 5000:5000 fraud-detector
```

Access the app at: [http://localhost:5000](http://localhost:5000)

## 🧠 Model Info

* Framework: PyTorch
* Architecture: Simple Feedforward NN
* Features: V1–V28 + Time + Amount
* Output: Binary classification (Fraud / Not Fraud)

## 📄 Sample CSV Format

| Time | V1 | V2 | ... | V28 | Amount |
| ---- | -- | -- | --- | --- | ------ |
| 1000 | .. | .. | ... | ..  | 120.50 |

> Ensure column headers match exactly.

## 🐳 DockerHub

The image is also available on Docker Hub:
👉 [`alirezafarkhondeh/fraud-detector`](https://hub.docker.com/r/alirezafarkhondeh/fraud-detector)

## 🧑‍💻 Author

**Alireza Farkhondeh**
Machine Learning Engineer | [LinkedIn](https://www.linkedin.com/in/alireza-farkhond)

---

````

You can:

1. Copy this and paste it directly into your `README.md`.
2. Commit and push it:

```bash
git add README.md
git commit -m "Add full project README"
git push
````
