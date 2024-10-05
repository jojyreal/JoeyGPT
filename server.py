from flask import Flask, request, jsonify, render_template
import subprocess

app = Flask(__name__)

# This will hold the conversation history
conversation_history = []

@app.route('/')
def index():
    return render_template('index.html')  # HTML file for the JoeyGPT interface

@app.route('/send_prompt', methods=['POST'])
def send_prompt():
    data = request.json
    prompt = data.get('prompt', '')

    # Append user message to conversation history
    conversation_history.append(f'User: {prompt}')

    # Build the full prompt with conversation history
    full_prompt = "\n".join(conversation_history)  # Join history into a single prompt

    try:
        # Start the Ollama process and run the command
        process = subprocess.Popen(['ollama', 'run', 'llama3.2'], 
                                    stdin=subprocess.PIPE, 
                                    stdout=subprocess.PIPE, 
                                    stderr=subprocess.PIPE,
                                    text=True)

        # Send the full prompt to Ollama
        ai_response, _ = process.communicate(full_prompt)  # Communicate with the process

        # Append AI response to conversation history
        conversation_history.append(f'AI: {ai_response.strip()}')

        return jsonify({'response': ai_response.strip()})
    except Exception as e:
        return jsonify({'response': f'Error: {str(e)}'}), 500  # Return error if exception occurs

if __name__ == '__main__':
    app.run(debug=True)
