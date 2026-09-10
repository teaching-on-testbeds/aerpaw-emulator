# LoRaWAN Gateway Performance Post-Processing Script

## Overview
This script processes data from LoRaWAN gateways to evaluate performance metrics such as **Received Signal Strength Indicator (RSSI)**, **Signal-to-Noise Ratio (SNR)**, and **time differences** between sent and received packets. The processed data is visualized and saved for further analysis.

## Data Source
The dataset is available for download from the following link:  
[LoRaWAN Gateway Performance Data](https://drive.google.com/drive/folders/14pEIBTHh6zVG0FDxs8m1X33OrQC66Wx1?usp=sharing)

## Purpose
The purpose of this analysis is to evaluate the performance of LoRaWAN gateways under various conditions. The results are intended to support the following use cases:

1. **LoRaWAN Optimization**: Analyze gateway performance to optimize IoT network deployments.
2. **Data Reliability Studies**: Assess the reliability of transmitted data under varying conditions.
3. **IoT-Based Navigation Systems**: Support the development of IoT-enabled vehicle navigation and telemetry systems.
4. **Energy Efficiency Analysis**: Explore power consumption patterns in LoRaWAN devices.

## Data Collection Details
### Transmitter:
- **Device**: LoRaWAN-enabled IoT LoStik device.
- **Host**: Connected to a LattePanda MiniPC.
- **Data Sent**: Telemetry data consisting of `packageNumber` and `timestamp` over LoRaWAN.
- **Transmission Rate**: Each packet was transmitted at intervals of **1.5 seconds**.

### Receiver:
- **Gateways**: RAK7289CV2-V1 LoRaWAN gateways located in multiple locations (LW1, LW2, LW3, LW4, LW5, CC2, CC3, RE2).
- **Metrics Recorded**: Signal strength (RSSI), noise levels (SNR), and reception timestamps.

### Experiment Context:
- The dataset was collected during **Packapalooza**.
- Both raw telemetry data from vehicles and gateway performance metrics were logged.

## Script Functionality
The script performs the following steps:

1. **Data Import and Parsing**:
   - Imports the provided CSV data.
   - Ensures specific columns (timestamps, RSSI, SNR) are treated correctly as numeric or text data.

2. **Timestamp Conversion**:
   - Converts `sent_timestamp` (milliseconds since epoch) to numeric format.
   - Parses `rx_time` (ISO 8601 format) into milliseconds since epoch.

3. **Time Difference Calculation**:
   - Computes the difference between `sent_timestamp` and `rx_time`.

4. **Data Cleaning**:
   - Converts RSSI and SNR values to numeric format.
   - Removes rows with missing or invalid data.

5. **Outlier Filtering**:
   - Filters out time differences outside a defined threshold (±1 second) for cleaner visualizations.

6. **Data Visualization**:
   - **RSSI Distribution**: Histogram showing frequency of RSSI values.
   - **SNR Distribution**: Histogram showing frequency of SNR values.
   - **Time Differences**: Plot of time differences for valid packets.
   - **Scatter Plot**: Visualization of the relationship between RSSI and SNR.

7. **Per-Gateway Analysis**:
   - Groups data by gateway IDs.
   - Computes and displays average RSSI and SNR for each gateway.

8. **Data Export**:
   - Saves the processed data (RSSI, SNR, time differences, gateway IDs) to a new CSV file: `processed_network_data.csv`.

## Required Software
The script is written in **MATLAB** and requires the following:
- MATLAB (any recent version).
- Access to the dataset in CSV format.

## How to Use
1. Download the dataset from the provided link.
2. Place the dataset (`helikate_vehicle_out_results_202411251748028.csv`) in the same directory as the script.
3. Run the script in MATLAB.
4. The script will:
   - Process the data.
   - Generate visualizations (RSSI, SNR, time differences).
   - Display average metrics per gateway.
   - Save the processed data to `processed_network_data.csv`.

## Output
### Visualizations:
- RSSI Distribution
- SNR Distribution
- Time Differences (Filtered)
- Scatter Plot of RSSI vs SNR

### Processed Data:
- A CSV file, `processed_network_data.csv`, containing:
  - RSSI
  - SNR
  - Time Differences (ms)
  - Gateway IDs

### Per-Gateway Metrics:
The script prints the average RSSI and SNR for each gateway in the MATLAB Command Window.

## Acknowledgments
The data was collected during **Packapalooza**, leveraging the following equipment:
- **Transmitter**: LoStik device with LattePanda MiniPC.
- **Gateways**: RAK7289CV2-V1.

## Notes
- Ensure the dataset file is accessible and formatted correctly.
- For large datasets, consider optimizing memory usage or processing only relevant columns.

For any questions or clarifications, feel free to reach out.
"svargas3@ncsu.edu"

