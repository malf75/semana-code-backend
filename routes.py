import uvicorn
import os
from setup.settings import app
from fastapi.responses import RedirectResponse

@app.get("/")
def redirect_index():
    return RedirectResponse("/docs")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
