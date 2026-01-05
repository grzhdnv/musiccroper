import os
from flask import Flask, render_template, request, send_file, redirect, url_for, flash
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader, PdfWriter
import io

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'output'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

# Create necessary directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)


def allowed_file(filename):
    """Check if file has an allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def crop_pdf_margins(input_path, output_path, margin_percent=10):
    """
    Crop margins from a PDF file
    
    Args:
        input_path: Path to input PDF file
        output_path: Path to save cropped PDF
        margin_percent: Percentage of margin to crop from each side (default: 10%)
    """
    reader = PdfReader(input_path)
    writer = PdfWriter()
    
    for page in reader.pages:
        # Get the page dimensions
        media_box = page.mediabox
        width = float(media_box.width)
        height = float(media_box.height)
        
        # Calculate crop margins
        crop_x = width * (margin_percent / 100)
        crop_y = height * (margin_percent / 100)
        
        # Set new page boundaries (crop margins)
        page.mediabox.lower_left = (crop_x, crop_y)
        page.mediabox.upper_right = (width - crop_x, height - crop_y)
        
        writer.add_page(page)
    
    # Write the cropped PDF to output file
    with open(output_path, 'wb') as output_file:
        writer.write(output_file)


@app.route('/')
def index():
    """Render the main upload page"""
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle PDF file upload and cropping"""
    if 'file' not in request.files:
        flash('No file selected')
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No file selected')
        return redirect(url_for('index'))
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_path)
        
        # Get margin percentage from form
        margin_percent = int(request.form.get('margin', 10))
        
        # Generate output filename
        output_filename = f"cropped_{filename}"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        
        try:
            # Crop the PDF
            crop_pdf_margins(input_path, output_path, margin_percent)
            
            # Clean up uploaded file
            os.remove(input_path)
            
            return send_file(
                output_path,
                as_attachment=True,
                download_name=output_filename,
                mimetype='application/pdf'
            )
        except Exception as e:
            flash(f'Error processing PDF: {str(e)}')
            return redirect(url_for('index'))
    else:
        flash('Invalid file type. Please upload a PDF file.')
        return redirect(url_for('index'))


@app.route('/about')
def about():
    """About page with information about the app"""
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
