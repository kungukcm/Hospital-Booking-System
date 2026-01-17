# Hospital Booking System - Deployment Guide

## Local Development

### Prerequisites
- Python 3.10+
- Virtual environment (venv)
- Groq API Key

### Setup

1. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   
   # Windows
   .\venv\Scripts\activate
   
   # Unix/macOS
   source venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   Create a `.env` file in the project root:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here (optional)
   ```

4. **Run the application:**
   ```bash
   streamlit run app.py
   ```
   The app will be accessible at `http://localhost:8501`

---

## Docker Deployment

### Prerequisites
- Docker installed
- Docker Compose installed (optional but recommended)

### Using Docker Compose (Recommended)

1. **Create `.env` file** with your API keys

2. **Build and run:**
   ```bash
   docker-compose up --build
   ```

3. **Access the application:**
   Open your browser to `http://localhost:8501`

4. **Stop the application:**
   ```bash
   docker-compose down
   ```

### Using Docker Directly

1. **Build the image:**
   ```bash
   docker build -t hospital-booking-system .
   ```

2. **Run the container:**
   ```bash
   docker run -p 8501:8501 \
     -e GROQ_API_KEY=your_groq_api_key \
     hospital-booking-system
   ```

---

## Cloud Deployment

### Option 1: Streamlit Cloud (Recommended for Streamlit apps)

1. **Push your code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/kungukcm/Hospital-Booking-System.git
   git push -u origin main
   ```

2. **Deploy to Streamlit Cloud:**
   - Go to https://streamlit.io/cloud
   - Click "New app"
   - Connect your GitHub repository
   - Select the branch and app.py file
   - Deploy!

3. **Set environment variables:**
   - In Streamlit Cloud dashboard, go to App settings
   - Add secrets:
     ```
     GROQ_API_KEY = "your_key"
     OPENAI_API_KEY = "your_key" (optional)
     ```

### Option 2: AWS (EC2)

1. **Launch an EC2 instance:**
   - Use Ubuntu 20.04 LTS or later
   - Allocate at least 2GB RAM

2. **SSH into your instance:**
   ```bash
   ssh -i your-key.pem ubuntu@your-instance-ip
   ```

3. **Install dependencies:**
   ```bash
   sudo apt-get update
   sudo apt-get install -y python3-pip python3-venv git
   ```

4. **Clone your repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/Hospital-Booking-System.git
   cd Hospital-Booking-System
   ```

5. **Create and activate virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

6. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

7. **Configure environment:**
   ```bash
   nano .env
   # Add your API keys
   ```

8. **Run with Streamlit:**
   ```bash
   streamlit run app.py --server.port 8501 --server.address 0.0.0.0
   ```

9. **Use systemd service for persistence:**
   Create `/etc/systemd/system/hospital-booking.service`:
   ```ini
   [Unit]
   Description=Hospital Booking System
   After=network.target

   [Service]
   Type=simple
   User=ubuntu
   WorkingDirectory=/home/ubuntu/Hospital-Booking-System
   Environment="PATH=/home/ubuntu/Hospital-Booking-System/venv/bin"
   Environment="GROQ_API_KEY=your_key"
   ExecStart=/home/ubuntu/Hospital-Booking-System/venv/bin/streamlit run app.py --server.port 8501 --server.address 0.0.0.0

   [Install]
   WantedBy=multi-user.target
   ```
   
   Then enable and start:
   ```bash
   sudo systemctl enable hospital-booking
   sudo systemctl start hospital-booking
   ```

### Option 3: Heroku

1. **Create `Procfile`:**
   ```
   web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. **Create `runtime.txt`:**
   ```
   python-3.11.0
   ```

3. **Login and deploy:**
   ```bash
   heroku login
   heroku create your-app-name
   git push heroku main
   ```

4. **Set environment variables:**
   ```bash
   heroku config:set GROQ_API_KEY="your_key"
   ```

### Option 4: Google Cloud Run

1. **Build and push Docker image:**
   ```bash
   docker build -t gcr.io/YOUR_PROJECT_ID/hospital-booking .
   docker push gcr.io/YOUR_PROJECT_ID/hospital-booking
   ```

2. **Deploy to Cloud Run:**
   ```bash
   gcloud run deploy hospital-booking \
     --image gcr.io/YOUR_PROJECT_ID/hospital-booking \
     --platform managed \
     --region us-central1 \
     --set-env-vars GROQ_API_KEY=your_key
   ```

---

## Monitoring and Maintenance

### Check Logs
- **Local:** Logs are written to `app.log`
- **Docker:** `docker-compose logs -f`
- **Cloud:** Use your cloud provider's log viewer

### Database Considerations
Currently, the app uses Streamlit's session state (in-memory). For production with persistent data:
- Integrate a database like PostgreSQL
- Implement a backend API using FastAPI (already in requirements)

### Security Best Practices
- Never commit `.env` file
- Use a secrets manager (e.g., AWS Secrets Manager, Heroku Config Vars)
- Rotate API keys regularly
- Use HTTPS in production
- Implement rate limiting for API calls

---

## Troubleshooting

**Issue:** GROQ_API_KEY not found
- Ensure `.env` file exists with correct key
- Verify key is set in cloud environment variables

**Issue:** Application crashes on startup
- Check `app.log` for errors
- Verify all dependencies are installed
- Ensure Python version is 3.10+

**Issue:** Port already in use
- Change port: `streamlit run app.py --server.port 8502`
- Or kill existing process using the port

---

## Support

For issues or questions, please check the logs and ensure:
1. API keys are valid and have appropriate permissions
2. Dependencies are correctly installed
3. Python version is compatible (3.10+)
4. Network connectivity to external APIs is available
