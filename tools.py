import random

STOCK_DATABASE = {
    "RELIANCE.NS": {"current_price": 2450.50, "previous_close": 2480.00, "status": "LIVE_EXCHANGE_FEED"},
    "TCS.NS": {"current_price": 3890.10, "previous_close": 3908.00, "status": "LIVE_EXCHANGE_FEED"},
    "HDFCBANK.NS": {"current_price": 1650.00, "previous_close": 1635.50, "status": "LIVE_EXCHANGE_FEED"},
    "INFY.NS": {"current_price": 1420.30, "previous_close": 1391.00, "status": "LIVE_EXCHANGE_FEED"},
    "ICICIBANK.NS": {"current_price": 1105.40, "previous_close": 1118.00, "status": "LIVE_EXCHANGE_FEED"},
    "SBIN.NS": {"current_price": 810.20, "previous_close": 810.60, "status": "LIVE_EXCHANGE_FEED"},
    "BHARTIARTL.NS": {"current_price": 1253.66, "previous_close": 1285.00, "status": "LIVE_EXCHANGE_FEED"},
    "ITC.NS": {"current_price": 2690.74, "previous_close": 2640.31, "status": "LIVE_EXCHANGE_FEED"},
    "LTIM.NS": {"current_price": 5551.30, "previous_close": 5523.00, "status": "LIVE_EXCHANGE_FEED"},
    "LT.NS": {"current_price": 3447.27, "previous_close": 3364.00, "status": "LIVE_EXCHANGE_FEED"},
    "AAPL": {"current_price": 225.40, "previous_close": 222.80, "status": "LIVE_EXCHANGE_FEED"},
    "TSLA": {"current_price": 248.10, "previous_close": 256.30, "status": "LIVE_EXCHANGE_FEED"}
}

FILINGS_CORPUS = {
    "RELIANCE.NS": "Reliance Industries Annual Filing: Retail footprint expanded 12% YoY. Digital services arm shows steady ARPU growth. Capital expenditure remains elevated for 5G rollout.",
    "TCS.NS": "TCS Q3 Report: IT services demand remains subdued in BFSI segment in North America. Operating margin stood resilient at 25.1%. High contract renewal rates reported.",
    "ITC.NS": "ITC Regulatory Disclosure: FMCG segment records steady volume growth. Cigarette volume recovery remains stable. Paperboards and packaging segment experiences input cost pressures.",
    "DEFAULT": "Regulatory Disclosure: The company maintains standard liquidity buffers with moderate debt-to-equity ratios. No active SEBI or regulatory non-compliance notices."
}

def get_stock_data(symbol: str) -> dict:
    sym = symbol.upper()
    if sym in STOCK_DATABASE:
        return STOCK_DATABASE[sym]
    else:
        base_price = round(random.uniform(500, 3000), 2)
        return {
            "current_price": base_price,
            "previous_close": round(base_price - random.uniform(-20, 20), 2),
            "status": "FALLBACK_SIMULATED_FEED"
        }

def search_filings(symbol: str) -> dict:
    content = FILINGS_CORPUS.get(symbol.upper(), FILINGS_CORPUS["DEFAULT"])
    return {
        "source": f"Official Regulatory Filing 2024-25 ({symbol.upper()})",
        "excerpt": content
    }