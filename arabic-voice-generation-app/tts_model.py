import torch
import torchaudio
from speechbrain.inference.text import GraphemeToPhoneme
from speechbrain.inference.TTS import Tacotron2
from speechbrain.inference.vocoders import HIFIGAN
import numpy as np
import librosa

class ArabicTTS:
    def __init__(self):
        """تهيئة نموذج تحويل النص إلى كلام للغة العربية"""
        # تحميل نموذج تحويل الحروف إلى أصوات (Grapheme-to-Phoneme)
        self.g2p = GraphemeToPhoneme.from_hparams(
            "speechbrain/tts_models/arabic-tacotron2-collab",
            savedir="pretrained_models/g2p"
        )

        # تحميل نموذج Tacotron2 للغة العربية
        self.tts_model = Tacotron2.from_hparams(
            "speechbrain/tts_models/arabic-tacotron2-collab",
            savedir="pretrained_models/tts"
        )

        # تحميل نموذج HIFIGAN لتوليد الصوت عالي الجودة
        self.vocoder = HIFIGAN.from_hparams(
            "speechbrain/tts_models/arabic-hifigan-collab",
            savedir="pretrained_models/vocoder"
        )

    def text_to_speech(self, text):
        """
        تحويل النص العربي إلى كلام

        Args:
            text (str): النص العربي المراد تحويله

        Returns:
            numpy.ndarray: الصوت المُوَلَّد
        """
        try:
            # تحويل النص إلى صوتيفات (Phonemes)
            phonemes = self.g2p.g2p(text)
            print(f"النصوص الصوتية: {phonemes}")

            # إنشاء التمثيل الطيفي للصوت
            mel_spec, _, _ = self.tts_model.encode_text(phonemes)

            # تحويل التمثيل الطيفي إلى صوت باستخدام HIFIGAN
            waveform = self.vocoder.decode_batch(mel_spec)

            # تحويل المصفوفة إلى مصفوفة numpy
            audio = waveform.squeeze().cpu().numpy()

            return audio
        except Exception as e:
            print(f"خطأ في توليد الصوت: {str(e)}")
            return None

    def save_audio(self, audio, filename, sample_rate=22050):
        """
        حفظ الصوت المُوَلَّد في ملف

        Args:
            audio (numpy.ndarray): الصوت المُوَلَّد
            filename (str): اسم الملف
            sample_rate (int): معدل العينة
        """
        if audio is not None:
            # حفظ الصوت بصيغة WAV
            torchaudio.save(filename, torch.tensor(audio).unsqueeze(0), sample_rate)
            print(f"تم حفظ الصوت في: {filename}")
