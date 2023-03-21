import csv

# Replace 'filename.csv' with the path to your CSV file
with open('./experiment_results/3_19_1_mega_prompt_8.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    # Skip the header row
    next(reader)
    # Change the number 2 to the index of the column you want to iterate over (0-based)
    freq_counts = {}
    for row in reader:
        num_question_marks = row[3].count('?')
        if num_question_marks in freq_counts:
            freq_counts[num_question_marks] += 1
        else:
            freq_counts[num_question_marks] = 1

    # Print the frequency counts
    for value, count in freq_counts.items():
        print(f"{count} question marks in '{value}'")
