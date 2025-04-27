from flask import Flask, render_template, request, jsonify
from deal_finder import DealFinder  # Make sure deal_finder.py is in the same directory
import pandas as pd


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/search', methods=['POST'])
def search():
    product_query = request.form.get('product_query')
    max_results = int(request.form.get('max_results', 5))
    save_results = request.form.get('save_results', 'on') == 'on'

    deal_finder = DealFinder(
        product_query=product_query,
        max_results=max_results,
        save_results=save_results
    )
    results_df = deal_finder.search_all_websites()
    results = results_df.to_dict(orient='records')  # Convert DataFrame to list of dictionaries for easy frontend handling
    
    return jsonify(results)  # Return results as JSON

if __name__ == '__main__':
    app.run(debug=True)
