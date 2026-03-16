import os
import io
import json
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

generation_config = {
  "temperature": 0.2,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "application/json",
}

model = genai.GenerativeModel(
  model_name="gemini-2.0-flash", 
  generation_config=generation_config,
  system_instruction="You are a Senior ISO-Certified Safety Auditor. Analyze campus images. Identify hazards. Rate severity 1-10. Crucially, cite relevant National Building Code (NBC) 2016 standards (e.g., Part 4 for Fire, Part 6 for Structural). Return ONLY a JSON object with these keys: hazard_type, severity_score, legal_citation, description, priority_action, professional_email_draft."
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/audit', methods=['POST'])
def audit():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "Empty file"}), 400

    try:
        # Save the file locally first
        from werkzeug.utils import secure_filename
        import datetime
        import uuid
        
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        upload_folder = os.path.join(app.root_path, 'static', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, unique_filename)
        file.save(file_path)

        # Re-open for Gemini
        image = Image.open(file_path)
        if image.mode != 'RGB':
            image = image.convert('RGB')
            
        print("Sending to Gemini...")
        try:
            print(f"API Key Status: {'SET' if os.environ.get('GEMINI_API_KEY') else 'NOT SET'}")
            response = model.generate_content([image, "Analyze this image for safety hazards."])
            text = response.text
            print("Gemini response received successfully")
        except Exception as api_error:
            print(f"Gemini API Error: {type(api_error).__name__}: {str(api_error)}")
            import traceback
            traceback.print_exc()
            raise api_error
        
        text = response.text
        # Use regex to find the JSON object within the response
        import re
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            json_str = match.group(0)
            result = json.loads(json_str)
            print("Successfully extracted JSON.")
            
            # Inject metadata and user inputs into the response
            result['image_url'] = f"/static/uploads/{unique_filename}"
            result['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %I:%M %p")
            
            # Retrieve optional user data from form
            user_description = request.form.get('user_description', '').strip()
            if user_description:
                result['user_description'] = user_description
                
            lat = request.form.get('latitude')
            lng = request.form.get('longitude')
            if lat and lng:
                result['latitude'] = lat
                result['longitude'] = lng
            
            return jsonify(result)
        else:
            print("Could not find JSON in response:", text)
            raise ValueError("No JSON object found in response")
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
