#!/bin/bash
# Build script for OBDPHAWD multi-language project

set -e

echo "🚗 Building OBDPHAWD - OBD2 and Automotive Protocol Handler"
echo "============================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default build configuration
BUILD_PYTHON=true
BUILD_JAVA=true
BUILD_C=true
BUILD_TESTS=true
BUILD_EXAMPLES=true
CLEAN_BUILD=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --python-only)
            BUILD_PYTHON=true
            BUILD_JAVA=false
            BUILD_C=false
            shift
            ;;
        --java-only)
            BUILD_PYTHON=false
            BUILD_JAVA=true
            BUILD_C=false
            shift
            ;;
        --c-only)
            BUILD_PYTHON=false
            BUILD_JAVA=false
            BUILD_C=true
            shift
            ;;
        --no-tests)
            BUILD_TESTS=false
            shift
            ;;
        --no-examples)
            BUILD_EXAMPLES=false
            shift
            ;;
        --clean)
            CLEAN_BUILD=true
            shift
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo "Options:"
            echo "  --python-only    Build only Python components"
            echo "  --java-only      Build only Java components"
            echo "  --c-only         Build only C components"
            echo "  --no-tests       Skip building tests"
            echo "  --no-examples    Skip building examples"
            echo "  --clean          Clean build directories first"
            echo "  --help           Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Function to print status messages
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Clean build directories if requested
if [ "$CLEAN_BUILD" = true ]; then
    print_status "Cleaning build directories..."
    rm -rf build/
    rm -rf src/python/build/
    rm -rf src/python/dist/
    rm -rf src/python/*.egg-info/
    rm -rf src/java/target/
    rm -rf src/c/build/
    mkdir -p build
fi

# Create build directory
mkdir -p build

# Build Python components
if [ "$BUILD_PYTHON" = true ]; then
    print_status "Building Python components..."
    
    cd src/python
    
    # Check if Python is available
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed or not in PATH"
        exit 1
    fi
    
    # Install dependencies
    print_status "Installing Python dependencies..."
    pip3 install -r requirements.txt
    
    # Build package
    print_status "Building Python package..."
    python3 setup.py build
    
    if [ "$BUILD_TESTS" = true ]; then
        print_status "Running Python tests..."
        if command -v pytest &> /dev/null; then
            pytest ../../tests/python/ -v
        else
            print_warning "pytest not available, skipping Python tests"
        fi
    fi
    
    cd ../..
    print_success "Python components built successfully"
fi

# Build Java components
if [ "$BUILD_JAVA" = true ]; then
    print_status "Building Java components..."
    
    cd src/java
    
    # Check if Maven is available
    if ! command -v mvn &> /dev/null; then
        print_error "Maven is not installed or not in PATH"
        exit 1
    fi
    
    # Check Java version
    if ! command -v java &> /dev/null; then
        print_error "Java is not installed or not in PATH"
        exit 1
    fi
    
    JAVA_VERSION=$(java -version 2>&1 | head -n1 | cut -d'"' -f2 | cut -d'.' -f1)
    if [ "$JAVA_VERSION" -lt 11 ]; then
        print_error "Java 11 or higher is required (found Java $JAVA_VERSION)"
        exit 1
    fi
    
    # Build with Maven
    print_status "Building Java package with Maven..."
    mvn clean compile package
    
    if [ "$BUILD_TESTS" = true ]; then
        print_status "Running Java tests..."
        mvn test
    fi
    
    cd ../..
    print_success "Java components built successfully"
fi

# Build C components
if [ "$BUILD_C" = true ]; then
    print_status "Building C components..."
    
    cd src/c
    
    # Check if CMake is available
    if ! command -v cmake &> /dev/null; then
        print_error "CMake is not installed or not in PATH"
        exit 1
    fi
    
    # Check if make is available
    if ! command -v make &> /dev/null; then
        print_error "Make is not installed or not in PATH"
        exit 1
    fi
    
    # Create build directory
    mkdir -p build
    cd build
    
    # Configure with CMake
    print_status "Configuring C build with CMake..."
    cmake .. -DCMAKE_BUILD_TYPE=Release \
             -DBUILD_EXAMPLES=$BUILD_EXAMPLES \
             -DBUILD_TESTS=$BUILD_TESTS
    
    # Build
    print_status "Building C library..."
    make -j$(nproc)
    
    if [ "$BUILD_TESTS" = true ]; then
        print_status "Running C tests..."
        make test
    fi
    
    cd ../../..
    print_success "C components built successfully"
fi

# Copy build artifacts
print_status "Copying build artifacts..."

# Python artifacts
if [ "$BUILD_PYTHON" = true ] && [ -d "src/python/build" ]; then
    cp -r src/python/build/* build/ 2>/dev/null || true
fi

# Java artifacts
if [ "$BUILD_JAVA" = true ] && [ -d "src/java/target" ]; then
    mkdir -p build/java
    cp src/java/target/*.jar build/java/ 2>/dev/null || true
fi

# C artifacts
if [ "$BUILD_C" = true ] && [ -d "src/c/build" ]; then
    mkdir -p build/c
    cp src/c/build/libobdphawd* build/c/ 2>/dev/null || true
    if [ "$BUILD_EXAMPLES" = true ]; then
        mkdir -p build/c/examples
        cp src/c/build/examples/* build/c/examples/ 2>/dev/null || true
    fi
fi

# Build summary
echo
echo "🎉 Build Summary"
echo "================"
if [ "$BUILD_PYTHON" = true ]; then
    print_success "✓ Python components built"
fi
if [ "$BUILD_JAVA" = true ]; then
    print_success "✓ Java components built"
fi
if [ "$BUILD_C" = true ]; then
    print_success "✓ C components built"
fi

echo
print_status "Build artifacts are available in the 'build/' directory"
print_status "Run examples from the 'examples/' directory"
print_status "For usage instructions, see README.md"

echo
print_success "🚗 OBDPHAWD build completed successfully!"