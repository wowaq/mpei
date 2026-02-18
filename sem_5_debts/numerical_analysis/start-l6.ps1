# save as start-jupyter.ps1

# Set the path to your virtual environment and notebook
$VENV_PATH = ".\.venv"  # or full path like "C:\projects\myenv"
$NOTEBOOK_PATH = ".\lab6.ipynb"  # or full path to your notebook

# Check if virtual environment exists
if (-not (Test-Path $VENV_PATH)) {
    Write-Host "Virtual environment not found at $VENV_PATH" -ForegroundColor Red
    exit 1
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Green
& "$VENV_PATH\Scripts\Activate.ps1"

# Check if jupyter is installed
$jupyterCheck = python -c "import jupyter" 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Jupyter not found in virtual environment. Installing..." -ForegroundColor Yellow
    pip install jupyter
}

# Start Jupyter notebook
Write-Host "Starting Jupyter notebook..." -ForegroundColor Green
if ($NOTEBOOK_PATH -and (Test-Path $NOTEBOOK_PATH)) {
    jupyter notebook $NOTEBOOK_PATH
} else {
    Write-Host "Starting Jupyter in current directory" -ForegroundColor Yellow
    jupyter notebook
}
