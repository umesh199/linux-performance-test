import csv
import re
import pandas as pd
import matplotlib.pyplot as plt
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
    """Write server performance data to Excel with graphs."""
    if not data:
        print("No data to write to Excel.")
        return

    # Create DataFrame from the list of dictionaries
    df = pd.DataFrame(data)
    
    # Write to Excel
    with pd.ExcelWriter(OUTPUT_EXCEL_FILE) as writer:
        df.to_excel(writer, index=False, sheet_name="CPU Performance")
        print(f"Data written to {OUTPUT_EXCEL_FILE}.")

    # Create a graph
    plot_graphs(df)

def plot_graphs(df):
    """Plot performance graphs."""
    plt.figure(figsize=(12, 6))

    # Plot Total Time
    plt.subplot(1, 2, 1)
    plt.bar(df["Server"], df["Total Time (s)"], color='skyblue')
    plt.title("Total CPU Test Time (Lower is Better)")
    plt.xticks(rotation=45)
    plt.xlabel("Server")
    plt.ylabel("Time (s)")

    # Plot Events Per Second
    plt.subplot(1, 2, 2)
    plt.bar(df["Server"], df["Events Per Second"], color='lightgreen')
    plt.title("CPU Events Per Second (Higher is Better)")
    plt.xticks(rotation=45)
    plt.xlabel("Server")
    plt.ylabel("Events/sec")

    plt.tight_layout()
    plt.savefig("cpu_performance_graphs.png")
    plt.show()
    print("Graphs saved as 'cpu_performance_graphs.png'.")

def main():
    # Parse the Ansible results and write to Excel
    server_data = parse_ansible_output(ANSIBLE_RESULTS_FILE)
    write_to_excel(server_data)

if __name__ == "__main__":
    main()
