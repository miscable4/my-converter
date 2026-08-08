import streamlit as st
import pytesseract
from PIL import Image
from docx import Document
from pdf2docx import Converter
import os
import io

# 1. Page Configuration
st.set_page_config(
    page_title="Universal Converter · Change is constant. Simple file tool.", 
    page_icon="📄", 
    layout="centered"
    st.markdown(
    '<meta name="google-site-verification" content="universal-converter-verification-tag" />', 
    unsafe_allow_html=True
)
st.title("📄 Universal Word Document Converter")
st.write("Upload any PDF or image with text to instantly convert it into a Word (.docx) file.")

# 2. Upload Interface
uploaded_file = st.file_uploader("Choose a file (PDF, PNG, JPG, JPEG, WEBP)", type=["pdf", "png", "jpg", "jpeg", "webp"])

if uploaded_file is not None:
    file_name = uploaded_file.name
    base_name, extension = os.path.splitext(file_name)
    extension = extension.lower()
    
    st.info(f"🔄 Processing '{file_name}'... Please wait.")
    docx_buffer = io.BytesIO()
    success = False

    # 3. PDF Conversion Logic
    if extension == ".pdf":
        try:
            with open("temp_input.pdf", "wb") as f:
                f.write(uploaded_file.getbuffer())
            cv = Converter("temp_input.pdf")
            cv.convert("temp_output.docx")
            cv.close()
            with open("temp_output.docx", "rb") as f:
                docx_buffer.write(f.read())
            os.remove("temp_input.pdf")
            os.remove("temp_output.docx")
            success = True
        except Exception as e:
            st.error(f"❌ Failed to parse PDF: {e}")

    # 4. Image OCR Logic
    elif extension in [".png", ".jpg", ".jpeg", ".webp"]:
        try:
            img = Image.open(uploaded_file)
            extracted_text = pytesseract.image_to_string(img)
            doc = Document()
            has_content = False
            for line in extracted_text.split('\n'):
                if line.strip():
                    doc.add_paragraph(line)
                    has_content = True
            if not has_content:
                doc.add_paragraph("[AI Note: No text detected.]")
            doc.save(docx_buffer)
            success = True
        except Exception as e:
            st.error(f"❌ Failed image OCR: {e}")

    # 5. Download Trigger
    if success:
        st.success("🎉 Conversion Complete!")
        st.download_button(
            label="📥 Download Word Document",
            data=docx_buffer.getvalue(),
            file_name=f"{base_name}_converted.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
