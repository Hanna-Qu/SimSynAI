# 鏈湴寮€鍙戠幆澧冭缃寚鍗?

鏈寚鍗椾粙缁嶅浣曞湪瀹夸富鏈轰笂璁剧疆SimSynAI椤圭洰鐨勫紑鍙戠幆澧冿紝鍖呮嫭conda铏氭嫙鐜鍜屾湰鍦版湇鍔￠厤缃€?

## 鐜鍑嗗

### 1. 瀹夎Anaconda/Miniconda

**Windows:**
- 涓嬭浇骞跺畨瑁?[Anaconda](https://www.anaconda.com/products/distribution) 鎴?[Miniconda](https://docs.conda.io/en/latest/miniconda.html)
- 閲嶅惎缁堢鎴栧懡浠ゆ彁绀虹

**macOS:**
```bash
# 浣跨敤Homebrew瀹夎
brew install --cask anaconda
# 鎴栬€?
brew install --cask miniconda
```

**Linux:**
```bash
# 涓嬭浇Miniconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

# 瀹夎
bash Miniconda3-latest-Linux-x86_64.sh

# 閲嶆柊鍔犺浇shell閰嶇疆
source ~/.bashrc
```

### 2. 楠岃瘉conda瀹夎
```bash
conda --version
```

## 鍒涘缓寮€鍙戠幆澧?

### 鏂瑰紡1锛氫娇鐢╡nvironment.yml锛堟帹鑽愶級

```bash
# 1. 鍏嬮殕椤圭洰锛堝鏋滆繕娌℃湁鐨勮瘽锛?
git clone https://github.com/Hanna-Qu/SimSynAI.git
cd SimSynAI

# 2. 鍒涘缓conda鐜
conda env create -f environment.yml

# 3. 婵€娲荤幆澧?
conda activate simsynai

# 4. 楠岃瘉瀹夎
python --version
pip list
```

### 鏂瑰紡2锛氭墜鍔ㄥ垱寤虹幆澧?

```bash
# 1. 鍒涘缓鏂扮殑conda鐜
conda create -n simsynai python=3.11 -y

# 2. 婵€娲荤幆澧?
conda activate simsynai

# 3. 瀹夎鍩虹渚濊禆
conda install -c conda-forge fastapi uvicorn sqlalchemy -y

# 4. 瀹夎鍚庣渚濊禆
pip install -r backend/requirements.txt

# 5. 瀹夎寮€鍙戝伐鍏?
pip install black isort flake8 pytest pytest-cov
```

## 寮€鍙戠幆澧冮厤缃?

### 1. 鍚庣寮€鍙?

#### 1.1 鐜鍙橀噺閰嶇疆
鍒涘缓鍚庣鐜鍙橀噺鏂囦欢锛?
```bash
# 鍦╞ackend鐩綍涓嬪垱寤?env鏂囦欢
cd backend
cat > .env << EOF
# 鍩虹閰嶇疆
PROJECT_NAME=SimSynAI
SECRET_KEY=your_development_secret_key_here
DEBUG=true

# 鏁版嵁搴撻厤缃?
DATABASE_URL=sqlite:///./dev_app.db

# API Keys锛堝紑鍙戠幆澧冿級
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
GOOGLE_API_KEY=your_google_key_here
QWEN_API_KEY=your_qwen_key_here
DEEPSEEK_API_KEY=your_deepseek_key_here

# Redis閰嶇疆锛堝鏋滀娇鐢ㄦ湰鍦癛edis锛?
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=

# CORS閰嶇疆
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:3001","http://127.0.0.1:3000"]
EOF
```

#### 1.2 鍚姩鍚庣鏈嶅姟
```bash
# 纭繚鍦╞ackend鐩綍骞舵縺娲籧onda鐜
cd backend
conda activate simsynai

# 鍚姩寮€鍙戞湇鍔″櫒
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 1.3 鏁版嵁搴撳垵濮嬪寲
```bash
# 棣栨杩愯闇€瑕佸垵濮嬪寲鏁版嵁搴?
python -c "
from app.db.session import engine, create_db_and_tables
from app.db.init_db import init_db
from app.db.session import SessionLocal

# 鍒涘缓琛?
create_db_and_tables()

# 鍒濆鍖栭粯璁ょ敤鎴?
db = SessionLocal()
try:
    init_db(db)
    print('鏁版嵁搴撳垵濮嬪寲瀹屾垚!')
finally:
    db.close()
"
```

### 2. 鍓嶇寮€鍙?

#### 2.1 瀹夎Node.js鍜宲npm
```bash
# 瀹夎Node.js锛堟帹鑽愪娇鐢↙TS鐗堟湰锛?
# Windows: 浠庡畼缃戜笅杞藉畨瑁?
# macOS: brew install node
# Linux: 浣跨敤鍖呯鐞嗗櫒鎴栧畼缃戜笅杞?

# 瀹夎pnpm
npm install -g pnpm
```

#### 2.2 瀹夎鍓嶇渚濊禆骞跺惎鍔?
```bash
cd frontend

# 瀹夎渚濊禆
pnpm install

# 鍚姩寮€鍙戞湇鍔″櫒
pnpm start
```

### 3. Redis鏈嶅姟锛堝彲閫夛級

#### 鏈湴瀹夎Redis
**Windows:**
```bash
# 浣跨敤Chocolatey
choco install redis-64

# 鎴栦娇鐢╓SL瀹夎Linux鐗堟湰
```

**macOS:**
```bash
# 浣跨敤Homebrew
brew install redis
brew services start redis
```

**Linux:**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install redis-server
sudo systemctl start redis-server

# CentOS/RHEL
sudo yum install redis
sudo systemctl start redis
```

#### 浣跨敤Docker杩愯Redis
```bash
# 濡傛灉涓嶆兂鍦ㄥ涓绘満瀹夎Redis锛屽彲浠ュ彧杩愯Redis瀹瑰櫒
docker run -d --name redis -p 6379:6379 redis:7.0-alpine
```

## 寮€鍙戝伐鍏烽厤缃?

### 1. VS Code閰嶇疆

鍒涘缓`.vscode/settings.json`锛?
```json
{
    "python.defaultInterpreterPath": "~/anaconda3/envs/simsynai/bin/python",
    "python.terminal.activateEnvironment": true,
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "python.sortImports.args": ["--profile", "black"],
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    }
}
```

### 2. Git Pre-commit閽╁瓙
```bash
# 瀹夎pre-commit
conda activate simsynai
pip install pre-commit

# 鍒涘缓.pre-commit-config.yaml锛堝鏋滄病鏈夌殑璇濓級
cat > .pre-commit-config.yaml << EOF
repos:
  - repo: https://github.com/psf/black
    rev: 23.1.0
    hooks:
      - id: black

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
        args: ["--profile", "black"]

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8

  - repo: https://github.com/pre-commit/mirrors-prettier
    rev: v3.0.0-alpha.4
    hooks:
      - id: prettier
        files: \.(js|ts|jsx|tsx|json|css|md)$
EOF

# 瀹夎pre-commit閽╁瓙
pre-commit install
```

## 寮€鍙戝伐浣滄祦

### 1. 鏃ュ父寮€鍙?
```bash
# 1. 婵€娲籧onda鐜
conda activate simsynai

# 2. 鍚姩鍚庣锛堢粓绔?锛?
cd backend
uvicorn app.main:app --reload

# 3. 鍚姩鍓嶇锛堢粓绔?锛?
cd frontend
pnpm start

# 4. 璁块棶搴旂敤
# 鍓嶇: http://localhost:3000
# 鍚庣API: http://localhost:8000
# API鏂囨。: http://localhost:8000/docs
```

### 2. 杩愯娴嬭瘯
```bash
# 鍚庣娴嬭瘯
cd backend
conda activate simsynai
pytest

# 鍓嶇娴嬭瘯
cd frontend
pnpm test
```

### 3. 浠ｇ爜鏍煎紡鍖?
```bash
# Python浠ｇ爜鏍煎紡鍖?
cd backend
black app/
isort app/

# 鍓嶇浠ｇ爜鏍煎紡鍖?
cd frontend
pnpm run lint --fix
```

## 閮ㄧ讲妯″紡瀵规瘮

| 鐗规€?| 鏈湴寮€鍙戠幆澧?| Docker瀹瑰櫒 | 娣峰悎妯″紡 |
|------|------------|-----------|---------|
| 鍚姩閫熷害 | 蹇?| 涓瓑 | 蹇?|
| 璧勬簮鍗犵敤 | 浣?| 楂?| 涓瓑 |
| 闅旂鎬?| 浣?| 楂?| 涓瓑 |
| 璋冭瘯渚垮埄鎬?| 楂?| 涓瓑 | 楂?|
| 閮ㄧ讲涓€鑷存€?| 浣?| 楂?| 涓瓑 |

### 鎺ㄨ崘鐨勬贩鍚堝紑鍙戞ā寮?
```bash
# 1. 鍓嶅悗绔湪鏈湴寮€鍙戠幆澧冭繍琛?
conda activate simsynai
cd backend && uvicorn app.main:app --reload &
cd frontend && pnpm start &

# 2. 鍙敤Docker杩愯渚濊禆鏈嶅姟
docker run -d --name redis -p 6379:6379 redis:7.0-alpine

# 3. 鏈€缁堟祴璇曚娇鐢ㄥ畬鏁碊ocker鐜
docker compose up -d
```

## 鐜绠＄悊鍛戒护

### Conda鐜绠＄悊
```bash
# 鍒楀嚭鎵€鏈夌幆澧?
conda env list

# 瀵煎嚭鐜閰嶇疆
conda env export > environment.yml

# 鏇存柊鐜
conda env update -f environment.yml

# 鍒犻櫎鐜
conda env remove -n simsynai

# 婵€娲?閫€鍑虹幆澧?
conda activate simsynai
conda deactivate
```

### 渚濊禆绠＄悊
```bash
# 娣诲姞鏂扮殑Python鍖?
conda install package_name
# 鎴?
pip install package_name

# 鏇存柊requirements.txt锛堝湪backend鐩綍锛?
pip freeze > requirements.txt

# 鏇存柊environment.yml
conda env export --no-builds > environment.yml
```

## 鏁呴殰鎺掗櫎

### 甯歌闂

**1. conda鍛戒护鎵句笉鍒?*
```bash
# 閲嶆柊鍒濆鍖朿onda
conda init
# 閲嶅惎缁堢
```

**2. 鐜婵€娲诲け璐?*
```bash
# Windows PowerShell鍙兘闇€瑕佹墽琛岀瓥鐣ヨ皟鏁?
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**3. 绔彛鍐茬獊**
```bash
# 妫€鏌ョ鍙ｅ崰鐢?
netstat -ano | findstr :8000  # Windows
lsof -i :8000                 # macOS/Linux

# 鏉€姝诲崰鐢ㄨ繘绋嬫垨鏇存敼绔彛
uvicorn app.main:app --port 8001
```

**4. 鏁版嵁搴撹繛鎺ラ棶棰?*
```bash
# 鍒犻櫎骞堕噸鏂板垱寤烘暟鎹簱
rm backend/dev_app.db
python backend/init_db_script.py
```

鎭枩锛佺幇鍦ㄦ偍宸茬粡鎷ユ湁浜嗕竴涓畬鏁寸殑鏈湴寮€鍙戠幆澧冿紝鍙互鍦ㄥ涓绘満涓婅繘琛岄珮鏁堢殑寮€鍙戝伐浣溿€?
