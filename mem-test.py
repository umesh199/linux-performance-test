import subprocess
import csv

# Sysbench Memory test parameters
NUM_THREADS = 32  # Adjust based on your system's configuration
OUTPUT_FILE = "sysbench_memory_results.csv"

def run_sysbench_memory():
    """Runs the sysbench memory benchmark test."""
    command = f"sysbench memory --threads={NUM_THREADS} run"
    print(f"Running sysbench memory benchmark with {NUM_THREADS} threads...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        output = result.stdout
        if result.returncode == 0:
            print("Memory benchmark test completed successfully.")
            return output
        else:
            print(f"Error during memory benchmark: {result.stderr}")
            return None
    except Exception as e:
        print(f"Exception while running memory benchmark: {e}")
        return None

def parse_sysbench_output(output):
    """Extract key performance metrics from sysbench output."""
    metrics = {}
    for line in output.splitlines():
        if "transferred" in line:
            metrics["Transfer Rate (MB/s)"] = line.split(":")[1].strip()
        if "total time:" in line:
            metrics["Total Time (s)"] = line.split(":")[1].strip().replace("s", "")
        if "Operations per second:" in line:
            metrics["Operations Per Second"] = line.split(":")[1].strip()
        if "Latency (ms)" in line:
            metrics["Latency (ms)"] = line.split(":")[1].strip()
    return metrics

def write_results_to_csv(metrics):
    """Write results to a CSV file."""
    print(f"Writing results to {OUTPUT_FILE}...")
    fieldnames = ["Transfer Rate (MB/s)", "Total Time (s)", "Operations Per Second", "Latency (ms)"]

    with open(OUTPUT_FILE, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(metrics)
    print(f"Results saved to {OUTPUT_FILE}")

def main():
    # Step 1: Run sysbench memory test
    output = run_sysbench_memory()

    if output:
        # Step 2: Parse and save the results
        metrics = parse_sysbench_output(output)
        write_results_to_csv(metrics)

if __name__ == "__main__":
    main()
