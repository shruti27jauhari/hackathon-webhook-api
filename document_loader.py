import pdfplumber
from docx import Document
import email
from email import policy
from email.parser import BytesParser


def extract_text_from_pdf(file):
    text = ''
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ''
    return text


def extract_text_from_docx(file):
    doc = Document(file)
    text = '\n'.join([para.text for para in doc.paragraphs])
    return text


def extract_text_from_eml(file):
    msg = BytesParser(policy=policy.default).parse(file)
    text = msg.get_body(preferencelist=('plain')).get_content() if msg.get_body(preferencelist=('plain')) else ''
    return text 