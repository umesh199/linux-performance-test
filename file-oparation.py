import subprocess
import csv

# Sysbench File I/O test parameters
FILE_SIZE = "100G"
BLOCK_SIZE = "4K"
NUM_THREADS = 4
TEST_DURATION = 300  # Test duration in seconds
OUTPUT_FILE = "sysbench_fileio_results.csv"

def run_sysbench_fileio():
    """Runs the sysbench file I/O benchmark."""
    prepare_command = f"sysbench fileio --file-total-size={FILE_SIZE} prepare"
    run_command = f"sysbench fileio --file-total-size={FILE_SIZE} --file-test-mode=rndrw --block-size={BLOCK_SIZE} --threads={NUM_THREADS} --time={TEST_DURATION} run"
    cleanup_command = f"sysbench fileio --file-total-size={FILE_SIZE} cleanup"

    try:
        # Step 1: Prepare file
        print(f"Preparing file system with size {FILE_SIZE}...")
        subprocess.run(prepare_command, shell=True, check=True)

        # Step 2: Run file I/O benchmark
        print(f"Running sysbench file I/O test for {TEST_DURATION} seconds with block size {BLOCK_SIZE} and {NUM_THREADS} threads...")
        result = subprocess.run(run_command, shell=True, capture_output=True, text=True)
        output = result.stdout
        if result.returncode == 0:
            print("File I/O benchmark test completed successfully.")
        else:
            print(f"Error during file I/O benchmark: {result.stderr}")
            output = None

        # Step 3: Cleanup test files
        print("Cleaning up test files...")
        subprocess.run(cleanup_command, shell=True, check=True)

        return output
    except subprocess.CalledProcessError as e:
        print(f"Error while running sysbench fileio: {e}")
        return None

def parse_sysbench_output(output):
    """Extract key performance metrics from sysbench output."""
    metrics = {}
    for line in output.splitlines():
        if "read, MiB/s:" in line:
            metrics["Read Throughput (MiB/s)"] = line.split(":")[1].strip()
        if "written, MiB/s:" in line:
            metrics["Write Throughput (MiB/s)"] = line.split(":")[1].strip()
        if "fsyncs per second:" in line:
            metrics["Fsyncs Per Second"] = line.split(":")[1].strip()
        if "total time:" in line:
            metrics["Total Time (s)"] = line.split(":")[1].strip().replace("s", "")
    return metrics

def write_results_to_csv(metrics):
    """Write results to a CSV file."""
    print(f"Writing results to {OUTPUT_FILE}...")
    fieldnames = ["Read Throughput (MiB/s)", "Write Throughput (MiB/s)", "Fsyncs Per Second", "Total Time (s)"]

    with open(OUTPUT_FILE, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(metrics)
    print(f"Results saved to {OUTPUT_FILE}")

def main():
    # Step 1: Run sysbench file I/O test
    output = run_sysbench_fileio()

    if output:
        # Step 2: Parse and save the results
        metrics = parse_sysbench_output(output)
        write_results_to_csv(metrics)

if __name__ == "__main__":
    main()
