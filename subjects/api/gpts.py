from io import BytesIO
import docx
import logging
import openai
import os
import chardet
import pdfplumber    
openai_api_key = os.getenv('API_KEY')


logging.basicConfig(filename='app.log', level=logging.INFO)
logger = logging.getLogger(__name__)


# Summary Generations from gpt
def generate_summary_from_gpt(content, prompt):
    openai.api_key = openai_api_key
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"{prompt}\n\n{content[:2000]}"}
        ],
        max_tokens=3000  # Adjust the max tokens based on the required summary length
    )
    summary = response.choices[0].message['content'].strip()
    return summary, prompt


# Key-Points Generations from gpt
def generate_keypoints_from_gpt(content, prompt):
    openai.api_key = openai_api_key
    # prompt = f"You are the key-points generator , Provide me the keypoints in bollet-points, related to the and everytime provide me unique keypoints : \n\n{content[:7500]}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"{prompt}\n\n{content[:2000]}"}
        ],
        max_tokens=1000  # Adjust the max tokens based on the required summary length
    )
    summary = response.choices[0].message['content'].strip()
    return summary, prompt


# Quizes Generations from gpt
def generate_quizes_from_gpt(content):
    openai.api_key = openai_api_key
    prompt = f"You are the teacher, Provide me a random number of quizzes with a maximum limit of 10 questions, each containing 4 options as MCQs. Indicate the correct option by labeling it A, B, C, or D and answer as 'Correct Answer'. Ensure the quizzes are different each time and challenging:\n\n{content[:7500]}\nPlease ensure your response is concise with no extra text, and format questions as 'Question:', and options as 'A:', 'B:', etc and aswer as 'Correct Answer: 'Correct Option''. please strictly follow this pattern for quiz and no other pattern will be allowed for quiz. Only allowed pattern is of question is 'Question:' and nothing else is allowed and make sure no new line will be in between 'Question:' and question heading"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=2000  # Adjust the max tokens based on the required summary length
    )
    quiz = response.choices[0].message['content'].strip()
    return quiz, prompt


#======================================================= Files reading and converting into text ===========================================
def read_file_content(file_path):
    try:
        if default_storage.exists(file_path):
            with default_storage.open(file_path) as file:
                if file_path.endswith('.docx'):
                    content = read_doc_file_content(file)
                elif file_path.endswith('.pdf'):
                    content = read_pdf_content(file)
                elif file_path.endswith('.txt'):
                    content = read_text_file_content(file)
                else:
                    logger.warning("Unsupported file type")
                    content = None
                return content
        else:
            logger.error("File does not exist.")
            return None
    except Exception as e:
        logger.error(f"Error processing file: {e}")
        return None


def read_doc_file_content(file):
    try:
        print(file)
        doc = docx.Document(file)
        print(doc)
        doc_content = [para.text for para in doc.paragraphs]
        print(doc_content)
        content = "\n".join(doc_content)
        print(content)
        return content.replace('\x00', '')  # Remove null bytes
    except Exception as e:
        logger.error(f"Error reading DOC/DOCX file: {e}")
        return None

def read_pdf_content(file):
    try:
        print(file)
        max_pages = 100
        pdf_content = []
        with pdfplumber.open(file) as pdf:
            for i, page in enumerate(pdf.pages):
                if i >= 5:
                    break
                text = page.extract_text()
                if text:
                    pdf_content.append(text)
        print(pdf_content)
        content = "\n".join(pdf_content)
        print(content)
        return content.replace('\x00', '')  # Remove null bytes
    except Exception as e:
        logger.error(f"Error reading PDF file: {e}")
        return None

def read_text_file_content(file):
    encodings = ['utf-8', 'latin-1']
    content = None

    for encoding in encodings:
        try:
            file.seek(0)  # Reset file pointer to the beginning
            content = file.read().decode(encoding)
            logger.info(f"Successfully decoded with encoding: {encoding}")
            break
        except UnicodeDecodeError:
            logger.warning(f"Failed to decode with encoding: {encoding}")
            continue

    if content is None:
        file.seek(0)
        raw_data = file.read()
        detected_encoding = chardet.detect(raw_data)['encoding']
        try:
            content = raw_data.decode(detected_encoding)
            logger.info(f"Successfully decoded with detected encoding: {detected_encoding}")
        except Exception as e:
            logger.error(f"Failed to decode with detected encoding: {detected_encoding}, Error: {e}")

    if content is None:
        logger.error("Unable to decode file content with any encoding")
        return None

    return content.replace('\x00', '')
