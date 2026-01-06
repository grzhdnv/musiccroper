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


def crop_pdf_margins(input_path, output_path, top=10, right=10, bottom=10, left=10):
    """
    Crop margins from a PDF file with individual margin control
    
    Args:
        input_path: Path to input PDF file
        output_path: Path to save cropped PDF
        top: Percentage of margin to crop from top (default: 10%)
        right: Percentage of margin to crop from right (default: 10%)
        bottom: Percentage of margin to crop from bottom (default: 10%)
        left: Percentage of margin to crop from left (default: 10%)
    """
    reader = PdfReader(input_path)
    writer = PdfWriter()
    
    for page in reader.pages:
        # Get the page dimensions
        media_box = page.mediabox
        width = float(media_box.width)
        height = float(media_box.height)
        
        # Get rotation and normalize it
        rotation = page.rotation % 360

        # Calculate crop margins based on rotation
        if rotation == 90:
            # 90 degrees clockwise
            # Visual Top -> Physical Left
            # Visual Right -> Physical Top
            # Visual Bottom -> Physical Right
            # Visual Left -> Physical Bottom
            crop_physical_left = width * (top / 100)
            crop_physical_right = width * (bottom / 100)
            crop_physical_bottom = height * (left / 100)
            crop_physical_top = height * (right / 100)
        elif rotation == 180:
            # 180 degrees
            # Visual Top -> Physical Bottom
            # Visual Right -> Physical Left
            # Visual Bottom -> Physical Top
            # Visual Left -> Physical Right
            crop_physical_left = width * (right / 100)
            crop_physical_right = width * (left / 100)
            crop_physical_bottom = height * (top / 100)
            crop_physical_top = height * (bottom / 100)
        elif rotation == 270:
            # 270 degrees clockwise
            # Visual Top -> Physical Right
            # Visual Right -> Physical Bottom
            # Visual Bottom -> Physical Left
            # Visual Left -> Physical Top
            crop_physical_left = width * (bottom / 100)
            crop_physical_right = width * (top / 100)
            crop_physical_bottom = height * (right / 100)
            crop_physical_top = height * (left / 100)
        else:
            # 0 degrees (normal)
            crop_physical_left = width * (left / 100)
            crop_physical_right = width * (right / 100)
            crop_physical_bottom = height * (bottom / 100)
            crop_physical_top = height * (top / 100)
        
        # Set new page boundaries (crop margins)
        page.mediabox.lower_left = (crop_physical_left, crop_physical_bottom)
        page.mediabox.upper_right = (width - crop_physical_right, height - crop_physical_top)
        
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
    """Handle PDF file upload for preview"""
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
        
        # Return to index with filename for preview
        return render_template('index.html', uploaded_filename=filename)
    else:
        flash('Invalid file type. Please upload a PDF file.')
        return redirect(url_for('index'))


@app.route('/preview/<filename>')
def preview_pdf(filename):
    """Serve uploaded PDF for preview"""
    filename = secure_filename(filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    if os.path.exists(file_path):
        return send_file(file_path, mimetype='application/pdf')
    else:
        flash('File not found')
        return redirect(url_for('index'))


@app.route('/crop', methods=['POST'])
def crop_pdf():
    """Handle PDF cropping with individual margins"""
    filename = request.form.get('filename')
    
    if not filename:
        flash('No file specified')
        return redirect(url_for('index'))
    
    filename = secure_filename(filename)
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    if not os.path.exists(input_path):
        flash('File not found')
        return redirect(url_for('index'))
    
    try:
        # Get individual margin values from form and validate
        top = float(request.form.get('top', 10))
        right = float(request.form.get('right', 10))
        bottom = float(request.form.get('bottom', 10))
        left = float(request.form.get('left', 10))
        
        # Validate margin values are within acceptable range (0-50%)
        for margin_name, margin_value in [('top', top), ('right', right), ('bottom', bottom), ('left', left)]:
            if not (0 <= margin_value <= 50):
                flash(f'Invalid {margin_name} margin value. Must be between 0 and 50%.')
                return redirect(url_for('index'))
        
        # Generate output filename
        output_filename = f"cropped_{filename}"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        
        # Crop the PDF with individual margins
        crop_pdf_margins(input_path, output_path, top, right, bottom, left)
        
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


@app.route('/about')
def about():
    """About page with information about the app"""
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
