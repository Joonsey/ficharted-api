from logging import Logger
import yfinance as yf
from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import get_tickers as gt
import logging
import test
from enum import Enum, auto

app = FastAPI()
tickers = gt.get_tickers()
logger = logging.getLogger(__name__)

origins = [
    "*"
]

class Exchange(Enum):
    OSLO = "OSLO"

stock_infos = []

async def update_stock_info():
    global stock_infos
    stock_infos = await test.main(stock_infos)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/run-update/')
async def run_update(backgroundtask: BackgroundTasks):
    backgroundtask.add_task(update_stock_info)
    return 'started update'

@app.get('/stocks-meta/')
async def stocks_meta(exchange: Exchange):
    if exchange == Exchange.OSLO:
        return stock_infos

    raise HTTPException(400, "no data for this exchange")

@app.get('/dividends/')
async def div(symbol: str):
    return yf.Ticker(symbol).dividends

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
