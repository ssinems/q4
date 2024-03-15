import csv


def read_csv(file_path):
    records = []
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            records.append(row)
    return records


def fill_missing_data(records):
    grouped_records = {}

    for record in records:
        country = record['country']
        daily_vaccinations = record['daily_vaccinations']

        if country not in grouped_records:
            if daily_vaccinations != '':
                daily_vaccinations = float(daily_vaccinations)
            else:
                daily_vaccinations = float('inf')
            grouped_records[country] = {'min_daily_vaccinations': daily_vaccinations, 'records': []}
        else:
            if daily_vaccinations != '':
                daily_vaccinations = float(daily_vaccinations)
            else:
                daily_vaccinations = float('inf')
            grouped_records[country]['min_daily_vaccinations'] = min(grouped_records[country]['min_daily_vaccinations'],
                                                                     daily_vaccinations)

        grouped_records[country]['records'].append(record)


    for country, data in grouped_records.items():
        min_daily_vaccinations = data['min_daily_vaccinations']
        for record in data['records']:
            if record['daily_vaccinations'] == '':
                record['daily_vaccinations'] = min_daily_vaccinations


    for country, data in grouped_records.items():
        for record in data['records']:
            if record['daily_vaccinations'] == float('inf'):
                record['daily_vaccinations'] = 0

    return records


def write_csv(records, file_path):
    with open(file_path, 'w', newline='') as csv_file:
        fieldnames = ['country', 'date', 'daily_vaccinations', 'vaccines']
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()
        for record in records:
            csv_writer.writerow(record)


if __name__ == '__main__':
    input_file = 'input.csv'
    records = read_csv(input_file)
    filled_records = fill_missing_data(records)
    write_csv(filled_records, input_file)