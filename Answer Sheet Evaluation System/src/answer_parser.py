import pdfplumber
import re

class AnswerParser:
    def __init__(self):
        # Comprehensive question pattern
        self.question_pattern = re.compile(
            r'(?:^|\n)(?:Q|Question|Problem|\d+)[\s.)-]*\s*(\d+)[\s:)-]*',
            re.IGNORECASE
        )

    def parse(self, pdf_path):
        """Parse PDF into {q_num: answer_text} using layout analysis"""
        answers = {}
        current_q = None
        answer_buffer = []

        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                # Extract text with layout preservation
                text = page.extract_text(layout=True, x_tolerance=5, y_tolerance=2)

                # Process text in order of appearance
                for line in text.split('\n'):
                    line = line.strip()
                    if not line:
                        continue

                    # Check for new question
                    match = self.question_pattern.search(line)
                    if match:
                        # Save previous answer
                        if current_q is not None:
                            answers[current_q] = ' '.join(answer_buffer).strip()
                            answer_buffer = []

                        current_q = int(match.group(1))
                        answer_start = match.end()
                        answer_buffer.append(line[answer_start:].strip())
                    else:
                        # Continue current answer
                        if current_q is not None:
                            answer_buffer.append(line)

        # Save last answer
        if current_q is not None:
            answers[current_q] = ' '.join(answer_buffer).strip()

        return self._merge_split_answers(answers)

    def _merge_split_answers(self, answers):
        """Merge answers split across pages/pages"""
        merged = {}
        sorted_qs = sorted(answers.keys())

        for q_num in sorted_qs:
            answer = answers[q_num]

            # Check if previous answer ends with continuation marker
            if q_num-1 in merged and merged[q_num-1].endswith((' ', '-')):
                merged[q_num-1] += ' ' + answer
            else:
                merged[q_num] = answer

        return merged





# import fitz
# import layoutparser as lp
# import torch
# from transformers import LayoutLMTokenizer, LayoutLMForTokenClassification

# class AdvancedAnswerParser:
#     def __init__(self):
#         # Load pre-trained LayoutLM model
#         self.model = LayoutLMForTokenClassification.from_pretrained('microsoft/layoutlm-base-uncased')
#         self.tokenizer = LayoutLMTokenizer.from_pretrained('microsoft/layoutlm-base-uncased')
        
#         # Initialize OCR agent
#         self.ocr_agent = lp.TesseractAgent(languages='eng')

#     def parse(self, pdf_path):
#         """Parse PDF using layout analysis and deep learning"""
#         # Extract text with layout information
#         doc = fitz.open(pdf_path)
#         pages = []
#         for page in doc:
#             words = page.get_text("words")
#             blocks = [{
#                 'text': word[4],
#                 'x0': word[0], 'y0': word[1],
#                 'x1': word[2], 'y1': word[3]
#             } for word in words]
#             pages.append(blocks)
        
#         # Process each page with LayoutLM
#         answers = {}
#         for page_num, page_blocks in enumerate(pages, 1):
#             # Prepare inputs
#             inputs = self.tokenizer(
#                 [block['text'] for block in page_blocks],
#                 return_tensors="pt",
#                 truncation=True,
#                 padding='max_length',
#                 max_length=512
#             )
            
#             # Add bounding boxes
#             boxes = [
#                 [block['x0'], block['y0'], block['x1'], block['y1']]
#                 for block in page_blocks
#             ]
#             inputs['bbox'] = torch.tensor([boxes[:512]])

#             # Get predictions
#             outputs = self.model(**inputs)
#             predictions = torch.argmax(outputs.logits, dim=2)[0]

#             # Post-process to group QA pairs
#             current_q = None
#             current_answer = []
#             for token, block in zip(predictions, page_blocks):
#                 if token == 0:  # Question class
#                     if current_q:
#                         answers[current_q] = ' '.join(current_answer)
#                     current_q = block['text']
#                     current_answer = []
#                 else:  # Answer class
#                     current_answer.append(block['text'])
#             if current_q:
#                 answers[current_q] = ' '.join(current_answer)

#         return answers





# import re

# class AnswerParser:
#     @staticmethod
#     def preprocess_pdf_text(text):
#         """Static method for text cleaning"""
#         # Remove page numbers and footers
#         text = re.sub(r'\n\d+\n', '\n', text)
#         # Normalize whitespace and line breaks
#         return ' '.join(text.replace('\n', ' ').split())

#     def parse(self, text):
#         """Parse text into question-answer pairs"""
#         # Remove LaTeX artifacts
#         text = re.sub(r'\\[a-z]+\*?\{.*?\}', '', text)
        
#         # Enhanced regex pattern (capture full answer without splitting)
#         pattern = r'(?:Q|Question)[\s\.]*(\d+)[\s:\-]*([\s\S]*?)(?=(?:Q|Question)[\s\.]*\d+|$)'
        
#         answers = {}
#         for match in re.finditer(pattern, text, re.IGNORECASE):
#             q_num = int(match.group(1))
#             # Normalize whitespace and line breaks in answer
#             answer = ' '.join(match.group(2).strip().split())  
#             answers[q_num] = answer
            
#         return answers


# import re
# import fitz  # PyMuPDF

# class AnswerParser:
#     def parse(self, pdf_path):
#         """Parse PDF with enhanced question detection"""
#         doc = fitz.open(pdf_path)
#         full_text = "\n".join([page.get_text() for page in doc])
        
#         # Unified pattern for both formats: "Q1" and "1)"
#         pattern = r'''
#             (?:^|\n)                          # Start of line
#             (?:                               # Question prefix
#                 (?:Q|Question|Problem)\s*(\d+)  # Format: Q1, Question 2
#                 |                             # OR
#                 (\d+)[.)\s-]                   # Format: 1), 2., 3-
#             )
#             [\s:\-)]*                         # Separators
#             (.*?)                              # Answer text
#             (?=(?:Q|Question|Problem|\d+[.)\s-]|\Z)) # Lookahead
#         '''
        
#         answers = {}
#         for match in re.finditer(pattern, full_text, re.VERBOSE | re.IGNORECASE | re.DOTALL):
#             q_num = int(match.group(1) or match.group(2))  # Handle both groups
#             answer = ' '.join(match.group(3).strip().split())
#             answers[q_num] = answer
            
#         return answers