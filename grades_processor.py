import csv
import sys
import os

# Threshold to determine pass/fail
PASS_THRESHOLD = 40

def read_student_data(input_file):
    """Reads student data from a CSV file."""
    students = []
    try:
        with open(input_file, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                name = row['Name']
                scores = [float(row[subject]) for subject in row if subject != 'Name']
                students.append({'name': name, 'scores': scores})
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
    return students

def process_student_data(students):
    """Calculates average score and pass/fail status for each student."""
    results = []
    for student in students:
        average = sum(student['scores']) / len(student['scores'])
        status = 'Pass' if average >= PASS_THRESHOLD else 'Fail'
        results.append({'name': student['name'], 'average': round(average, 2), 'status': status})
    return results

def write_output_file(results, output_file='grades_output.csv'):
    """Writes the processed results to an output CSV file."""
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['Name', 'Average', 'Status'])
        writer.writeheader()
        for result in results:
            writer.writerow({'Name': result['name'], 'Average': result['average'], 'Status': result['status']})

def generate_summary(results, report_file='summary.txt'):
    """Generates a summary report file based on the results."""
    highest = max(results, key=lambda x: x['average'])
    lowest = min(results, key=lambda x: x['average'])
    class_average = round(sum(r['average'] for r in results) / len(results), 2)
    pass_count = sum(1 for r in results if r['status'] == 'Pass')
    fail_count = sum(1 for r in results if r['status'] == 'Fail')

    with open(report_file, mode='w', encoding='utf-8') as f:
        f.write(f"Number of students: {len(results)}\n")
        f.write(f"Highest Scorer: {highest['name']} ({highest['average']})\n")
        f.write(f"Lowest Scorer: {lowest['name']} ({lowest['average']})\n")
        f.write(f"Average Class Score: {class_average}\n")
        f.write(f"Pass Count: {pass_count}\n")
        f.write(f"Fail Count: {fail_count}\n")

def main():
    if len(sys.argv) != 2:
        print("Usage: python grades_processor.py <input_file.csv>")
        sys.exit(1)

    input_file = sys.argv[1]
    students = read_student_data(input_file)
    results = process_student_data(students)
    write_output_file(results)
    generate_summary(results)
    print("Processing complete. Output saved to 'grades_output.csv' and 'summary.txt'.")

if __name__ == "__main__":
    main()
