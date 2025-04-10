from flask import Blueprint, render_template, request, jsonify
import os
import uuid
from werkzeug.utils import secure_filename
from app.src.emo.emp_chains import EmoChains

main = Blueprint('main', __name__)

# 确保上传目录存在
UPLOAD_FOLDER = 'app/static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'status': 'error', 'message': '没有文件部分'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'status': 'error', 'message': '没有选择文件'}), 400
    
    if file and allowed_file(file.filename):
        # 生成安全的文件名
        filename = secure_filename(file.filename)
        # 添加随机字符串避免文件名冲突
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        file.save(file_path)
        
        return jsonify({
            'status': 'success',
            'filename': unique_filename,
            'file_path': file_path,
            'display_url': f'/static/uploads/{unique_filename}'
        })
    
    return jsonify({'status': 'error', 'message': '不允许的文件类型'}), 400

@main.route('/analyze', methods=['POST'])
def analyze_image():
    data = request.json
    file_path = data.get('file_path')
    text = data.get('text', '这张图片中人物的情绪是什么？请详细分析。')
    
    if not file_path or not os.path.exists(file_path):
        return jsonify({'status': 'error', 'message': '文件不存在'}), 400
    
    try:
        # 创建EmoChains实例并分析图片
        emo_chains = EmoChains(None)
        result = emo_chains.analyze_image_and_text_sync(text=text, image_path=file_path)
        
        return jsonify({
            'status': 'success',
            'result': result
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'分析过程中出错: {str(e)}'
        }), 500