from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="Calculator API")

class CalcRequest(BaseModel):
    expression: str

class CalcResponse(BaseModel):
    result: float | str
    error: str | None = None

def safe_eval(expr: str) -> float | str:
    """Safely evaluate a math expression."""
    allowed = set("0123456789+-*/().% ")
    if not all(c in allowed for c in expr):
        raise ValueError("Invalid characters")
    try:
        return eval(expr, {"__builtins__": {}}, {})
    except ZeroDivisionError:
        raise ValueError("Division by zero")
    except Exception:
        raise ValueError("Invalid expression")

@app.post("/api/calculate", response_model=CalcResponse)
async def calculate(req: CalcRequest):
    try:
        result = safe_eval(req.expression)
        return CalcResponse(result=result)
    except ValueError as e:
        return CalcResponse(result=0, error=str(e))

@app.get("/", response_class=HTMLResponse)
async def index():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Calculator</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: system-ui, sans-serif; min-height: 100vh; display: flex; align-items: center; justify-content: center; background: #f5f5f5; }
        .calc { background: white; border-radius: 16px; box-shadow: 0 4px 24px rgba(0,0,0,0.1); padding: 24px; width: 100%; max-width: 360px; }
        .display { background: #1e1e1e; color: #fff; font-size: 2.5rem; text-align: right; padding: 16px; border-radius: 8px; margin-bottom: 16px; overflow: hidden; text-overflow: ellipsis; min-height: 64px; font-family: monospace; }
        .error { color: #ff6b6b; font-size: 0.875rem; min-height: 20px; margin-bottom: 12px; text-align: right; }
        .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }
        button { padding: 20px; font-size: 1.25rem; border: none; border-radius: 8px; cursor: pointer; transition: all 0.1s; font-weight: 500; }
        button:hover { transform: translateY(-1px); box-shadow: 0 2px 8px rgba(0,0,0,0.15); }
        button:active { transform: translateY(0); }
        .num { background: #fff; color: #1e1e1e; border: 1px solid #e0e0e0; }
        .num:hover { background: #fafafa; }
        .op { background: #0066cc; color: white; }
        .op:hover { background: #0052a3; }
        .func { background: #f0f0f0; color: #333; }
        .func:hover { background: #e0e0e0; }
        .eq { background: #28a745; color: white; grid-column: span 2; }
        .eq:hover { background: #218838; }
        .wide { grid-column: span 2; }
    </style>
</head>
<body>
    <div class="calc">
        <div class="display" id="display">0</div>
        <div class="error" id="error"></div>
        <div class="grid">
            <button class="func wide" data-action="clear">C</button>
            <button class="func" data-action="backspace">⌫</button>
            <button class="func" data-action="percent">%</button>
            <button class="op" data-value="/">÷</button>
            <button class="num" data-value="7">7</button>
            <button class="num" data-value="8">8</button>
            <button class="num" data-value="9">9</button>
            <button class="op" data-value="*">×</button>
            <button class="num" data-value="4">4</button>
            <button class="num" data-value="5">5</button>
            <button class="num" data-value="6">6</button>
            <button class="op" data-value="-">−</button>
            <button class="num" data-value="1">1</button>
            <button class="num" data-value="2">2</button>
            <button class="num" data-value="3">3</button>
            <button class="op" data-value="+">+</button>
            <button class="num wide" data-value="0">0</button>
            <button class="num" data-value=".">.</button>
            <button class="eq" data-action="equals">=</button>
        </div>
    </div>
    <script>
        const display = document.getElementById('display');
        const errorEl = document.getElementById('error');
        let expr = '';

        function updateDisplay() {
            display.textContent = expr || '0';
        }

        function showError(msg) {
            errorEl.textContent = msg;
            setTimeout(() => errorEl.textContent = '', 3000);
        }

        async function calculate() {
            if (!expr) return;
            try {
                const res = await fetch('/api/calculate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ expression: expr })
                });
                const data = await res.json();
                if (data.error) {
                    showError(data.error);
                } else {
                    expr = String(data.result);
                    updateDisplay();
                }
            } catch (e) {
                showError('Connection error');
            }
        }

        document.querySelectorAll('button').forEach(btn => {
            btn.addEventListener('click', () => {
                const val = btn.dataset.value;
                const action = btn.dataset.action;

                if (val !== undefined) {
                    if (val === '.' && expr.slice(expr.lastIndexOf(/[+\-*/]/)+1).includes('.')) return;
                    expr += val;
                    updateDisplay();
                } else if (action) {
                    if (action === 'clear') { expr = ''; updateDisplay(); }
                    else if (action === 'backspace') { expr = expr.slice(0, -1); updateDisplay(); }
                    else if (action === 'percent') { expr += '*0.01'; updateDisplay(); }
                    else if (action === 'equals') { calculate(); }
                }
            });
        });

        document.addEventListener('keydown', e => {
            if (e.key >= '0' && e.key <= '9') { expr += e.key; updateDisplay(); }
            else if ('+-*/.'.includes(e.key)) { expr += e.key; updateDisplay(); }
            else if (e.key === 'Enter' || e.key === '=') { e.preventDefault(); calculate(); }
            else if (e.key === 'Backspace') { expr = expr.slice(0, -1); updateDisplay(); }
            else if (e.key === 'Escape') { expr = ''; updateDisplay(); }
        });
    </script>
</body>
</html>
"""

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)