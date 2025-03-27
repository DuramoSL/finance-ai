import gradio as gr
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from transformers import pipeline
from datetime import datetime
import numpy as np
import os
from PIL import Image, ImageDraw, ImageFont
import io
import base64

# Create logos directory if it doesn't exist
os.makedirs("logos", exist_ok=True)

# Company data - using local logos
COMPANIES = {
    "TCS": {"ticker": "TCS.NS", "logo": "tcs.png"},
    "HDFC Bank": {"ticker": "HDFCBANK.NS", "logo": "hdfc.png"},
    "Reliance": {"ticker": "RELIANCE.NS", "logo": "relience.png"}
}

# Create default logo with better styling
# def create_default_logo(company):
#     img = Image.new('RGB', (200, 100), color=(240, 240, 240))
#     try:
#         d = ImageDraw.Draw(img)
#         font = ImageFont.load_default()
#         d.text((10, 40), company, fill='navy', font=font)
#     except:
#         pass
#     buffered = io.BytesIO()
#     img.save(buffered, format="PNG")
#     return f"data:image/png;base64,{base64.b64encode(buffered.getvalue()).decode()}"

# Initialize LLM
financial_analyst = pipeline(
    "text-generation",
    model="gpt2",
    device="cpu",
    truncation=True
)

def analyze_company(company):
    """Simplified analysis function matching your UI"""
    try:
        # Get stock data
        ticker = COMPANIES[company]["ticker"]
        data = yf.download(ticker, period="1y")
        
        # Generate analysis
        prompt = f"Analyze {company}'s FY24 financial performance in 3 bullet points:"
        analysis = financial_analyst(prompt, max_length=200)[0]['generated_text']
        
        # Create plot
        plt.figure(figsize=(8, 3))
        plt.plot(data['Close'], color='royalblue')
        plt.title(f"{company} Stock Price (1 Year)")
        plt.grid(True, alpha=0.3)
        plot = plt.gcf()
        
        return analysis, plot
    
    except Exception as e:
        return f"Analysis failed: {str(e)}", None

# Create the clean interface shown in your screenshot
with gr.Blocks(title="Indian Stock Analysis", theme=gr.themes.Soft()) as app:
    gr.Markdown("## Indian Stock Analysis Dashboard")
    gr.Markdown("Analyze FY24 financial performance of top Indian companies")
    
    with gr.Row():
        with gr.Column():
            company = gr.Dropdown(
                list(COMPANIES.keys()),
                label="Select Company",
                value="TCS"
            )
            analyze_btn = gr.Button("Analyze", variant="primary")

    
    with gr.Row():
        analysis_output = gr.Textbox(
            label="Analysis Report",
            interactive=False,
            placeholder="Analysis will appear here..."
        )
    
    plot_output = gr.Plot(
        label="Price Trend",
        show_label=False
    )
    
    # Connect components
    analyze_btn.click(
        analyze_company,
        inputs=company,
        outputs=[analysis_output, plot_output]
    )


if __name__ == "__main__":
    app.launch(server_port=7860)