# app.py
from flask import Flask, render_template, request, jsonify
from langflow_client import LangflowAPIClient

app = Flask(__name__)
api_client = LangflowAPIClient()

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        post_type = request.form.get('post_type')
        if post_type:
            result = api_client.get_social_analysis(post_type)
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)