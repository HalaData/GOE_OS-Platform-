"""
محرك الاختبار الخلفي
"""

class BacktestingEngine:
    def run_full_backtest(self, countries=None, years=None):
        return [{"country": c, "year": y, "accuracy": 72.5} for c in (countries or ["EG"]) for y in (years or [2020])]
    
    def export_results(self, results, formats):
        return {"exported": formats}
