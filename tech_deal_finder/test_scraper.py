#!/usr/bin/env python3
"""
Test script for the Tech Deal Finder.
This script tests the basic functionality of the web scraper.
"""

import sys
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

def test_dependencies():
    """Test that all required dependencies are installed."""
    print("Testing dependencies...")
    
    try:
        import requests
        print("✓ requests is installed")
    except ImportError:
        print("✗ requests is not installed")
        return False
    
    try:
        import bs4
        print("✓ beautifulsoup4 is installed")
    except ImportError:
        print("✗ beautifulsoup4 is not installed")
        return False
    
    try:
        import pandas
        print("✓ pandas is installed")
    except ImportError:
        print("✗ pandas is not installed")
        return False
    
    return True

def test_website_connection(url, name):
    """Test that we can connect to a website."""
    print(f"Testing connection to {name}...")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        print(f"✓ Successfully connected to {name}")
        return True
    except Exception as e:
        print(f"✗ Failed to connect to {name}: {str(e)}")
        return False

def test_html_parsing(url, name):
    """Test that we can parse HTML from a website."""
    print(f"Testing HTML parsing for {name}...")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Check if we can find the <body> tag
        body = soup.find('body')
        if body:
            print(f"✓ Successfully parsed HTML from {name}")
            return True
        else:
            print(f"✗ Failed to parse HTML from {name}: No <body> tag found")
            return False
    except Exception as e:
        print(f"✗ Failed to parse HTML from {name}: {str(e)}")
        return False

def test_deal_finder_import():
    """Test that we can import the DealFinder class."""
    print("Testing DealFinder import...")
    
    try:
        from deal_finder import DealFinder
        print("✓ Successfully imported DealFinder")
        return True
    except Exception as e:
        print(f"✗ Failed to import DealFinder: {str(e)}")
        return False

def main():
    """Main function to run the tests."""
    print("=" * 80)
    print("Tech Deal Finder - Test Script")
    print("=" * 80)
    print()
    
    # Test dependencies
    if not test_dependencies():
        print("\nDependency test failed. Please install the required dependencies:")
        print("pip install -r requirements.txt")
        return False
    
    print()
    
    # Test website connections
    websites = [
        ("https://www.amazon.com", "Amazon"),
        ("https://www.bestbuy.com", "Best Buy"),
        ("https://www.walmart.com", "Walmart"),
        ("https://www.newegg.com", "Newegg")
    ]
    
    connection_results = []
    for url, name in websites:
        result = test_website_connection(url, name)
        connection_results.append(result)
        
        # Add a small delay to avoid being blocked
        time.sleep(random.uniform(1, 3))
    
    print()
    
    # Test HTML parsing
    parsing_results = []
    for url, name in websites:
        result = test_html_parsing(url, name)
        parsing_results.append(result)
        
        # Add a small delay to avoid being blocked
        time.sleep(random.uniform(1, 3))
    
    print()
    
    # Test DealFinder import
    import_result = test_deal_finder_import()
    
    print()
    print("=" * 80)
    print("Test Results")
    print("=" * 80)
    print()
    
    # Print dependency test results
    print("Dependencies: " + ("PASS" if all([
        'requests' in sys.modules,
        'bs4' in sys.modules,
        'pandas' in sys.modules
    ]) else "FAIL"))
    
    # Print website connection test results
    print("Website Connections: " + ("PASS" if all(connection_results) else "FAIL"))
    
    # Print HTML parsing test results
    print("HTML Parsing: " + ("PASS" if all(parsing_results) else "FAIL"))
    
    # Print DealFinder import test results
    print("DealFinder Import: " + ("PASS" if import_result else "FAIL"))
    
    # Print overall test results
    overall_result = all([
        all([
            'requests' in sys.modules,
            'bs4' in sys.modules,
            'pandas' in sys.modules
        ]),
        all(connection_results),
        all(parsing_results),
        import_result
    ])
    
    print()
    print("Overall: " + ("PASS" if overall_result else "FAIL"))
    
    return overall_result

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
