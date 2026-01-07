# إعدادات الصوت
AUDIO_SAMPLE_RATE = 22050
AUDIO_CHANNELS = 1

# إعدادات النموذج
MODEL_CONFIG = {
    "g2p_model": "speechbrain/tts_models/arabic-tacotron2-collab",
    "tts_model": "speechbrain/tts_models/arabic-tacotron2-collab",
    "vocoder_model": "speechbrain/tts_models/arabic-hifigan-collab"
}

# إعدادات الواجهة
INTERFACE_CONFIG = {
    "title": "تطبيق توليدي للأصوات العربية",
    "server_name": "0.0.0.0",
    "server_port": 7860
}
