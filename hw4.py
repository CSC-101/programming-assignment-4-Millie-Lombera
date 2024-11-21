import sys
from build_data import get_data

def display(counties):
    for county in counties:
        print(f"County: {county.county}, State: {county.state}")
        print(f"  Population: {county.population}")
        print(f"  Income: {county.income}")
        print(f"  Education: {county.education}")
        print(f"  Ethnicities: {county.ethnicities}")
        print("-" * 40)

def filter_state(counties, state_abbreviation):
    filtered = [county for county in counties if county.state == state_abbreviation]
    print(f"Filter: state == {state_abbreviation} ({len(filtered)} entries)")
    return filtered

def filter_gt(self, field, threshold):
    self.data = [entry for entry in self.data if float(entry.get(field, 0)) > threshold]
    print(f"Filter: {field} gt {threshold} ({len(self.data)} entries)")

def filter_lt(self, field, threshold):
    self.data = [entry for entry in self.data if float(entry.get(field, 0)) < threshold]
    print(f"Filter: {field} lt {threshold} ({len(self.data)} entries)")

def population_total(counties):
    total_population = sum(county.population['2014 Population'] for county in counties)
    print(f"2014 population: {total_population}")

def population_field(counties, field):
    total_population = sum(county.population['2014 Population'] for county in counties)
    sub_population = sum(
        county.population['2014 Population'] * (county.ethnicities[field] / 100)
        for county in counties if field in county.ethnicities
    )
    print(f"2014 {field} population: {sub_population}")

def population_percentage(counties, field):
    total_population = sum(county.population['2014 Population'] for county in counties)
    sub_population = sum(
        county.population['2014 Population'] * (county.ethnicities[field] / 100)
        for county in counties if field in county.ethnicities
    )
    percentage = (sub_population / total_population) * 100
    print(f"2014 {field} percentage: {percentage}")

def main():
    if len(sys.argv) != 2:
        print("Error: Please provide a valid operations file.")
        return

    operations_file = sys.argv[1]
    try:
        with open(operations_file, 'r') as file:
            operations = file.readlines()
    except FileNotFoundError:
        print(f"Error: Cannot open file '{operations_file}'.")
        return

    counties = get_data()

    for operation in operations:
        parts = operation.strip().split(":")
        command = parts[0]
        if command == "display":
            display(counties)
        elif command == "filter-state":
            counties = filter_state(counties, parts[1])
        elif command.startswith("filter-"):
            op = ">" if "gt" in command else "<"
            counties = filter_field(counties, parts[1], op, float(parts[2]))
        elif command == "population-total":
            population_total(counties)
        elif command == "population":
            population_field(counties, parts[1])
        elif command == "percent":
            population_percentage(counties, parts[1])
        else:
            print(f"Error: Unknown operation '{command}'.")

if __name__ == "__main__":
    main()