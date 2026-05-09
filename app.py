from flask import Flask, render_template, request, jsonify
import re, random

app = Flask(__name__)

class ReaperEngine:
    @staticmethod
    def process(data, action, keyword=""):
        lines = [l.strip() for l in data.splitlines() if l.strip()]
        
        if action == "rem_dup": return sorted(list(set(lines)))
        if action == "get_dup": return [x for x in set(lines) if lines.count(x) > 1]
        if action == "sort": return sorted(lines)
        if action == "random": 
            random.shuffle(lines)
            return lines
        if action == "rem_empty": return lines
        if action == "rem_capture": return [l.split('|')[0].strip() if '|' in l else l for l in lines]
        
        if action == "email_to_user":
            new_lines = []
            for l in lines:
                if ":" in l:
                    parts = l.split(":", 1)
                    user = parts[0].split("@")[0]
                    new_lines.append(f"{user}:{parts[1]}")
            return new_lines

        if action == "extract_email":
            full_text = "\n".join(lines)
            return re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}', full_text)

        if action == "filter":
            return [l for l in lines if keyword.lower() in l.lower()]

        return lines

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/process', methods=['POST'])
def api_process():
    req = request.json
    res = ReaperEngine.process(req['data'], req['action'], req.get('keyword', ''))
    return jsonify({"result": "\n".join(res), "count": len(res)})

if __name__ == '__main__':
    app.run(debug=True)
