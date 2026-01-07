import re
import os

def preprocess_arabic_text(text):
    """
    معالجة النص العربي قبل التحويل إلى كلام

    Args:
        text (str): النص العربي الأصلي

    Returns:
        str: النص المُعالج
    """
    # إزالة المسافات الزائدة
    text = re.sub(r'\s+', ' ', text).strip()

    # معالجة الأرقام العربية
    arabic_numbers = {
        '٠': '0', '١': '1', '٢': '2', '٣': '3', '٤': '4',
        '٥': '5', '٦': '6', '٧': '7', '٨': '8', '٩': '9'
    }

    for arabic, english in arabic_numbers.items():
        text = text.replace(arabic, english)

    return text

def check_model_files():
    """التحقق من وجود ملفات النماذج المطلوبة"""
    required_dirs = [
        "pretrained_models/g2p",
        "pretrained_models/tts",
        "pretrained_models/vocoder"
    ]

    for directory in required_dirs:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"تم إنشاء المجلد: {directory}")
