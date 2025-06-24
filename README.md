# SimSynAI - 鍩轰簬澶ц瑷€妯″瀷鐨勬櫤鑳藉寲浠跨湡骞冲彴

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI/CD](https://github.com/Hanna-Qu/SimSynAI/workflows/CI/CD%20Pipeline/badge.svg)](https://github.com/Hanna-Qu/SimSynAI/actions)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://docker.com)
[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)](https://github.com/Hanna-Qu/SimSynAI/releases)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

SimSynAI 鏄竴涓泦鎴愪簡澶氱澶ц瑷€妯″瀷鐨勬櫤鑳藉寲浠跨湡骞冲彴锛屾敮鎸佹櫤鑳藉璇濄€佷豢鐪熷缓妯°€佹暟鎹彲瑙嗗寲绛夊姛鑳姐€?

## 鉁?涓昏鐗规€?

- 馃 **澶歀LM妯″瀷闆嗘垚** - 鏀寔OpenAI銆丆laude銆丟emini銆佸崈闂€丏eepSeek绛?
- 馃攼 **瀹夊叏鐨勭敤鎴风郴缁?* - JWT璁よ瘉銆丄PI瀵嗛挜鍔犲瘑瀛樺偍
- 馃挰 **鏅鸿兘瀵硅瘽** - 瀹炴椂AI瀵硅瘽銆佸巻鍙茶褰曠鐞?
- 馃敩 **浠跨湡瀹為獙** - 鍙鍖栧缓妯°€佸弬鏁伴厤缃€佺粨鏋滃垎鏋?
- 馃搳 **鏁版嵁鍙鍖?* - 澶氱鍥捐〃绫诲瀷銆佷氦浜掑紡灞曠ず
- 馃寪 **鍥介檯鍖栨敮鎸?* - 涓嫳鏂囧弻璇晫闈?
- 馃摫 **鍝嶅簲寮忚璁?* - 瀹岀編閫傞厤妗岄潰鍜岀Щ鍔ㄨ澶?
- 馃惓 **瀹瑰櫒鍖栭儴缃?* - 寮€绠卞嵆鐢ㄧ殑Docker瑙ｅ喅鏂规

## 馃殌 蹇€熷紑濮?

### 鐜瑕佹眰
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (鐢熶骇閮ㄧ讲)
- Git

### 鏂瑰紡1锛欴ocker瀹瑰櫒鍖栬繍琛岋紙鎺ㄨ崘鐢ㄤ簬鐢熶骇锛?

```bash
# 1. 鍏嬮殕椤圭洰
git clone https://github.com/Hanna-Qu/SimSynAI.git
cd SimSynAI

# 2. 鍚姩鎵€鏈夋湇鍔?
docker compose up -d

# 3. 绛夊緟鏈嶅姟鍚姩瀹屾垚 (绾?-2鍒嗛挓)
docker compose ps

# 4. 璁块棶搴旂敤
# 鍓嶇: http://localhost:3000
# 鍚庣API: http://localhost:8000
# API鏂囨。: http://localhost:8000/api/v1/docs
```

### 鏂瑰紡2锛氭湰鍦板紑鍙戠幆澧冿紙鎺ㄨ崘鐢ㄤ簬寮€鍙戯級

浣跨敤conda铏氭嫙鐜杩涜鏈湴寮€鍙戯紝鑾峰緱鏇村ソ鐨勫紑鍙戜綋楠岋細

#### 蹇€熷惎鍔?
```bash
# 1. 鍏嬮殕椤圭洰
git clone https://github.com/Hanna-Qu/SimSynAI.git
cd SimSynAI

# 2. 鍒濆鍖栧紑鍙戠幆澧冿紙棣栨杩愯锛?
# Windows
.\scripts\dev-start.ps1 init

# Linux/macOS
chmod +x scripts/dev-start.sh
./scripts/dev-start.sh init

# 3. 鍚姩寮€鍙戞湇鍔?
# Windows
.\scripts\dev-start.ps1 full

# Linux/macOS  
./scripts/dev-start.sh full
```

#### 鍒嗗埆鍚姩鏈嶅姟
```bash
# 鍚姩鍚庣鏈嶅姟
./scripts/dev-start.sh backend   # 鎴?.\scripts\dev-start.ps1 backend

# 鍚姩鍓嶇鏈嶅姟锛堟柊缁堢锛?
./scripts/dev-start.sh frontend  # 鎴?.\scripts\dev-start.ps1 frontend
```

#### 鎵嬪姩鐜閰嶇疆
濡傛灉鎮ㄥ枩娆㈡墜鍔ㄦ帶鍒讹紝璇峰弬鑰?[鏈湴寮€鍙戠幆澧冭缃寚鍗梋(docs/development-setup.md)

### 榛樿璐︽埛
- **绠＄悊鍛?*: `admin` / `admin123`
- **娴嬭瘯鐢ㄦ埛**: `demo` / `demo123`

### 璁块棶鍦板潃
- 鍓嶇搴旂敤: http://localhost:3000
- 鍚庣API: http://localhost:8000
- API鏂囨。: http://localhost:8000/api/v1/docs
- Redis: localhost:6379 (浠匘ocker鏂瑰紡)

## 鎶€鏈爤

### 鍓嶇
- React 18 + TypeScript
- Ant Design UI缁勪欢搴?
- React Router v6 璺敱绠＄悊
- Axios HTTP瀹㈡埛绔?
- ECharts 鏁版嵁鍙鍖?
- i18next 鍥介檯鍖?

### 鍚庣
- Python 3.11 + FastAPI
- SQLAlchemy ORM
- SQLite 鏁版嵁搴?
- 澶歀LM闆嗘垚 (OpenAI, Claude, Gemini, Qwen, DeepSeek)
- Redis 缂撳瓨

### 閮ㄧ讲
- Docker + Docker Compose
- Nginx 鍙嶅悜浠ｇ悊

## 椤圭洰缁撴瀯

```
SimSynAI/
鈹溾攢鈹€ frontend/          # React鍓嶇搴旂敤
鈹?  鈹溾攢鈹€ src/
鈹?  鈹?  鈹溾攢鈹€ components/    # React缁勪欢
鈹?  鈹?  鈹溾攢鈹€ locales/       # 鍥介檯鍖栨枃浠?
鈹?  鈹?  鈹斺攢鈹€ styles/        # 鏍峰紡鏂囦欢
鈹?  鈹斺攢鈹€ public/            # 闈欐€佽祫婧?
鈹溾攢鈹€ backend/           # FastAPI鍚庣
鈹?  鈹溾攢鈹€ app/
鈹?  鈹?  鈹溾攢鈹€ api/           # API璺敱
鈹?  鈹?  鈹溾攢鈹€ core/          # 鏍稿績閰嶇疆
鈹?  鈹?  鈹溾攢鈹€ db/            # 鏁版嵁搴撴ā鍨?
鈹?  鈹?  鈹溾攢鈹€ llm/           # LLM闆嗘垚
鈹?  鈹?  鈹溾攢鈹€ services/      # 涓氬姟閫昏緫
鈹?  鈹?  鈹斺攢鈹€ simulation/    # 浠跨湡寮曟搸
鈹?  鈹斺攢鈹€ tests/             # 娴嬭瘯鏂囦欢
鈹溾攢鈹€ data/              # 鏁版嵁瀛樺偍
鈹斺攢鈹€ docker-compose.yml # Docker閰嶇疆
```

## 涓昏鍔熻兘

### 1. 鐢ㄦ埛璁よ瘉
- 鐢ㄦ埛娉ㄥ唽/鐧诲綍
- JWT浠ょ墝璁よ瘉
- 鐢ㄦ埛璧勬枡绠＄悊

### 2. 鏅鸿兘瀵硅瘽
- 澶歀LM妯″瀷鏀寔
- 瀹炴椂娑堟伅閫氫俊
- 瀵硅瘽鍘嗗彶绠＄悊

### 3. 浠跨湡寤烘ā
- 鍙鍖栧缓妯＄晫闈?
- 鍙傛暟閰嶇疆绠＄悊
- 浠跨湡缁撴灉鍒嗘瀽

### 4. 鏁版嵁鍙鍖?
- 澶氱鍥捐〃绫诲瀷
- 瀹炴椂鏁版嵁鏇存柊
- 浜や簰寮忓浘琛?

### 5. 鍥介檯鍖?
- 涓嫳鏂囧垏鎹?
- 鏈湴鍖栭厤缃?

## 寮€鍙戣鏄?

### 鐜鍙橀噺閰嶇疆

鍦?`docker-compose.yml` 涓厤缃互涓嬬幆澧冨彉閲忥細

```yaml
# LLM API Keys
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
GOOGLE_API_KEY=your_google_key
QWEN_API_KEY=your_qwen_key
DEEPSEEK_API_KEY=your_deepseek_key

# 鏁版嵁搴?
DATABASE_URL=sqlite:///./app.db

# Redis
REDIS_PASSWORD=simsynai

# 瀹夊叏
SECRET_KEY=your_secret_key
```

### 鏃ュ織鍜屾暟鎹?

椤圭洰鏁版嵁瀛樺偍鍦ㄤ互涓嬬洰褰曪細
- `./data/logs/` - 搴旂敤鏃ュ織
- `./data/simulation_results/` - 浠跨湡缁撴灉

### 鍋滄鏈嶅姟

```bash
docker compose down
```

### 閲嶅缓鏈嶅姟

```bash
docker compose down
docker compose build --no-cache
docker compose up -d
```

## 璐＄尞鎸囧崡

1. Fork 椤圭洰
2. 鍒涘缓鐗规€у垎鏀?(`git checkout -b feature/AmazingFeature`)
3. 鎻愪氦鏇存敼 (`git commit -m 'Add some AmazingFeature'`)
4. 鎺ㄩ€佸埌鍒嗘敮 (`git push origin feature/AmazingFeature`)
5. 鎵撳紑 Pull Request

## 璁稿彲璇?

鏈」鐩噰鐢?MIT 璁稿彲璇併€傝缁嗕俊鎭鍙傞槄 LICENSE 鏂囦欢銆?
