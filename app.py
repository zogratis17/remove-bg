import streamlit as stimport streamlit as st

from PIL import Imagefrom PIL import Image

import ioimport io

from rembg import removefrom rembg import remove

import osimport os



# Set model cache directory to project folder# Set model cache directory to project folder

project_dir = os.path.dirname(os.path.abspath(__file__))project_dir = os.path.dirname(os.path.abspath(__file__))

model_cache_dir = os.path.join(project_dir, "models")model_cache_dir = os.path.join(project_dir, "models")

os.environ['U2NET_HOME'] = model_cache_diros.environ['U2NET_HOME'] = model_cache_dir

os.makedirs(model_cache_dir, exist_ok=True)os.makedirs(model_cache_dir, exist_ok=True)



# Suppress TensorFlow/ONNX warnings# Suppress TensorFlow/ONNX warnings

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'



# Page configuration# Page configuration

st.set_page_config(st.set_page_config(

    page_title="Background Remover",    page_title="Background Remover",

    page_icon="🎨",    page_icon="🎨",

    layout="wide",    layout="wide",

    initial_sidebar_state="collapsed"    initial_sidebar_state="collapsed"

))



# Cache the remove function to avoid reloading the model# Cache the remove function to avoid reloading the model

@st.cache_resource@st.cache_resource

def load_model():def load_model():

    """Load the rembg model once and cache it"""    """Load the rembg model once and cache it"""

    # This will download the model on first run    # This will download the model on first run

    return remove    return remove



# Title and description# Title and description

st.title("🎨 Background Remover")st.title("🎨 Background Remover")

st.markdown("Remove backgrounds from images instantly using AI!")st.markdown("Remove backgrounds from images instantly using AI!")



# Load model on app start (cached)# Load model on app start (cached)

with st.spinner("🔄 Loading AI model... (one-time setup)"):with st.spinner("🔄 Loading AI model... (one-time setup)"):

    remove_func = load_model()    remove_func = load_model()



st.success("✅ Model loaded and ready!")st.success("✅ Model loaded and ready!")



# Initialize session state for processed image and original image# Initialize session state for processed image and original image

if 'processed_image' not in st.session_state:if 'processed_image' not in st.session_state:

    st.session_state.processed_image = None    st.session_state.processed_image = None

if 'original_image' not in st.session_state:if 'original_image' not in st.session_state:

    st.session_state.original_image = None    st.session_state.original_image = None

if 'bg_color' not in st.session_state:if 'bg_color' not in st.session_state:

    st.session_state.bg_color = "transparent"    st.session_state.bg_color = "transparent"



# Helper function to apply background color# Helper function to apply background color

def apply_background_color(image_with_alpha, bg_color):def apply_background_color(image_with_alpha, bg_color):

    """Apply background color to image with alpha channel"""    """Apply background color to image with alpha channel"""

    if bg_color == "transparent":    if bg_color == "transparent":

        return image_with_alpha        return image_with_alpha

        

    # Convert to RGB if needed    # Convert to RGB if needed

    if image_with_alpha.mode != 'RGBA':    if image_with_alpha.mode != 'RGBA':

        image_with_alpha = image_with_alpha.convert('RGBA')        image_with_alpha = image_with_alpha.convert('RGBA')

        

    # Create a new image with the selected background color    # Create a new image with the selected background color

    background = Image.new('RGB', image_with_alpha.size, bg_color)    background = Image.new('RGB', image_with_alpha.size, bg_color)

    background.paste(image_with_alpha, mask=image_with_alpha.split()[3])    background.paste(image_with_alpha, mask=image_with_alpha.split()[3])

    return background    return background



# File uploader# File uploader

st.subheader("📤 Upload Image")st.subheader("📤 Upload Image")

uploaded_file = st.file_uploader(uploaded_file = st.file_uploader(

    "Choose an image file",    "Choose an image file",

    type=["jpg", "jpeg", "png", "bmp", "gif"],    type=["jpg", "jpeg", "png", "bmp", "gif"],

    help="Supported formats: JPG, PNG, BMP, GIF"    help="Supported formats: JPG, PNG, BMP, GIF"

))



if uploaded_file is not None:if uploaded_file is not None:

    original_image = Image.open(uploaded_file)    original_image = Image.open(uploaded_file)

    st.session_state.original_image = original_image    st.session_state.original_image = original_image

        

    # Background color selection    # Background color selection

    st.subheader("🎨 Background Color Options")    st.subheader("🎨 Background Color Options")

    col_color1, col_color2, col_color3 = st.columns(3)    col_color1, col_color2, col_color3 = st.columns(3)

        

    with col_color1:    with col_color1:

        bg_option = st.radio(        bg_option = st.radio(

            "Choose background:",            "Choose background:",

            ["transparent", "white", "black", "custom"],            ["transparent", "white", "black", "custom"],

            key="bg_option"            key="bg_option"

        )        )

        

    custom_color = None    custom_color = None

    if bg_option == "custom":    if bg_option == "custom":

        with col_color2:        with col_color2:

            custom_color = st.color_picker("Pick a color", "#FFFFFF")            custom_color = st.color_picker("Pick a color", "#FFFFFF")

        st.session_state.bg_color = custom_color        st.session_state.bg_color = custom_color

    else:    else:

        st.session_state.bg_color = bg_option        st.session_state.bg_color = bg_option

        

    # Process button    # Process button

    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])

    with col_btn1:    with col_btn1:

        if st.button("🚀 Remove Background", use_container_width=True):        if st.button("🚀 Remove Background", use_container_width=True):

            with st.spinner("⏳ Processing image... Please wait"):            with st.spinner("⏳ Processing image... Please wait"):

                try:                try:

                    # Remove background using cached model                    # Remove background using cached model

                    processed = remove_func(original_image)                    processed = remove_func(original_image)

                    st.session_state.processed_image = processed                    st.session_state.processed_image = processed

                    st.success("✅ Background removed successfully!")                    st.success("✅ Background removed successfully!")

                except Exception as e:                except Exception as e:

                    st.error(f"❌ Error processing image: {str(e)}")                    st.error(f"❌ Error processing image: {str(e)}")

        

    with col_btn2:    with col_btn2:

        if st.button("🗑️ Clear All", use_container_width=True):        if st.button("🗑️ Clear All", use_container_width=True):

            st.session_state.processed_image = None            st.session_state.processed_image = None

            st.session_state.original_image = None            st.session_state.original_image = None

            st.session_state.bg_color = "transparent"            st.session_state.bg_color = "transparent"

            st.rerun()            st.rerun()



# Display images side by side# Display images side by side

if st.session_state.original_image is not None or st.session_state.processed_image is not None:if st.session_state.original_image is not None or st.session_state.processed_image is not None:

    st.markdown("---")    st.markdown("---")

    st.subheader("📸 Preview")    st.subheader("📸 Preview")

        

    col_img1, col_img2 = st.columns(2)    col_img1, col_img2 = st.columns(2)

        

    # Display original image    # Display original image

    if st.session_state.original_image is not None:    if st.session_state.original_image is not None:

        with col_img1:        with col_img1:

            st.markdown("**Original Image**")            st.markdown("**Original Image**")

            st.image(st.session_state.original_image, use_container_width=True)            st.image(st.session_state.original_image, use_container_width=True)

        

    # Display processed image and download button    # Display processed image and download button

    if st.session_state.processed_image is not None:    if st.session_state.processed_image is not None:

        with col_img2:        with col_img2:

            st.markdown("**Processed Image**")            st.markdown("**Processed Image**")

                        

            # Apply background color to display            # Apply background color to display

            display_image = st.session_state.processed_image            display_image = st.session_state.processed_image

            if st.session_state.bg_color != "transparent":            if st.session_state.bg_color != "transparent":

                display_image = apply_background_color(st.session_state.processed_image, st.session_state.bg_color)                display_image = apply_background_color(st.session_state.processed_image, st.session_state.bg_color)

                        

            st.image(display_image, use_container_width=True)            st.image(display_image, use_container_width=True)

                        

            # Prepare download based on background selection            # Prepare download based on background selection

            img_byte_arr = io.BytesIO()            img_byte_arr = io.BytesIO()

                        

            if st.session_state.bg_color == "transparent":            if st.session_state.bg_color == "transparent":

                # Save as PNG for transparency                # Save as PNG for transparency

                st.session_state.processed_image.save(img_byte_arr, format='PNG')                st.session_state.processed_image.save(img_byte_arr, format='PNG')

                file_name = "output.png"                file_name = "output.png"

                mime_type = "image/png"                mime_type = "image/png"

            else:            else:

                # Apply background and save as PNG or JPG                # Apply background and save as PNG or JPG

                final_image = apply_background_color(st.session_state.processed_image, st.session_state.bg_color)                final_image = apply_background_color(st.session_state.processed_image, st.session_state.bg_color)

                final_image.save(img_byte_arr, format='PNG')                final_image.save(img_byte_arr, format='PNG')

                file_name = f"output_{st.session_state.bg_color.replace('#', '')}.png"                file_name = f"output_{st.session_state.bg_color.replace('#', '')}.png"

                mime_type = "image/png"                mime_type = "image/png"

                        

            img_byte_arr.seek(0)            img_byte_arr.seek(0)

                        

            # Download button            # Download button

            st.download_button(            st.download_button(

                label="📥 Download Processed Image",                label="📥 Download Processed Image",

                data=img_byte_arr,                data=img_byte_arr,

                file_name=file_name,                file_name=file_name,

                mime=mime_type,                mime=mime_type,

                use_container_width=True                use_container_width=True

            )            )





# Footer# Footer

st.markdown("---")st.markdown("---")

st.markdown(st.markdown(

    """    """

    <div style='text-align: center; color: gray;'>    <div style='text-align: center; color: gray;'>

        Made with ❤️ | Powered by rembg AI        Made with ❤️ | Powered by rembg AI

    </div>    </div>

    """,    """,

    unsafe_allow_html=True    unsafe_allow_html=True

))

