function plot_csv_data(logfile, x_column, y_column, graph_type, y1_color, y2_color)
    % Set default values for optional arguments
    if nargin < 5
        y1_color = 'b'; % Default color for y1
    end
    if nargin < 6
        y2_color = 'r'; % Default color for y2
    end

    % Read CSV file with 'preserve' rule to keep original column names
    data = readtable(logfile, 'VariableNamingRule', 'preserve');

    lon_column = 'Longitude';
    lat_column = 'Latitude';

    % Check if the necessary columns exist
    required_columns = {x_column, y_column, lon_column, lat_column};
    if ~all(ismember(required_columns, data.Properties.VariableNames))
        error('Columns "%s", "%s", "%s", or "%s" not found in the CSV file.', ...
              x_column, y_column, lon_column, lat_column);
    end

    % Define starting position
    start_lon = data.(lon_column)(1);
    start_lat = data.(lat_column)(1);

    % Calculate distances using the Haversine formula
    data.distance = haversine_m(start_lon, start_lat, data.(lon_column), data.(lat_column)) * 100;

    % Plot based on the graph type
    figure;
    hold on;
    if strcmp(graph_type, 'scatter')
        scatter(data.(x_column), data.(y_column), 8, y1_color, 'filled');
        scatter(data.(x_column), data.distance, 8, y2_color, 'filled');
    elseif strcmp(graph_type, 'line')
        plot(data.(x_column), data.(y_column), 'Color', y1_color, 'LineWidth', 1.5);
        plot(data.(x_column), (data.distance - 35) * -1, 'Color', y2_color, 'LineWidth', 1.5);
    else
        error('Invalid graph type');
    end

    xlabel(x_column);
    title(sprintf('%s (y1) and distance (y2) vs %s', y_column, x_column));
    legend(y_column, 'distance');
    grid on;
    hold off;
end

function dist = haversine_m(lon1, lat1, lon2, lat2)
    % Convert degrees to radians
    lon1 = deg2rad(lon1);
    lat1 = deg2rad(lat1);
    lon2 = deg2rad(lon2);
    lat2 = deg2rad(lat2);

    % Haversine formula
    dlon = lon2 - lon1;
    dlat = lat2 - lat1;
    a = sin(dlat / 2).^2 + cos(lat1) .* cos(lat2) .* sin(dlon / 2).^2;
    c = 2 * atan2(sqrt(a), sqrt(1 - a));
    r = 6371; % Radius of Earth in kilometers
    dist = r * c; % Distance in kilometers
end
