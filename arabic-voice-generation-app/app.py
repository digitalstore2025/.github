import gradio as gr
import numpy as np
from tts_model import ArabicTTS
import os

# تهيئة نموذج تحويل النص إلى كلام
tts = ArabicTTS()

def generate_speech(text, speed=1.0):
    """
    توليد الصوت من النص العربي

    Args:
        text (str): النص العربي
        speed (float): سرعة القراءة (0.5-2.0)

    Returns:
        tuple: (معدل العينة, الصوت المُوَلَّد)
    """
    if not text.strip():
        return None, "الرجاء إدخال نص للتحويل"

    # توليد الصوت
    audio = tts.text_to_speech(text)

    if audio is not None:
        # تعديل سرعة القراءة إذا لزم الأمر
        if speed != 1.0:
            # يمكن إضافة تعديل السرعة هنا
            pass

        # حفظ الصوت مؤقتًا
        temp_filename = "temp_output.wav"
        tts.save_audio(audio, temp_filename)

        # إرجاع الصوت للواجهة
        return (22050, audio), None
    else:
        return None, "حدث خطأ في توليد الصوت"

# إنشاء واجهة المستخدم
with gr.Blocks(title="تطبيق توليدي للأصوات العربية") as demo:
    gr.Markdown("# 🗣️ تطبيق توليدي للأصوات العربية")
    gr.Markdown("تحويل النص العربي إلى كلام باستخدام تقنيات مفتوحة المصدر")

    with gr.Row():
        with gr.Column():
            text_input = gr.Textbox(
                label="أدخل النص العربي",
                placeholder="اكتب النص الذي تريد تحويله إلى كلام...",
                lines=5
            )
            speed_slider = gr.Slider(
                minimum=0.5,
                maximum=2.0,
                value=1.0,
                label="سرعة القراءة"
            )
            generate_btn = gr.Button("تحويل إلى كلام", variant="primary")

        with gr.Column():
            audio_output = gr.Audio(label="الصوت المُوَلَّد")
            error_output = gr.Textbox(label="رسائل الخطأ", interactive=False)

    generate_btn.click(
        fn=generate_speech,
        inputs=[text_input, speed_slider],
        outputs=[audio_output, error_output]
    )

    gr.Markdown("### أمثلة للنصوص العربية:")
    gr.Examples(
        examples=[
            "السلام عليكم ورحمة الله وبركاته",
            "مرحباً بك في تطبيق تحويل النص إلى كلام",
            "هذا التطبيق يستخدم تقنيات مفتوحة المصدر",
            "يمكنك كتابة أي نص عربي وسيتم تحويله إلى كلام",
            "نأمل أن تجد هذا التطبيق مفيداً"
        ],
        inputs=text_input
    )

# تشغيل التطبيق
if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
