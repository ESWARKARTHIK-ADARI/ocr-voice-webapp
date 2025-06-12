import streamlit as st
import cv2
import pytesseract
from gtts import gTTS
from io import BytesIO
import base64
import os
import numpy as np

# Set Tesseract path if needed (for Windows)
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

st.set_page_config(page_title="Handwriting to Voice App", layout="centered")

st.title("📝 Handwritten Text to 🎙️ Voice")
st.markdown("Upload a handwritten image. The app will extract text and speak it out loud!")

uploaded_file = st.file_uploader("📤 Upload Handwritten Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Convert file to OpenCV image
    file_bytes = uploaded_file.read()
    np_arr = bytearray(file_bytes)
    np_img = cv2.imdecode(np.frombuffer(file_bytes, np.uint8), cv2.IMREAD_COLOR)

    st.image(uploaded_file, caption="🖼️ Uploaded Image", use_column_width=True)

    # Preprocess and OCR
    gray = cv2.cvtColor(np_img, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    text = pytesseract.image_to_string(gray)

    st.subheader("📄 Extracted Text:")
    st.text_area("Detected Text", value=text, height=200)

    if text.strip():
        # Convert to speech using gTTS
        tts = gTTS(text=text)
        tts_bytes = BytesIO()
        tts.write_to_fp(tts_bytes)
        tts_bytes.seek(0)

        # Base64 encode audio for Streamlit player
        b64 = base64.b64encode(tts_bytes.read()).decode()
        audio_html = f"""
            <audio controls autoplay>
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
        """
        st.markdown("🔊 **Speech Output:**", unsafe_allow_html=True)
        st.markdown(audio_html, unsafe_allow_html=True)
    else:
        st.warning("⚠️ No text could be extracted. Try a clearer image.")
