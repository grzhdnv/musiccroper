# Music Score Cropper

A web application that crops margins from PDF music scores for better viewing on iPad and tablet screens.

## Features

- 🎵 Simple web interface for uploading PDF scores
- ✂️ Automatic margin cropping with adjustable percentage
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
pip install -r requirements.txt
```

## Usage

1. Start the Flask application:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

3. Upload a PDF music score, adjust the margin percentage (default is 10%), and click "Crop PDF"

4. Download your cropped PDF with enlarged notes for better viewing

## How it Works

The application removes unnecessary margins from PDF files by:
1. Reading each page of the PDF
2. Calculating the specified margin percentage
3. Cropping the margins from all four sides
4. Generating a new PDF with the cropped pages

## Configuration

You can modify the following settings in `app.py`:
- `MAX_CONTENT_LENGTH`: Maximum file upload size (default: 16MB)
- `margin_percent`: Default margin to crop (default: 10%)

## Technology Stack

- **Backend**: Flask (Python web framework)
- **PDF Processing**: PyPDF2
- **Frontend**: HTML5, CSS3, JavaScript
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
