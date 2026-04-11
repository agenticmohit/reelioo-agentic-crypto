import requests


def get_crypto_price(symbol: str):
    """Get current price and 24h stats for a coin from Binance.
    Symbol examples: BTC, ETH, SOL — just the coin name, no USDT needed"""
    symbol = symbol.upper().strip()
    if not symbol.endswith("USDT"):
        symbol = symbol + "USDT"

    response = requests.get(
        f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}",
        timeout=10
    )
    data = response.json()

    return {
        "symbol": symbol,
        "price": float(data["lastPrice"]),
        "change_24h": float(data["priceChangePercent"]),
        "high_24h": float(data["highPrice"]),
        "low_24h": float(data["lowPrice"]),
        "volume_24h": float(data["volume"]),
    }


def get_market_momentum(symbol: str):
    """Calculate Velocity score 0-100 for a coin.
    High Velocity = aggressive momentum. Low = passive, weak market"""
    symbol = symbol.upper().strip()
    if not symbol.endswith("USDT"):
        symbol = symbol + "USDT"

    response = requests.get(
        "https://api.binance.com/api/v3/klines",
        params={"symbol": symbol, "interval": "1h", "limit": 20},
        timeout=10
    )
    klines = response.json()

    closes  = [float(k[4]) for k in klines]
    volumes = [float(k[5]) for k in klines]

    recent_move = sum(abs(closes[i] - closes[i-1]) for i in range(-5, 0)) / 5
    avg_move    = sum(abs(closes[i] - closes[i-1]) for i in range(1, 15)) / 14

    velocity_ratio = recent_move / avg_move if avg_move > 0 else 1
    vol_ratio      = (sum(volumes[-5:]) / 5) / (sum(volumes) / len(volumes))

    score     = min(100, int((velocity_ratio * 0.6 + vol_ratio * 0.4) * 50))
    direction = "UPWARD" if closes[-1] > closes[-5] else "DOWNWARD"

    return {
        "velocity_score": score,
        "direction": direction,
        "label": (
            "HIGH — Strong momentum"     if score >= 75 else
            "MODERATE — Steady movement" if score >= 50 else
            "LOW — Weak momentum"
        )
    }


def get_volume_analysis(symbol: str):
    """Calculate Mass score 0-100.
    Low Mass on a big price move = Vacuum Trap (likely reversal)"""
    symbol = symbol.upper().strip()
    if not symbol.endswith("USDT"):
        symbol = symbol + "USDT"

    response = requests.get(
        "https://api.binance.com/api/v3/klines",
        params={"symbol": symbol, "interval": "1h", "limit": 48},
        timeout=10
    )
    klines = response.json()

    volumes    = [float(k[5]) for k in klines]
    closes     = [float(k[4]) for k in klines]
    recent_vol = sum(volumes[-6:]) / 6
    avg_vol    = sum(volumes) / len(volumes)
    mass_ratio = recent_vol / avg_vol if avg_vol > 0 else 1
    score      = min(100, int(mass_ratio * 50))
    price_move = abs(closes[-1] - closes[-6]) / closes[-6] * 100

    result = {
        "mass_score":   score,
        "volume_ratio": round(mass_ratio, 2),
        "label": (
            "HIGH — Heavy volume"  if score >= 75 else
            "MODERATE — OK volume" if score >= 50 else
            "LOW — Light volume"
        )
    }

    if price_move > 2.0 and mass_ratio < 0.7:
        result["warning"] = "VACUUM TRAP — Price moved without volume. Likely reversal."
    elif price_move < 0.5 and mass_ratio > 1.8:
        result["warning"] = "LOADING — Volume building with flat price. Breakout coming."

    return result
