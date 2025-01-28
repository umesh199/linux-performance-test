import subprocess
import csv

# Sysbench parameters
FILE_SIZE = "100G"
BLOCK_SIZE = "4K"
THREADS = 4
TEST_DURATION = 300  # Test duration in seconds
OUTPUT_FILE = "sysbench_fileio_results.csv"

# Commands for sysbench file I/O preparation and execution
prepare_command = f"sysbench fileio --file-total-size={FILE_SIZE} --file-block-size={BLOCK_SIZE} --threads={THREADS} prepare"
run_command = f"sysbench fileio --file-total-size={FILE_SIZE} --file-block-size={BLOCK_SIZE} --threads={THREADS} --time={TEST_DURATION} --file-test-mode=rndrw run"
cleanup_command = f"sysbench fileio cleanup"


def run_sysbench_command(command, description):
    """Runs a sysbench command and returns the result."""
    print(f"Executing {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        output = result.stdout
        if result.returncode == 0:
            print(f"{description} completed successfully.")
            return output
        else:
            print(f"Error during {description}: {result.stderr}")
            return None
    except Exception as e:
        print(f"Exception while running {description}: {e}")
        return None


def parse_sysbench_output(output):
    """Extract key performance metrics from sysbench output."""
    metrics = {}
    for line in output.splitlines():
        if "read," in line:
            metrics["Read Rate (MB/s)"] = line.split(":")[1].strip()
        if "written," in line:
            metrics["Write Rate (MB/s)"] = line.split(":")[1].strip()
        if "total time:" in line:
            metrics["Total Time (s)"] = line.split(":")[1].strip().replace("s", "")
        if "Latency" in line:
            metrics["Latency (ms)"] = line.split(":")[1].strip()
    return metrics


def write_results_to_csv(metrics):
    """Write results to CSV file."""
    print(f"Writing results to {OUTPUT_FILE}...")
    fieldnames = ["Read Rate (MB/s)", "Write Rate (MB/s)", "Total Time (s)", "Latency (ms)"]

    with open(OUTPUT_FILE, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(metrics)
    print(f"Results saved to {OUTPUT_FILE}")


def main():
    # Step 1: Prepare file I/O
    run_sysbench_command(prepare_command, "File I/O Preparation")

    # Step 2: Execute sysbench file I/O test
    output = run_sysbench_command(run_command, "File I/O Benchmark Test")

    if output:
        # Parse and save the results
        metrics = parse_sysbench_output(output)
        write_results_to_csv(metrics)

    # Step 3: Cleanup after the test
    run_sysbench_command(cleanup_command, "File I/O Cleanup")


if __name__ == "__main__":
    main()
