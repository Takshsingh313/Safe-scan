<<<<<<< HEAD
# Safe-Scan: Campus Safety Dashboard

**Safe-Scan** is a rapid-response safety dashboard that allows anyone on a university campus to report infrastructure hazards instantly using their phone camera, and automatically generates a professional, code-compliant safety audit.

## The Problem
Maintaining safety across a large university campus is challenging. There are minor structural cracks, exposed wires, and blocked fire exits that thousands of students walk past every day. The current reporting process is often slow, manual, and most students don't know the actual safety laws being broken, making it difficult for maintenance teams to prioritize effectively.

## Our Solution
We built a "Command Center" web app that turns a normal photo into an official, ISO-certified audit report. 

1. **Snap a photo** of a broken handrail or exposed wire.
2. **Upload it** to the Safe-Scan dashboard.
3. Our backend uses **Google Gemini 2.5 Flash** to analyze the image. 
4. Gemini acts as a safety inspector: it identifies the hazard, scores the severity out of 10, cites the exact **National Building Code (NBC) 2016** law that is being violated, and drafts an email ticket for the maintenance team.
5. The dashboard instantly updates with the new report, adjusts the campus safety score, and drops a red pin on the live map.

## Tech Stack
- **Backend:** Python + Flask
- **AI Integration:** Google Generative AI (`gemini-2.5-flash`). Utilized for its multimodal image analysis and capability to return strict JSON data.
- **Frontend:** HTML, Tailwind CSS, & DaisyUI for the dark-mode aesthetic.
- **Map:** Leaflet.js

## How to Run It Locally

1. Install the requirements:
   ```bash
   pip install -r requirements.txt
   ```
2. Create a `.env` file and add your Gemini API Key:
   ```env
   GEMINI_API_KEY=your_api_key
   ```
3. Run the Flask server:
   ```bash
   python app.py
   ```
4. Open your browser and go to `http://127.0.0.1:5000`
=======
# Safe-scan
>>>>>>> 9af3df73d9662163351253a12a22e62bbdac103d
