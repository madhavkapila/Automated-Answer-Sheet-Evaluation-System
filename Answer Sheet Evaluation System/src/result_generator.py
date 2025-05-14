import pandas as pd
from config.paths import PATHS


class ResultGenerator:
    def __init__(self):
        self.results_df = pd.DataFrame(columns=['RollNo', 'Name', 'Total', 'Percentage'])
        self.metadata_df = pd.DataFrame()

    def add_student(self, rollno, name, scores):
        # Add default 0 scores for missing questions
        for q_num in range(1, 201):
            if q_num not in scores:
                scores[q_num] = 0

        # Calculate total and percentage CORRECTLY
        max_possible = 200  # 200 questions × 5 marks each
        total = sum(scores.values())
        perc = (total / max_possible) * 100  # Fixed here
        
        self.results_df.loc[len(self.results_df)] = [rollno, name, total, perc]

        # Update metadata
        student_data = {'RollNo': rollno, 'Name': name}
        student_data.update({'Total': total, 'Percentage': perc})

        self.metadata_df = pd.concat([self.metadata_df, pd.DataFrame([student_data])], ignore_index=True)

        return [rollno, name, total, perc]

    def save_results(self):
        self.results_df.to_csv(PATHS['output']['results'], mode='a', header=False, index=False)
        self.metadata_df.to_csv(PATHS['output']['metadata'], mode='a', header=False, index=False)
