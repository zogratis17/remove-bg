# Background Remover

A simple and elegant Streamlit web application that removes backgrounds from images using AI-powered background removal.

## Features

✨ **Image Upload**: Upload images in JPG, PNG, BMP, or GIF format
🎯 **AI Background Removal**: Uses advanced rembg library for accurate background removal
👀 **Live Preview**: See the processed image before downloading
🎨 **Multiple Background Colors**: Choose transparent, white, black, or custom colors
📥 **Easy Download**: Download the processed image with one click
🗑️ **Clear Functionality**: Reset and start over with a new image

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone the repository**:
```bash
git clone https://github.com/zogratis17/remove-bg.git
cd remove-bg
```

2. **Create a virtual environment** (optional but recommended):
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

## Running the App

### Option 1: Pre-download the Model (Recommended for faster startup)

1. Download the AI model (one-time, takes 2-5 minutes):
```bash
python setup_model.py
```

2. After download completes, run the Streamlit app:
```bash
streamlit run app.py
```

### Option 2: Let the app download the model on first run

1. Run the Streamlit app directly (model downloads on first use):
```bash
streamlit run app.py
```

The app will open in your default web browser at `http://localhost:8501`

## Usage

1. **Upload an Image**: Click on the upload area and select an image file
2. **Choose Background Color**: Select from transparent, white, black, or pick a custom color
3. **Remove Background**: Click the "Remove Background" button
4. **Preview**: See the processed image with your chosen background
5. **Download**: Click the "Download Processed Image" button to save the file
6. **Clear**: Use the "Clear All" button to process another image

## Supported Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- GIF (.gif)

## Background Color Options

- **Transparent** (PNG with alpha channel) - Preserves transparency
- **White** - Solid white background
- **Black** - Solid black background
- **Custom** - Pick any color you prefer using the color picker

## Technical Details

- **Framework**: Streamlit
- **AI Library**: rembg (Remove Background)
- **Image Processing**: PIL (Python Imaging Library)
- **Model**: U2-Net trained on COCO dataset

## Notes

- The AI model is ~340MB and only needs to be downloaded once
- Pre-downloading the model using `setup_model.py` speeds up app startup
- Processing time depends on image size and your system's capabilities
- Output images are saved in PNG format to preserve quality
- Model is cached locally in the `models/` folder

## File Structure

```
remove-bg/
├── app.py              # Main Streamlit application
├── setup_model.py      # Model download script
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── models/            # AI model folder (created after setup)
└── .gitignore         # Git ignore rules
```

## License

MIT License - Feel free to use this project for personal and commercial purposes.

## Author

Created with ❤️

---

Enjoy removing backgrounds! 🎨