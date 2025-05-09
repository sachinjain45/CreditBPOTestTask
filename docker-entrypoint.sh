#!/bin/bash

# Function to display help message
show_help() {
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  up        Start all services"
    echo "  down      Stop all services"
    echo "  build     Build all services"
    echo "  logs      Show logs from all services"
    echo "  clean     Remove all containers, networks, and volumes"
    echo "  help      Show this help message"
    echo ""
}

# Function to start services
start_services() {
    echo "Starting services..."
    docker-compose up -d
    echo "Services started successfully!"
}

# Function to stop services
stop_services() {
    echo "Stopping services..."
    docker-compose down
    echo "Services stopped successfully!"
}

# Function to build services
build_services() {
    echo "Building services..."
    docker-compose build
    echo "Services built successfully!"
}

# Function to show logs
show_logs() {
    echo "Showing logs..."
    docker-compose logs -f
}

# Function to clean up
clean_up() {
    echo "Cleaning up..."
    docker-compose down -v
    echo "Cleanup completed successfully!"
}

# Main script logic
case "$1" in
    "up")
        start_services
        ;;
    "down")
        stop_services
        ;;
    "build")
        build_services
        ;;
    "logs")
        show_logs
        ;;
    "clean")
        clean_up
        ;;
    "help"|"")
        show_help
        ;;
    *)
        echo "Unknown command: $1"
        show_help
        exit 1
        ;;
esac 