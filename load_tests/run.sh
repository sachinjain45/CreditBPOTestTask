#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Function to display help message
show_help() {
    echo "Usage: $0 [test_type] [options]"
    echo ""
    echo "Test Types:"
    echo "  auth       Run authentication load tests"
    echo "  payments   Run payment system load tests"
    echo "  matching   Run matching system load tests"
    echo "  all        Run all load tests"
    echo ""
    echo "Options:"
    echo "  -u, --url     API URL (default: http://localhost:8000/api)"
    echo "  -h, --help    Show this help message"
    echo ""
}

# Default values
API_URL="http://localhost:8000/api"
TEST_TYPE=""

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        auth|payments|matching|all)
            TEST_TYPE="$1"
            shift
            ;;
        -u|--url)
            API_URL="$2"
            shift 2
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            show_help
            exit 1
            ;;
    esac
done

# Check if test type is specified
if [ -z "$TEST_TYPE" ]; then
    echo -e "${RED}Error: Test type not specified${NC}"
    show_help
    exit 1
fi

# Function to run a test
run_test() {
    local test_file=$1
    local test_name=$2
    
    echo -e "${YELLOW}Running $test_name load test...${NC}"
    k6 run -e API_URL="$API_URL" "$test_file"
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}$test_name load test completed successfully${NC}"
    else
        echo -e "${RED}$test_name load test failed${NC}"
        exit 1
    fi
}

# Run selected tests
case $TEST_TYPE in
    auth)
        run_test "auth.js" "Authentication"
        ;;
    payments)
        run_test "payments.js" "Payment System"
        ;;
    matching)
        run_test "matching.js" "Matching System"
        ;;
    all)
        run_test "auth.js" "Authentication"
        run_test "payments.js" "Payment System"
        run_test "matching.js" "Matching System"
        ;;
esac 