import yfinance as yf
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

nas = yf.Ticker('nas.ol')
msft = yf.Ticker('msft')

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def div(symbol: str):
    return yf.Ticker(symbol).dividends


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
