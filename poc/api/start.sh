#!/bin/bash

# OCR Document Processing - Quick Start Script
# This script helps you start the application easily

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print banner
echo -e "${BLUE}"
echo "╔═══════════════════════════════════════════════════════╗"
echo "║                                                       ║"
echo "║        OCR Document Processing System                 ║"
echo "║                                                       ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to start locally
start_local() {
    echo -e "${GREEN}Starting locally...${NC}"
    
    # Check Python
    if ! command_exists python3 && ! command_exists python; then
        echo -e "${RED}Error: Python is not installed${NC}"
        echo "Please install Python 3.11 or higher"
        exit 1
    fi
    
    # Determine Python command
    if command_exists python3; then
        PYTHON_CMD="python3"
    else
        PYTHON_CMD="python"
    fi
    
    # Start backend
    echo -e "${YELLOW}Starting backend...${NC}"
    
    if [ ! -d "env_api/" ]; then
        echo -e "${YELLOW}Creating virtual environment...${NC}"
        $PYTHON_CMD -m venv env_api
        
        echo -e "${YELLOW}Installing dependencies...${NC}"
        if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
            source env_api/Scripts/activate
        else
            source env_api/bin/activate
        fi
        
        pip install -r requirements.txt
        cd ..
    fi
    
    # Start backend in background
    cd backend
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        source env_api/Scripts/activate
    else
        source ../env_api/bin/activate
    fi
    
    echo -e "${GREEN}Starting FastAPI server...${NC}"
    nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 > ../logs/backend.log 2>&1 &
    BACKEND_PID=$!
    echo $BACKEND_PID > ../logs/backend.pid
    cd ..
    
    # Wait for backend to start
    echo -e "${YELLOW}Waiting for backend to start...${NC}"
    sleep 3
    
    # Start frontend
    echo -e "${YELLOW}Starting frontend...${NC}"
    cd frontend
    
    echo -e "${GREEN}Starting HTTP server...${NC}"
    nohup $PYTHON_CMD -m http.server 8080 > ../logs/frontend.log 2>&1 &
    FRONTEND_PID=$!
    echo $FRONTEND_PID > ../logs/frontend.pid
    cd ..
    
    echo ""
    echo -e "${GREEN}✅ Application started successfully!${NC}"
    echo ""
    echo -e "${BLUE}Access the application:${NC}"
    echo -e "  Frontend:         ${GREEN}http://localhost:8080${NC}"
    echo -e "  Backend API:      ${GREEN}http://localhost:8000${NC}"
    echo -e "  API Docs:         ${GREEN}http://localhost:8000/docs${NC}"
    echo ""
    echo -e "${YELLOW}Backend PID: ${BACKEND_PID}${NC}"
    echo -e "${YELLOW}Frontend PID: ${FRONTEND_PID}${NC}"
    echo ""
    echo -e "${YELLOW}To view logs:${NC}"
    echo -e "  Backend:  tail -f backend.log"
    echo -e "  Frontend: tail -f frontend.log"
    echo ""
    echo -e "${YELLOW}To stop the application:${NC}"
    echo -e "  ./stop.sh"
    echo ""
}

# Main menu
echo "How would you like to start the application?"
echo ""
echo "1) Local Development (Python)"
echo "2) Exit"
echo ""
read -p "Enter your choice [1-2]: " choice

case $choice in
    1)
        start_local
        ;;
    2)
        echo -e "${BLUE}Goodbye!${NC}"
        exit 0
        ;;
    *)
        echo -e "${RED}Invalid choice${NC}"
        exit 1
        ;;
esac
