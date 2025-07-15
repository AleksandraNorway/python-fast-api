# FastAPI Items Management API

A simple REST API for managing items with CRUD operations.

## 🚀 Quick Start

### 1. Setup Virtual Environment

> **macOS/Linux**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install --upgrade pip              # optional, to get latest pip
pip install -r requirements.txt
```

### 3. Run the Server

```bash
uvicorn main:app --reload
```

✅ **Your API is now running at:** http://127.0.0.1:8000  
📚 **Interactive docs:** http://127.0.0.1:8000/docs

## Test the API

### Create an item:

```bash
curl -X POST http://127.0.0.1:8000/items/ \
     -H "Content-Type: application/json" \
     -d '{"name": "apple", "price": 1.50, "description": "Fresh red apple"}'
```

### Get all items:

```bash
curl http://127.0.0.1:8000/items/
```

### Get item by ID:

```bash
curl http://127.0.0.1:8000/items/1
```

## API Endpoints

- `GET /` - Welcome message
- `GET /items/` - Get all items
- `POST /items/` - Create new item
- `GET /items/{id}` - Get item by ID

## Troubleshooting

**Port already in use?**

```bash
lsof -i :8000          # Find what's using port 8000
kill <PID>             # Kill the process
```

**Or run on different port:**

```bash
uvicorn main:app --reload --port 8001
```

## 📝 Extras (optional)

**Add a .gitignore:**

```gitignore
venv/
__pycache__/
*.pyc
.vscode/
```

**Keep your dependencies in sync:**

```bash
pip freeze > requirements.txt
```
