from config.paths import PATHS
from src.pdf_processor import PDFProcessor
from src.answer_parser import AnswerParser
from src.scoring_engine import ScoringEngine
from src.result_generator import ResultGenerator
import warnings
import os
import logging


logging.getLogger("pdfminer").setLevel(logging.ERROR)

def evaluate_student(pdf_path, rollno, name, start_page=1):
    # Initialize components
    processor = PDFProcessor(start_page)
    parser = AnswerParser()
    scorer = ScoringEngine()
    reporter = ResultGenerator()
    
    # Process PDF
    raw_text = processor.extract_text(pdf_path)
    # clean_text = parser.preprocess_pdf_text(raw_text)  # Static method call
    answers = parser.parse(pdf_path)  # Instance method

    # Score answers with detailed logging
    scores = {}
    for q_num, answer_text in answers.items():
        try:
            # answer_text = answer_data['answer']
            score = scorer.calculate_total_score(answer_text, q_num)
            print(f"Q{q_num}: {score:.2f}/1.0")  # Print individual scores 
            scores[q_num] = score
        except KeyError as e:
            print(f"\n⚠️ Skipping Q{q_num}: {str(e)}")
        except Exception as e:
            print(f"\n❌ Error processing Q{q_num}: {str(e)}")

    # Generate reports
    reporter.add_student(rollno, name, scores)
    reporter.save_results()
    total = sum(scores.values())
    max_score = len(answers)
    print(f"\nProcessed {name} ({rollno}). Total: {total}/{max_score} ({total/max_score*100:.2f}%)")

