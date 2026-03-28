# Music Score Cropper

A web application that crops margins from PDF music scores for better viewing on iPad and tablet screens.

## Features

- 🎵 Simple web interface for uploading PDF scores
- 👁️ Interactive PDF preview with page navigation before cropping
- ✂️ Individual margin control (top, right, bottom, left) with draggable crop boundaries
- 🔄 Correct handling of rotated PDF pages (0°, 90°, 180°, 270°)
- 📱 Optimized for better viewing on tablets and iPads
- 🚀 Fast processing with PyPDF2
- 🔒 Secure - uploaded files are automatically deleted after processing

## Installation

1. Clone the repository:
```bash
git clone https://github.com/grzhdnv/musiccroper.git
cd musiccroper
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
# Requires Python 3.12 latest
pip install -r requirements.txt
```

## Usage

1. Start the Flask application:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5001
```

3. Upload a PDF music score and use the interactive preview to set per-side margins (top, right, bottom, left) by dragging crop boundaries or typing values directly

4. Click "Crop PDF" to process and download your cropped PDF with enlarged notes for better viewing

## How it Works

The application removes unnecessary margins from PDF files by:
1. Accepting a PDF upload and displaying a live preview via PDF.js
2. Allowing independent margin control for each side (0–50%) with real-time overlay feedback
3. Reading each page of the PDF and applying the chosen margins, respecting page rotation
4. Generating and serving a new PDF with the cropped pages, then deleting the temporary files

## Configuration

You can modify the following settings in `app.py`:
- `MAX_CONTENT_LENGTH`: Maximum file upload size (default: 16 MB)
- Default margin values passed to `crop_pdf_margins`: top, right, bottom, left (each 0–50%, default: 10%)

## Technology Stack

- **Backend**: Flask 3.0.0 (Python web framework)
- **PDF Processing**: PyPDF2 3.0.1 (margin cropping and rotation handling)
- **PDF Preview**: PDF.js (client-side in-browser rendering)
- **Image Processing**: pdf2image 1.16.3, Pillow 10.1.0
- **Frontend**: HTML5, CSS3, JavaScript (Canvas API for overlay visualization)
- **Styling**: Custom CSS with gradient design

## Project Structure

```
musiccroper/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/            
│   ├── index.html        # Main upload page
│   └── about.html        # About page
├── static/
│   └── css/
│       └── style.css     # Application styling
├── uploads/              # Temporary upload directory (created automatically)
└── output/               # Temporary output directory (created automatically)
```

## License

This project is open source and available for use.
