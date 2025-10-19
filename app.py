import streamlit as st
from PIL import Image
import io
from rembg import remove
import os

# Set model cache directory to project folder
project_dir = os.path.dirname(os.path.abspath(__file__))
model_cache_dir = os.path.join(project_dir, "models")
os.environ['U2NET_HOME'] = model_cache_dir
os.makedirs(model_cache_dir, exist_ok=True)

# Suppress TensorFlow/ONNX warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Page configuration
st.set_page_config(
    page_title="Background Remover",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Cache the remove function to avoid reloading the model
@st.cache_resource
def load_model():
    """Load the rembg model once and cache it"""
    return remove

# Title and description
st.title("🎨 Background Remover")
st.markdown("Remove backgrounds from images instantly using AI!")

# Load model on app start (cached)
with st.spinner("🔄 Loading AI model... (one-time setup)"):
    remove_func = load_model()

st.success("✅ Model loaded and ready!")

# Initialize session state
if 'processed_image' not in st.session_state:
    st.session_state.processed_image = None
if 'original_image' not in st.session_state:
    st.session_state.original_image = None
if 'bg_color' not in st.session_state:
    st.session_state.bg_color = "transparent"

def apply_background_color(image_with_alpha, bg_color):
    """Apply background color to image with alpha channel"""
    if bg_color == "transparent":
        return image_with_alpha
    
    if image_with_alpha.mode != 'RGBA':
        image_with_alpha = image_with_alpha.convert('RGBA')
    
    background = Image.new('RGB', image_with_alpha.size, bg_color)
    background.paste(image_with_alpha, mask=image_with_alpha.split()[3])
    return background

# File uploader
st.subheader("📤 Upload Image")
uploaded_file = st.file_uploader(
    "Choose an image file",
    type=["jpg", "jpeg", "png", "bmp", "gif"],
    help="Supported formats: JPG, PNG, BMP, GIF"
)

if uploaded_file is not None:
    original_image = Image.open(uploaded_file)
    st.session_state.original_image = original_image
    
    # Background color selection
    st.subheader("🎨 Background Color Options")
    col_color1, col_color2, col_color3 = st.columns(3)
    
    with col_color1:
        bg_option = st.radio(
            "Choose background:",
            ["transparent", "white", "black", "custom"],
            key="bg_option"
        )
    
    if bg_option == "custom":
        with col_color2:
            custom_color = st.color_picker("Pick a color", "#FFFFFF")
        st.session_state.bg_color = custom_color
    else:
        st.session_state.bg_color = bg_option
    
    # Process button
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
    with col_btn1:
        if st.button("🚀 Remove Background", use_container_width=True):
            with st.spinner("⏳ Processing image... Please wait"):
                try:
                    processed = remove_func(original_image)
                    st.session_state.processed_image = processed
                    st.success("✅ Background removed successfully!")
                except Exception as e:
                    st.error(f"❌ Error processing image: {str(e)}")
    
    with col_btn2:
        if st.button("🗑️ Clear All", use_container_width=True):
            st.session_state.processed_image = None
            st.session_state.original_image = None
            st.session_state.bg_color = "transparent"
            st.rerun()

# Display images side by side
if st.session_state.original_image is not None or st.session_state.processed_image is not None:
    st.markdown("---")
    st.subheader("📸 Preview")
    
    col_img1, col_img2 = st.columns(2)
    
    if st.session_state.original_image is not None:
        with col_img1:
            st.markdown("**Original Image**")
            st.image(st.session_state.original_image, use_container_width=True)
    
    if st.session_state.processed_image is not None:
        with col_img2:
            st.markdown("**Processed Image**")
            
            display_image = st.session_state.processed_image
            if st.session_state.bg_color != "transparent":
                display_image = apply_background_color(st.session_state.processed_image, st.session_state.bg_color)
            
            st.image(display_image, use_container_width=True)
            
            img_byte_arr = io.BytesIO()
            
            if st.session_state.bg_color == "transparent":
                st.session_state.processed_image.save(img_byte_arr, format='PNG')
                file_name = "output.png"
                mime_type = "image/png"
            else:
                final_image = apply_background_color(st.session_state.processed_image, st.session_state.bg_color)
                final_image.save(img_byte_arr, format='PNG')
                file_name = f"output_{st.session_state.bg_color.replace('#', '')}.png"
                mime_type = "image/png"
            
            img_byte_arr.seek(0)
            
            st.download_button(
                label="📥 Download Processed Image",
                data=img_byte_arr,
                file_name=file_name,
                mime=mime_type,
                use_container_width=True
            )

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
        Made with love | Powered by rembg AI
    </div>
    """,
    unsafe_allow_html=True
)
