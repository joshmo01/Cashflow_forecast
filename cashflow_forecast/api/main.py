from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd

from cashflow_forecast.models.forecasting import LendingCashflowModel

app = FastAPI(title="Cashflow Forecast API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ForecastResponse(BaseModel):
    historical_data: list
    forecast_data: list
    risk_metrics: dict

@app.post("/api/forecast", response_model=ForecastResponse)
async def generate_forecast(file: UploadFile = File(...)):
    # Read CSV file
    df = pd.read_csv(file.file)
    
    # Initialize model
    model = LendingCashflowModel()
    
    # Process data
    monthly_data = model.preprocess_transactions(df)
    features = model.extract_features(monthly_data)
    
    # Generate forecast
    model.train_model(monthly_data, features)
    forecast = model.generate_forecast(monthly_data, features)
    scenarios = model.calculate_stress_scenarios(forecast)
    risk_metrics = model.calculate_risk_metrics(monthly_data)
    
    return ForecastResponse(
        historical_data=monthly_data.to_dict('records'),
        forecast_data=[{
            'month': f'2025-{i+1:02d}',
            **{k: v[i] for k, v in scenarios.items()}
        } for i in range(len(forecast))],
        risk_metrics=risk_metrics
    )

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}