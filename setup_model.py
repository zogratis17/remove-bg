"""
Model Setup Script
This script downloads the rembg AI model to the project's models folder.
Run this once to pre-download the model, then the Streamlit app will use it directly.
"""

import os
import sys
from rembg import remove
from PIL import Image
import io

def setup_model():
    """Download and cache the rembg model"""
    
    # Set model cache directory to project folder
    project_dir = os.path.dirname(os.path.abspath(__file__))
    model_cache_dir = os.path.join(project_dir, "models")
    os.environ['U2NET_HOME'] = model_cache_dir
    os.makedirs(model_cache_dir, exist_ok=True)
    
    print("🔄 Downloading rembg AI model...")
    print(f"📁 Model will be saved to: {model_cache_dir}")
    print()
    
    try:
        dummy_img = Image.new('RGB', (100, 100), color='white')
        
        print("⏳ Downloading model (this may take 2-5 minutes)...")
        print("   Model size: ~340MB")
        print()
        
        result = remove(dummy_img)
        
        print()
        print("✅ Model downloaded successfully!")
        print(f"📁 Location: {model_cache_dir}")
        print()
        print("You can now run the Streamlit app without waiting for model download:")
        print("   streamlit run app.py")
        print()
        return True
        
    except Exception as e:
        print(f"❌ Error downloading model: {str(e)}")
        return False

if __name__ == "__main__":
    success = setup_model()
    sys.exit(0 if success else 1)
