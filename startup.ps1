# PowerShell Startup Script for Hospital Appointment System
# Starts backend, frontend, and admin dashboard in separate processes

Write-Host "🏥 KUTRRH Hospital Appointment System - Startup Script" -ForegroundColor Cyan
Write-Host "=======================================================" -ForegroundColor Cyan
Write-Host ""

# Activate virtual environment
if (Test-Path ".\venv\Scripts\Activate.ps1") {
    & ".\venv\Scripts\Activate.ps1"
    $PythonExe = (Resolve-Path ".\venv\Scripts\python.exe").Path
} elseif (Test-Path ".\.venv\Scripts\Activate.ps1") {
    & ".\.venv\Scripts\Activate.ps1"
    $PythonExe = (Resolve-Path ".\.venv\Scripts\python.exe").Path
} else {
    Write-Host "❌ Virtual environment not found. Please create one first." -ForegroundColor Red
    exit 1
}

# Function to start process
function Start-ServiceProcess {
    param (
        [string]$Name,
        [string]$Command,
        [string]$Port,
        [string]$Emoji
    )
    
    Write-Host "$Emoji Starting $Name on port $Port..." -ForegroundColor Yellow
    
    # Start process in new window
    if ($Name -eq "Backend API") {
        Start-Process -FilePath $PythonExe -ArgumentList "backend_api.py" -WorkingDirectory (Get-Location)
    } else {
        Start-Process -FilePath $PythonExe -ArgumentList "-m streamlit run $Command --logger.level=info --client.showErrorDetails=false" -WorkingDirectory (Get-Location)
    }
    
    Start-Sleep -Seconds 2
}

# Start all services
Start-ServiceProcess -Name "Backend API" -Command "backend_api.py" -Port "8000" -Emoji "🚀"
Start-ServiceProcess -Name "Public Frontend" -Command "frontend_app.py" -Port "8501" -Emoji "🚀"

# For admin dashboard, need to pass different port
Write-Host "🚀 Starting Admin Dashboard on port 8502..." -ForegroundColor Yellow
Start-Process -FilePath $PythonExe -ArgumentList "-m streamlit run admin_dashboard.py --logger.level=info --server.port 8502 --client.showErrorDetails=false" -WorkingDirectory (Get-Location)

Start-Sleep -Seconds 2

Write-Host ""
Write-Host "✅ All services started successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "📱 Public Frontend:  http://localhost:8501" -ForegroundColor Cyan
Write-Host "🔒 Admin Dashboard:  http://localhost:8502" -ForegroundColor Cyan
Write-Host "📡 Backend API:      http://localhost:8000" -ForegroundColor Cyan
Write-Host "📊 API Docs:         http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Default Admin Credentials:" -ForegroundColor Yellow
Write-Host "  Username: admin" -ForegroundColor Yellow
Write-Host "  Password: admin123" -ForegroundColor Yellow
Write-Host ""
Write-Host "⚠️  IMPORTANT: Change default admin password after first login!" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Ctrl+C in each window to stop services" -ForegroundColor Gray
Write-Host ""
