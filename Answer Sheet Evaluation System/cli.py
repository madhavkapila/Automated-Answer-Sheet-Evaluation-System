# import argparse
# import os
# from src.main import evaluate_student
# from config.paths import PATHS

# # CLI for evaluating student answer sheets
# # This script allows users to evaluate student answer sheets from the command line.
# # It takes the roll number, name, and PDF filename as input arguments.
# # The script processes the PDF, extracts answers, scores them, and generates a report.
# # The CLI input will look like:
# # python cli.py --rollno S001 --name "John Doe" --pdf answers.pdf --start-page 3

# def main():
#     parser = argparse.ArgumentParser(
#         description='Evaluate Student Answer Sheets',
#         formatter_class=argparse.RawTextHelpFormatter
#     )
#     parser.add_argument('--rollno', type=str, required=True, 
#                       help='Student roll number (e.g. S001)')
#     parser.add_argument('--name', type=str, required=True,
#                       help='Student full name (e.g. "John Doe")')
#     parser.add_argument('--pdf', type=str, required=True,
#                       help='PDF filename in data/ directory (e.g. answers.pdf)')
#     parser.add_argument('--start-page', type=int, default=1,
#                       help='First page containing answers (default: 1)')

#     args = parser.parse_args()

#     try:
#         # Build full PDF path
#         pdf_path = os.path.join(PATHS['data'], args.pdf)
        
#         if not os.path.exists(pdf_path):
#             raise FileNotFoundError(f"PDF file not found: {pdf_path}")

#         # Process and get results
#         total_score, percentage = evaluate_student(
#             pdf_path=pdf_path,
#             rollno=args.rollno,
#             name=args.name,
#             start_page=args.start_page
#         )

#         # Print formatted output
#         print("\nEvaluation Results:")
#         print(f"Roll No: {args.rollno}")
#         print(f"Name: {args.name}")
#         print(f"Total Score: {total_score}/{(len(PATHS['weights']))}")  # Assuming 5 marks per question
#         print(f"Percentage: {percentage:.2f}%")

#     except Exception as e:
#         print(f"\nError: {str(e)}")
#         exit(1)

# if __name__ == "__main__":
#     main()
