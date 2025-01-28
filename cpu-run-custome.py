import subprocess
import csv

# Sysbench CPU test parameters
NUM_THREADS = 32  # Adjust based on your system's core count
CPU_MAX_PRIME = 20000
TEST_DURATION = 300  # Test duration in seconds
OUTPUT_FILE = "sysbench_cpu_prime_results.csv"

def run_sysbench_cpu_max_prime():
    """Runs the sysbench CPU benchmark with --cpu-max-prime."""
    command = f"sysbench cpu --cpu-max-prime={CPU_MAX_PRIME} --threads={NUM_THREADS} --time={TEST_DURATION} run"
    print(f"Running sysbench CPU test for {TEST_DURATION} seconds with max prime {CPU_MAX_PRIME} using {NUM_THREADS} threads...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        output = result.stdout
        if result.returncode == 0:
            print("CPU max-prime benchmark test completed successfully.")
            return output
        else:
            print(f"Error during CPU benchmark: {result.stderr}")
            return None
    except Exception as e:
        print(f"Exception while running CPU max-prime benchmark: {e}")
        return None

def parse_sysbench_output(output):
    """Extract key performance metrics from sysbench output."""
    metrics = {}
    for line in output.splitlines():
        if "total time:" in line:
            metrics["Total Time (s)"] = line.split(":")[1].strip().replace("s", "")
        if "total number of events:" in line:
            metrics["Total Events"] = line.split(":")[1].strip()
        if "execution time (avg/stddev):" in line:
            metrics["Execution Time (ms)"] = line.split(":")[1].strip()
        if "events per second:" in line:
            metrics["Events Per Second"] = line.split(":")[1].strip()
    return metrics

def write_results_to_csv(metrics):
    """Write results to a CSV file."""
    print(f"Writing results to {OUTPUT_FILE}...")
    fieldnames = ["Total Time (s)", "Total Events", "Execution Time (ms)", "Events Per Second"]

    with open(OUTPUT_FILE, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(metrics)
    print(f"Results saved to {OUTPUT_FILE}")

def main():
    # Step 1: Run sysbench CPU max-prime test
    output = run_sysbench_cpu_max_prime()

    if output:
        # Step 2: Parse and save the results
        metrics = parse_sysbench_output(output)
        write_results_to_csv(metrics)

if __name__ == "__main__":
    main()
