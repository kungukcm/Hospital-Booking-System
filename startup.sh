#!/bin/bash
# Startup script for local development (Unix/Linux/macOS)
# Starts backend, frontend, and admin dashboard in separate processes

echo "🏥 KUTRRH Hospital Appointment System - Startup Script"
echo "======================================================="
echo ""

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
elif [ -d ".venv" ]; then
    source .venv/bin/activate
else
    echo "❌ Virtual environment not found. Please create one first."
    exit 1
fi

# Start backend API
echo "🚀 Starting Backend API on port 8000..."
python backend_api.py &
BACKEND_PID=$!

sleep 2

# Start Frontend
echo "🚀 Starting Public Frontend on port 8501..."
streamlit run frontend_app.py --logger.level=info --client.showErrorDetails=false &
FRONTEND_PID=$!

sleep 2

# Start Admin Dashboard
echo "🚀 Starting Admin Dashboard on port 8502..."
streamlit run admin_dashboard.py --logger.level=info --server.port 8502 --client.showErrorDetails=false &
ADMIN_PID=$!

echo ""
echo "✅ All services started successfully!"
echo ""
echo "📱 Public Frontend:  http://localhost:8501"
echo "🔒 Admin Dashboard:  http://localhost:8502"
echo "📡 Backend API:      http://localhost:8000"
echo "📊 API Docs:         http://localhost:8000/docs"
echo ""
echo "Default Admin Credentials:"
echo "  Username: admin"
echo "  Password: admin123"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Handle cleanup
trap "kill $BACKEND_PID $FRONTEND_PID $ADMIN_PID 2>/dev/null" EXIT

# Keep script running
wait
