# 代码生成时间: 2025-09-24 06:01:48
import os
import logging
from celery import Celery
# 改进用户体验
from celery.signals import worker_process_init
from docx import Document
from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams


# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Celery配置
broker_url = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
app = Celery('document_converter', broker=broker_url)


# Celery任务：将Word文档转换为文本
# TODO: 优化性能
@app.task
def convert_docx_to_txt(file_path):
    """将Word文档转换为文本文件"""
    try:
        doc = Document(file_path)
        full_text = ""
        for para in doc.paragraphs:
            full_text += para.text + "\
"
        with open(file_path.replace('.docx', '.txt'), 'w') as txt_file:
            txt_file.write(full_text)
# 增强安全性
        return f'Converted {file_path} to TXT successfully'
    except Exception as e:
        logger.error(f'Error converting {file_path} to TXT: {e}')
# 改进用户体验
        raise


# Celery任务：将PDF文档转换为文本
@app.task
def convert_pdf_to_txt(file_path):
    "