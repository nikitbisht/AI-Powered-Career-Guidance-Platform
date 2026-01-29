"""
AI Career Mentor Chatbot Route
Provides streaming chat responses using LangChain with ChatOpenAI
"""

from flask import Blueprint, request, jsonify, Response
import json
from datetime import datetime

try:
    from backend.utils.langchain_utils import get_career_mentor_chain, generate_career_response
except ImportError as e:
    print(f"Warning: Langchain utils not available: {e}")
    get_career_mentor_chain = None
    generate_career_response = None

chatbot_bp = Blueprint('chatbot', __name__)

# Global conversation storage (in-memory for demo)
conversations = {}

@chatbot_bp.route('/message', methods=['POST'])
def send_message():
    """
    Send a message to the career mentor chatbot
    Expects: message (string), session_id (optional)
    Returns: AI response
    """
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        session_id = data.get('session_id', 'default')
        
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Initialize chain for this session if needed
        if session_id not in conversations:
            conversations[session_id] = get_career_mentor_chain()
        
        # Generate response
        response = generate_career_response(conversations[session_id], user_message)
        
        return jsonify({
            'success': True,
            'response': response,
            'timestamp': datetime.now().isoformat()
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Error processing message: {str(e)}'}), 500

@chatbot_bp.route('/stream', methods=['POST'])
def stream_message():
    """
    Send a message to the career mentor with streaming response (SSE)
    Expects: message (string), session_id (optional)
    Returns: Server-Sent Events stream
    """
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        session_id = data.get('session_id', 'default')
        
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Initialize chain for this session if needed
        if session_id not in conversations:
            conversations[session_id] = get_career_mentor_chain()
        
        def generate():
            """Generator for streaming response"""
            try:
                # Get response from LangChain
                response = generate_career_response(conversations[session_id], user_message)
                
                # Stream response character by character
                for char in response:
                    yield f"data: {json.dumps({'content': char})}\n\n"
                
                # Send completion signal
                yield f"data: {json.dumps({'status': 'complete'})}\n\n"
            
            except Exception as e:
                yield f"data: {json.dumps({'error': str(e)})}\n\n"
        
        return Response(generate(), mimetype='text/event-stream')
    
    except Exception as e:
        return jsonify({'error': f'Error processing message: {str(e)}'}), 500

@chatbot_bp.route('/sample', methods=['GET'])
def get_sample_response():
    """
    Get a sample chatbot response for demo
    """
    return jsonify({
        'success': True,
        'message': 'How can I improve my resume for a Data Science role?',
        'response': '''To improve your resume for a Data Science role, consider these key points:

1. **Technical Skills**: Prominently list programming languages (Python, R, SQL), machine learning frameworks (scikit-learn, TensorFlow), and data visualization tools (Tableau, Power BI).

2. **Quantifiable Results**: Include specific metrics from past projects. For example: "Improved model accuracy by 15%" or "Reduced data processing time by 40%".

3. **Relevant Projects**: Showcase 2-3 portfolio projects that demonstrate your data science capabilities. Include the problem, your approach, and results.

4. **Certifications**: Include relevant certifications like Google Data Analytics, AWS Certified ML, or Andrew Ng's Machine Learning course.

5. **Education**: List your degree in Computer Science, Statistics, Mathematics, or related fields. Highlight relevant coursework.

6. **Keywords**: Incorporate job description keywords like "predictive modeling", "statistical analysis", "data pipeline", "big data", etc.

Start with a strong summary highlighting your unique value proposition in data science!''',
        'timestamp': datetime.now().isoformat()
    }), 200

@chatbot_bp.route('/clear', methods=['POST'])
def clear_conversation():
    """
    Clear conversation history for a session
    """
    try:
        data = request.get_json()
        session_id = data.get('session_id', 'default')
        
        if session_id in conversations:
            del conversations[session_id]
        
        return jsonify({'success': True, 'message': 'Conversation cleared'}), 200
    
    except Exception as e:
        return jsonify({'error': f'Error clearing conversation: {str(e)}'}), 500
