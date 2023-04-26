def parse_historical_data(txt_file):
    with open(txt_file, 'r') as file:
        lines = file.readlines()

    data = [line.strip().split() for line in lines[-10:-1]]

    monthly_data = [list(map(float, row[0:])) for row in data]

    monthly_sums = [0] * 12
    for row in monthly_data:
        for i in range(1, 13):
            monthly_sums[i - 1] += row[i]

    monthly_means = [round(month_sum / len(monthly_data), 1)
                     for month_sum in monthly_sums]

    month_names = ["jan", "feb", "mar", "apr", "may",
                   "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
    mean_temps_by_month = dict(zip(month_names, monthly_means))

    return mean_temps_by_month


# Usage example
weather_data_file = "historical.txt"
mean_temps = parse_historical_data(weather_data_file)
print(mean_temps)
