#!/bin/bash

# OCR Document Processing - Stop Script
# This script helps you stop the application

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
echo "║              Stopping Services...                     ║"
echo "║                                                       ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to stop local processes
stop_local() {
    echo -e "${YELLOW}Stopping local processes...${NC}"

    stopped_count=0

    # Stop backend
    if [ -f "logs/backend.pid" ]; then
        BACKEND_PID=$(cat logs/backend.pid)
        if ps -p $BACKEND_PID > /dev/null 2>&1; then
            echo -e "${YELLOW}Stopping backend (PID: $BACKEND_PID)...${NC}"
            kill $BACKEND_PID 2>/dev/null || true
            stopped_count=$((stopped_count + 1))
        fi
        rm logs/backend.pid
    fi

    # Stop frontend
    if [ -f "logs/frontend.pid" ]; then
        FRONTEND_PID=$(cat logs/frontend.pid)
        if ps -p $FRONTEND_PID > /dev/null 2>&1; then
            echo -e "${YELLOW}Stopping frontend (PID: $FRONTEND_PID)...${NC}"
            kill $FRONTEND_PID 2>/dev/null || true
            stopped_count=$((stopped_count + 1))
        fi
        rm logs/frontend.pid
    fi

    # Also try to kill any uvicorn or http.server processes on the ports
    if command_exists lsof; then
        # Kill process on port 8000 (backend)
        PORT_8000_PID=$(lsof -ti:8000 2>/dev/null || true)
        if [ ! -z "$PORT_8000_PID" ]; then
            echo -e "${YELLOW}Stopping process on port 8000...${NC}"
            kill $PORT_8000_PID 2>/dev/null || true
            stopped_count=$((stopped_count + 1))
        fi

        # Kill process on port 8080 (frontend)
        PORT_8080_PID=$(lsof -ti:8080 2>/dev/null || true)
        if [ ! -z "$PORT_8080_PID" ]; then
            echo -e "${YELLOW}Stopping process on port 8080...${NC}"
            kill $PORT_8080_PID 2>/dev/null || true
            stopped_count=$((stopped_count + 1))
        fi
    fi

    # Clean up log files
    if [ -f "logs/backend.log" ]; then
        rm logs/backend.log
    fi

    if [ -f "logs/frontend.log" ]; then
        rm logs/frontend.log
    fi

    if [ $stopped_count -eq 0 ]; then
        echo -e "${YELLOW}No running processes found${NC}"
    else
        echo -e "${GREEN}✅ Stopped $stopped_count process(es)${NC}"
    fi
}

# Main logic
echo "Select stop method:"
echo ""
echo "1) Stop local processes"
echo "2) Exit"
echo ""
read -p "Enter your choice [1-2]: " choice

case $choice in
    1)
        stop_local
        ;;
    2)
        echo -e "${BLUE}No changes made${NC}"
        exit 0
        ;;
    *)
        echo -e "${RED}Invalid choice${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}Application stopped successfully!${NC}"
echo ""
