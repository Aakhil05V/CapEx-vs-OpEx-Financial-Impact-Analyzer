from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json

app = Flask(__name__)

@app.route('/')
def index():
    """Render the main application page"""
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    """Calculate CapEx vs OpEx financial analysis"""
    try:
        data = request.get_json()
        
        capex = float(data.get('capex', 0))
        opex_monthly = float(data.get('opex_monthly', 0))
        years = int(data.get('years', 5))
        
        # Validate inputs
        if capex < 0 or opex_monthly < 0 or years <= 0:
            return jsonify({'error': 'Invalid input values'}), 400
        
        # Calculate yearly costs
        years_list = list(range(1, years + 1))
        capex_values = [capex] * len(years_list)  # Constant CapEx
        opex_cumulative = [opex_monthly * 12 * year for year in years_list]  # Cumulative OpEx
        
        # Find break-even point
        break_even_year = None
        for i, opex_val in enumerate(opex_cumulative):
            if opex_val >= capex:
                break_even_year = years_list[i]
                break
        
        # Calculate totals
        total_capex = capex
        total_opex = opex_cumulative[-1] if opex_cumulative else 0
        difference = total_opex - total_capex
        
        return jsonify({
            'years': years_list,
            'capex_values': capex_values,
            'opex_values': opex_cumulative,
            'break_even_year': break_even_year,
            'total_capex': total_capex,
            'total_opex': total_opex,
            'difference': difference
        })
    
    except (ValueError, TypeError) as e:
        return jsonify({'error': 'Invalid input format'}), 400
    except Exception as e:
        return jsonify({'error': 'Server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
