# Tech Deal Finder

A web scraper that finds the best deals on technology products across multiple e-commerce websites.

![Tech Deal Finder](https://via.placeholder.com/800x400?text=Tech+Deal+Finder)

## Description

Tech Deal Finder is a command-line tool that helps you find the best deals on technology products. It searches multiple e-commerce websites (Amazon, Best Buy, Walmart, and Newegg) for the product you're looking for, compares prices, and recommends the best deal.

## Features

- Search for technology products across multiple websites
- Compare prices and find the best deal
- Save search results to a JSON file
- Concurrent searching for faster results
- User-friendly command-line interface

## Installation

1. Clone this repository or download the files
2. Make sure you have Python 3.6+ installed
3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

4. Run the test script to verify your installation:

```bash
python test_scraper.py
```

Or use the provided batch file (Windows):

```
run_tests.bat
```

The test script checks:
- That all required dependencies are installed
- That the scraper can connect to the e-commerce websites
- That the scraper can parse HTML from the websites
- That the DealFinder class can be imported correctly

## Usage

Tech Deal Finder offers both a command-line interface and a graphical user interface.

### Command-Line Interface

#### Basic Usage

Run the script and enter the product you're looking for when prompted:

```bash
python deal_finder.py
```

Or use the provided batch file (Windows):

```
run_deal_finder.bat
```

#### Command-line Arguments

You can also provide the product as a command-line argument:

```bash
python deal_finder.py "macbook pro"
```

#### Additional Options

- `--max-results`: Maximum number of results to return per website (default: 5)
- `--no-save`: Do not save results to a file

Example:

```bash
python deal_finder.py "ipad pro" --max-results 10 --no-save
```

### Graphical User Interface

For a more user-friendly experience, you can use the GUI version:

```bash
python deal_finder_gui.py
```

Or use the provided batch file (Windows):

```
run_gui.bat
```

The GUI provides the same functionality as the command-line interface but with a more intuitive interface:

- Enter your search query in the text field
- Adjust the maximum number of results per website
- Choose whether to save results to a file
- View the search progress and results in a tabbed interface
- Double-click on a result to open its URL in your default web browser

## Example Output

```
Searching for 'macbook pro' across multiple websites...

Searching Amazon...
Searching Best Buy...
Searching Walmart...
Searching Newegg...

Results saved to results_20250413_152500.json

================================================================================
BEST DEALS FOR: macbook pro
================================================================================

BEST DEAL: Apple MacBook Pro 13.3" with Retina Display, M1 Chip, 8GB Memory, 256GB SSD
Price: $1199.99
Website: Best Buy
URL: https://www.bestbuy.com/site/apple-macbook-pro-13-3-with-retina-display-m1-chip-8gb-memory-256gb-ssd-space-gray/6418601.p

ALL RESULTS:
--------------------------------------------------------------------------------
1. Apple MacBook Pro 13.3" with Retina Display, M1 Chip, 8GB Memory, 256GB SSD
   Price: $1199.99
   Website: Best Buy
   URL: https://www.bestbuy.com/site/apple-macbook-pro-13-3-with-retina-display-m1-chip-8gb-memory-256gb-ssd-space-gray/6418601.p
--------------------------------------------------------------------------------
2. Apple MacBook Pro (13-inch, M1, 2020) 8GB RAM, 256GB SSD - Space Gray
   Price: $1249.00
   Website: Amazon
   URL: https://www.amazon.com/Apple-MacBook-13-inch-256GB-Storage/dp/B08N5KWB9H
--------------------------------------------------------------------------------
...
```

## Limitations and Considerations

- **Website Structure Changes**: E-commerce websites frequently update their HTML structure, which may break the scraping functionality. If you encounter issues, the parsers may need to be updated.
- **Rate Limiting**: Excessive requests to these websites may result in your IP being temporarily blocked. The script includes random delays between requests to mitigate this.
- **Legal Considerations**: Always check the terms of service of websites before scraping them. Some websites prohibit scraping.
- **Accuracy**: The script attempts to find the best matches for your query, but may not always return the exact product you're looking for.

## Future Improvements

- Add more e-commerce websites
- Implement product filtering (by brand, price range, etc.)
- Create a web interface
- Add product reviews and ratings
- Implement price history tracking

## License

This project is licensed under the MIT License - see the LICENSE file for details.
