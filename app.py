from flask import Flask, request, jsonify
from QnA.model import phi3
from flask_cors import CORS, cross_origin

app = Flask(__name__)
path_to_data = '../data/'

CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

sample_ans = """
Hello Rajesh, I hope you are doing well. I am an expert assistant specializing in answering queries about a school resource accessible to parents. You are the parent of a student named Ravi at ABC School. I will use only the school's public resources to answer the questions. Responses should be concise and journalistic, not exceeding 80 words. If the answer is not found in the context, I will not provide an answer. I will respond as if generating answers directly from the school's public resources. I will use the same language as you are asking the question. If the context does not contain the requested information, I will state that the school does not have data on the matter. I will respond to Hi or Hello with a greeting. I will not provide personal opinions or advice or any sample questions.
"""


@app.route('/api/message', methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def get_message():
    if request.method == 'POST':
        # get last message from user
        message = request.json.get('messages')
        if message:
            # return jsonify({"text": sample_ans})
            response = phi3(message)
            return jsonify({"text": response})
        else:
            return jsonify({"error": "No query provided"})


@app.route('/api/test', methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def test():
    return jsonify({"text": "Hello World!"})
