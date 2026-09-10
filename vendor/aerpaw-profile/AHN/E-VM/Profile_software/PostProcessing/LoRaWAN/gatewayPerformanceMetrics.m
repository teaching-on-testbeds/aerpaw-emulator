% Load the CSV file
opts = detectImportOptions('helikate_vehicle_out_results_202411251748028.csv', 'Delimiter', ',');
opts = setvartype(opts, {'sent_timestamp', 'rx_time', 'rx_rssi', 'rx_snr'}, 'char'); % Ensure specific columns are treated as text
data = readtable('helikate_vehicle_out_results_202411251748028.csv', opts);

% Convert sent_timestamp (milliseconds since epoch) to numeric
sent_timestamp = str2double(data.sent_timestamp); % Convert to numeric (milliseconds since epoch)

% Convert rx_time (ISO 8601 format) to numeric (milliseconds since epoch)
rx_time = datetime(data.rx_time, 'InputFormat', 'yyyy-MM-dd''T''HH:mm:ss.SSSSSSXXX', 'TimeZone', 'UTC'); % Parse with UTC time zone
rx_time = posixtime(rx_time) * 1000; % Convert to milliseconds

% Calculate time differences (ms)
time_differences = rx_time - sent_timestamp;

% Convert RSSI and SNR to numeric
rx_rssi = str2double(data.rx_rssi); % Ensure RSSI is numeric
rx_snr = str2double(data.rx_snr);  % Ensure SNR is numeric

% Remove rows with NaN values in any column
valid_indices = ~isnan(rx_rssi) & ~isnan(rx_snr); % Valid rows
rx_rssi = rx_rssi(valid_indices);
rx_snr = rx_snr(valid_indices);
gateway_ids = data.rx_gatewayId(valid_indices); % Filter gateway IDs to match valid indices
time_differences = time_differences(valid_indices); % Filter time differences

% Filter outliers in time differences for plotting only
threshold = 1e3; % Define a threshold for valid time differences (e.g., ±1 second in ms)
valid_time_indices = abs(time_differences) <= threshold; % Logical array of valid indices
filtered_time_differences = time_differences(valid_time_indices); % Filtered time differences
filtered_packet_indices = find(valid_time_indices); % Corresponding packet indices

% Plot RSSI Distribution
figure;
histogram(rx_rssi, 20);
title('RSSI Distribution');
xlabel('RSSI (dBm)');
ylabel('Frequency');
grid on;

% Plot SNR Distribution
figure;
histogram(rx_snr, 20);
title('SNR Distribution');
xlabel('SNR (dB)');
ylabel('Frequency');
grid on;

% Plot Time Differences (Filtered)
figure;
plot(filtered_packet_indices, filtered_time_differences, 'o-');
title('Filtered Time Differences Between Sent and Received (ms)');
xlabel('Packet Index');
ylabel('Time Difference (ms)');
grid on;

% Group by Gateway and Analyze
unique_gateways = unique(gateway_ids);
for i = 1:length(unique_gateways)
   gateway = unique_gateways{i};
   gateway_indices = strcmp(gateway_ids, gateway);

   % Calculate average RSSI and SNR for this gateway
   avg_rssi = mean(rx_rssi(gateway_indices));
   avg_snr = mean(rx_snr(gateway_indices));
   fprintf('Gateway: %s, Avg RSSI: %.2f dBm, Avg SNR: %.2f dB\n', ...
      gateway, avg_rssi, avg_snr);
end

% Scatter Plot: RSSI vs SNR
figure;
scatter(rx_rssi, rx_snr, 'filled');
title('RSSI vs SNR');
xlabel('RSSI (dBm)');
ylabel('SNR (dB)');
grid on;

% Save processed data to a new CSV
output_table = table(rx_rssi, rx_snr, time_differences, gateway_ids, ...
   'VariableNames', {'RSSI', 'SNR', 'TimeDifference_ms', 'GatewayID'});
writetable(output_table, 'processed_network_data.csv');
disp('Processed data saved to processed_network_data.csv');