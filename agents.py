import os
from google import genai
import tools

client = genai.Client(api_key='AQ.Ab8RN6Luj8LjnNs7Z8Vuv-JV4WURv6gPv9Z_PX4se1yFA3HQhA')
MODEL_ID = 'gemini-3.5-flash-lite'

def quant_agent(symbol: str) -> str:
    market_data = tools.get_stock_data(symbol)
    price = market_data.get("current_price", 0.0)
    prev = market_data.get("previous_close", 0.0)
    delta = round(price - prev, 2)
    pct = round((delta / prev) * 100, 2) if prev > 0 else 0.0
    
    prompt = f"""You are a Quantitative Technical Analyst. 
    Asset: {symbol}
    Current Price: {price}
    Previous Close: {prev}
    Net Change: {delta} ({pct}%)
    
    Provide a concise 2-sentence technical evaluation of this price movement."""
    
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=prompt
    )
    return response.text

def research_agent(symbol: str) -> str:
    doc_data = tools.search_filings(symbol)
    prompt = f"""You are a Fundamental and Compliance Researcher. Read this corporate filing excerpt: '{doc_data['excerpt']}'. 
    Summarize the key risks or positives in 2 sentences. You MUST cite this exact source at the end: [{doc_data['source']}]."""
    
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=prompt
    )
    return response.text

def manager_agent(symbol: str, profile: str, quant_res: str, research_res: str) -> str:
    prompt = f"""You are an Expert Portfolio Manager. 
    Target Asset: {symbol}
    Investor Profile: {profile}
    Quantitative Analysis: {quant_res}
    Research/Compliance Analysis: {research_res}
    
    Provide a definitive Buy/Hold/Sell recommendation tailored to the investor profile in 3-4 sentences."""
    
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=prompt
    )
    return response.text