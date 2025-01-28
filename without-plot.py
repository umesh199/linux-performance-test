import re
import pandas as pd
import os

ANSIBLE_RESULTS_FILE = "/tmp/sysbench_cpu_results.txt"
OUTPUT_EXCEL_FILE = "cpu_performance_results.xlsx"

def parse_ansible_output(file_path):
    """Parse the sysbench output from Ansible."""
    server_data = []
    
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return server_data

    with open(file_path, "r") as file:
        for line in file:
            match = re.search(r"(?P<server_name>.*?): .*?total time:\s*(?P<total_time>[\d.]+)s.*?events per second:\s*(?P<events_per_sec>[\d.]+)", line.replace("\n", " "))
            if match:
                server_data.append({
                    "Server": match.group("server_name"),
                    "Total Time (s)": float(match.group("total_time")),
                    "Events Per Second": float(match.group("events_per_sec"))
                })
    return server_data

def write_to_excel(data):
    """Write server performance data to Excel."""
    if not data:
        print("No data to write to Excel.")
        return

    # Create DataFrame from the list of dictionaries
    df = pd.DataFrame(data)
    
    # Write to Excel
    df.to_excel(OUTPUT_EXCEL_FILE, index=False, sheet_name="CPU Performance")
    print(f"Data written to {OUTPUT_EXCEL_FILE}.")

def main():
    # Parse the Ansible results and write to Excel
    server_data = parse_ansible_output(ANSIBLE_RESULTS_FILE)
    write_to_excel(server_data)

if __name__ == "__main__":
    main()
