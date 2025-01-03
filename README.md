# Cashflow Forecast

A machine learning-powered cashflow forecasting tool for credit evaluation and lending decisions. This project combines advanced time series analysis with risk metrics to provide accurate 12-month cashflow predictions.

## Features

### Forecasting Capabilities
- Bank statement analysis and preprocessing
- 12-month cashflow predictions using machine learning
- Seasonal pattern detection and adjustment
- Multiple forecasting scenarios (Baseline, Optimistic, Pessimistic)

### Risk Analysis
- Operating Cash Flow Ratio
- Cash Flow Volatility
- Coverage Ratio Analysis
- Trend Strength Detection
- Negative Cashflow Period Analysis

### Interactive Dashboard
- Real-time data visualization
- Historical cashflow analysis
- Stress testing scenarios
- Key risk metrics display

## Tech Stack

### Backend
- Python 3.9+
- FastAPI
- scikit-learn
- pandas
- numpy
- statsmodels

### Frontend
- React
- Recharts for visualization
- Tailwind CSS
- shadcn/ui components

## Installation

### Prerequisites
- Python 3.9 or higher
- Node.js 16 or higher
- uv package installer

### Backend Setup

1. Clone the repository:
```bash
git clone https://github.com/joshmo01/Cashflow_forecast.git
cd Cashflow_forecast
```

2. Create and activate virtual environment using uv:
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
uv pip install -r requirements.txt
```

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

## Usage

1. Start the backend server:
```bash
uvicorn cashflow_forecast.api.main:app --reload
```

2. Start the frontend development server:
```bash
cd frontend
npm run dev
```

3. Access the application at http://localhost:3000

### Input Data Format
The application expects bank statement data in CSV format with the following columns:
- date: Transaction date (YYYY-MM-DD)
- inflow: Money received
- outflow: Money spent
- category (optional): Transaction category

## Project Structure

```
├── cashflow_forecast/          # Main package directory
│   ├── api/                    # FastAPI backend
│   ├── models/                 # ML models
│   └── utils/                  # Utility functions
├── frontend/                   # React frontend
│   ├── src/
│   ├── package.json
│   └── vite.config.js
├── tests/                      # Test directory
├── pyproject.toml             # Project metadata
└── requirements.txt           # Dependencies
```

## Development

### Running Tests
```bash
pytest tests/
```

### Code Formatting
```bash
black cashflow_forecast
isort cashflow_forecast
```

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
Distributed under the MIT License. See `LICENSE` for more information.

## Acknowledgments
- scikit-learn for machine learning capabilities
- FastAPI for the efficient backend
- React and Recharts for the interactive frontend
- shadcn/ui for beautiful UI components