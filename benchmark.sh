#!/bin/bash
# Performance benchmark script for PDF extraction system

echo "PDF Extraction System Performance Benchmark"
echo "==========================================="

# Create test directory
mkdir -p benchmark_results

# Function to run benchmark
run_benchmark() {
    local pdf_file="$1"
    local iterations=5
    local total_time=0

    echo "Benchmarking: $pdf_file"
    echo "Running $iterations iterations..."

    for i in $(seq 1 $iterations); do
        echo -n "Iteration $i: "
        start_time=$(date +%s.%N)

        docker run --rm -v $(pwd)/test:/test pdf-extractor:latest "/test/$pdf_file" > /dev/null 2>&1

        end_time=$(date +%s.%N)
        iteration_time=$(echo "$end_time - $start_time" | bc -l)
        echo "${iteration_time}s"

        total_time=$(echo "$total_time + $iteration_time" | bc -l)
    done

    avg_time=$(echo "scale=2; $total_time / $iterations" | bc -l)
    echo "Average time: ${avg_time}s"
    echo "Target: ≤10s for 50 pages"
    echo ""
}

# Check if test PDFs exist
if [ ! -d "test" ]; then
    echo "Please create a 'test' directory with PDF files for benchmarking"
    exit 1
fi

# Run benchmarks on all PDFs in test directory
for pdf in test/*.pdf; do
    if [ -f "$pdf" ]; then
        run_benchmark "$(basename "$pdf")"
    fi
done

echo "Benchmark completed!"