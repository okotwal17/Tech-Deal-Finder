#!/usr/bin/env python3
"""
Tech Deal Finder - A web scraper that finds the best deals on technology products.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
import random
from urllib.parse import quote_plus
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from datetime import datetime

# User agent to mimic a browser
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

# Headers for HTTP requests
HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
}

# List of e-commerce websites to search
WEBSITES = {
    "amazon": {
        "name": "Amazon",
        "search_url": "https://www.amazon.com/s?k={}",
        "base_url": "https://www.amazon.com"
    },
    "bestbuy": {
        "name": "Best Buy",
        "search_url": "https://www.bestbuy.com/site/searchpage.jsp?st={}",
        "base_url": "https://www.bestbuy.com"
    },
    "walmart": {
        "name": "Walmart",
        "search_url": "https://www.walmart.com/search?q={}",
        "base_url": "https://www.walmart.com"
    },
    "newegg": {
        "name": "Newegg",
        "search_url": "https://www.newegg.com/p/pl?d={}",
        "base_url": "https://www.newegg.com"
    }
}

class DealFinder:
    """Main class for finding tech deals across multiple websites."""
    
    def __init__(self, product_query, max_results=5, save_results=True):
        """
        Initialize the DealFinder.
        
        Args:
            product_query (str): The product to search for
            max_results (int): Maximum number of results to return per website
            save_results (bool): Whether to save results to a file
        """
        self.product_query = product_query
        self.max_results = max_results
        self.save_results = save_results
        self.results = []
        
    def search_all_websites(self):
        """Search all websites for the product."""
        print(f"\nSearching for '{self.product_query}' across multiple websites...\n")
        
        # Use ThreadPoolExecutor to search websites concurrently
        with ThreadPoolExecutor(max_workers=len(WEBSITES)) as executor:
            futures = {executor.submit(self.search_website, site_id): site_id for site_id in WEBSITES}
            
            for future in futures:
                try:
                    future.result()
                except Exception as e:
                    site_id = futures[future]
                    print(f"Error searching {WEBSITES[site_id]['name']}: {str(e)}")
        
        # Convert results to DataFrame for easier manipulation
        if self.results:
            df = pd.DataFrame(self.results)
            
            # Sort by price (ascending)
            df = df.sort_values('price')
            
            # Save results if requested
            if self.save_results:
                self._save_results(df)
                
            return df
        else:
            print("No results found.")
            return pd.DataFrame()
    
    def search_website(self, site_id):
        """
        Search a specific website for the product.
        
        Args:
            site_id (str): The ID of the website to search
        """
        website = WEBSITES[site_id]
        print(f"Searching {website['name']}...")
        
        # Format the search URL with the product query
        search_url = website['search_url'].format(quote_plus(self.product_query))
        
        try:
            # Make the HTTP request
            response = requests.get(search_url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            
            # Parse the HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract product information based on the website
            if site_id == 'amazon':
                self._parse_amazon(soup, website)
            elif site_id == 'bestbuy':
                self._parse_bestbuy(soup, website)
            elif site_id == 'walmart':
                self._parse_walmart(soup, website)
            elif site_id == 'newegg':
                self._parse_newegg(soup, website)
            
            # Add a small delay to avoid being blocked
            time.sleep(random.uniform(1, 3))
            
        except Exception as e:
            print(f"Error searching {website['name']}: {str(e)}")
    
    def _parse_amazon(self, soup, website):
        """Parse Amazon search results."""
        products = soup.select('div.s-result-item[data-component-type="s-search-result"]')
        count = 0
        
        for product in products:
            if count >= self.max_results:
                break
                
            try:
                # Extract product title
                title_element = product.select_one('h2 a span')
                if not title_element:
                    continue
                title = title_element.text.strip()
                
                # Extract product URL
                url_element = product.select_one('h2 a')
                if not url_element or not url_element.get('href'):
                    continue
                url = website['base_url'] + url_element['href'] if url_element['href'].startswith('/') else url_element['href']
                
                # Extract product price
                price_element = product.select_one('span.a-price .a-offscreen')
                if not price_element:
                    continue
                price_text = price_element.text.strip()
                price = self._extract_price(price_text)
                
                # Extract product image
                img_element = product.select_one('img.s-image')
                img_url = img_element['src'] if img_element else ""
                
                # Add to results
                self.results.append({
                    'title': title,
                    'price': price,
                    'website': website['name'],
                    'url': url,
                    'img_url': img_url
                })
                
                count += 1
                
            except Exception as e:
                print(f"Error parsing Amazon product: {str(e)}")
    
    def _parse_bestbuy(self, soup, website):
        """Parse Best Buy search results."""
        products = soup.select('li.sku-item')
        count = 0
        
        for product in products:
            if count >= self.max_results:
                break
                
            try:
                # Extract product title
                title_element = product.select_one('h4.sku-title a')
                if not title_element:
                    continue
                title = title_element.text.strip()
                
                # Extract product URL
                url = website['base_url'] + title_element['href'] if title_element.get('href') else ""
                
                # Extract product price
                price_element = product.select_one('div.priceView-customer-price span')
                if not price_element:
                    continue
                price_text = price_element.text.strip()
                price = self._extract_price(price_text)
                
                # Extract product image
                img_element = product.select_one('img.product-image')
                img_url = img_element['src'] if img_element and img_element.get('src') else ""
                
                # Add to results
                self.results.append({
                    'title': title,
                    'price': price,
                    'website': website['name'],
                    'url': url,
                    'img_url': img_url
                })
                
                count += 1
                
            except Exception as e:
                print(f"Error parsing Best Buy product: {str(e)}")
    
    def _parse_walmart(self, soup, website):
        """Parse Walmart search results."""
        products = soup.select('div[data-item-id]')
        count = 0
        
        for product in products:
            if count >= self.max_results:
                break
                
            try:
                # Extract product title
                title_element = product.select_one('span.lh-title')
                if not title_element:
                    continue
                title = title_element.text.strip()
                
                # Extract product URL
                url_element = product.select_one('a[link-identifier="linkText"]')
                if not url_element or not url_element.get('href'):
                    continue
                url = website['base_url'] + url_element['href'] if url_element['href'].startswith('/') else url_element['href']
                
                # Extract product price
                price_element = product.select_one('div[data-automation-id="product-price"] span.w_iUH7')
                if not price_element:
                    continue
                price_text = price_element.text.strip()
                price = self._extract_price(price_text)
                
                # Extract product image
                img_element = product.select_one('img')
                img_url = img_element['src'] if img_element and img_element.get('src') else ""
                
                # Add to results
                self.results.append({
                    'title': title,
                    'price': price,
                    'website': website['name'],
                    'url': url,
                    'img_url': img_url
                })
                
                count += 1
                
            except Exception as e:
                print(f"Error parsing Walmart product: {str(e)}")
    
    def _parse_newegg(self, soup, website):
        """Parse Newegg search results."""
        products = soup.select('div.item-cell')
        count = 0
        
        for product in products:
            if count >= self.max_results:
                break
                
            try:
                # Extract product title
                title_element = product.select_one('a.item-title')
                if not title_element:
                    continue
                title = title_element.text.strip()
                
                # Extract product URL
                url = title_element['href'] if title_element.get('href') else ""
                
                # Extract product price
                price_element = product.select_one('li.price-current strong')
                if not price_element:
                    continue
                price_text = price_element.text.strip()
                price_decimal = product.select_one('li.price-current sup')
                if price_decimal:
                    price_text += price_decimal.text.strip()
                price = self._extract_price(price_text)
                
                # Extract product image
                img_element = product.select_one('img.item-img')
                img_url = img_element['src'] if img_element and img_element.get('src') else ""
                
                # Add to results
                self.results.append({
                    'title': title,
                    'price': price,
                    'website': website['name'],
                    'url': url,
                    'img_url': img_url
                })
                
                count += 1
                
            except Exception as e:
                print(f"Error parsing Newegg product: {str(e)}")
    
    def _extract_price(self, price_text):
        """
        Extract the price as a float from a price string.
        
        Args:
            price_text (str): The price text (e.g., "$1,299.99")
            
        Returns:
            float: The price as a float
        """
        # Remove currency symbols and commas
        price_text = re.sub(r'[^\d.]', '', price_text)
        
        try:
            return float(price_text)
        except ValueError:
            return float('inf')  # Return infinity if price can't be parsed
    
    def _save_results(self, df):
        """
        Save results to a JSON file.
        
        Args:
            df (DataFrame): The results DataFrame
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"results_{timestamp}.json"
        
        # Convert DataFrame to JSON
        results_json = df.to_json(orient='records')
        
        # Save to file
        with open(filename, 'w') as f:
            f.write(results_json)
            
        print(f"\nResults saved to {filename}")
    
    def display_results(self, df):
        """
        Display the results in a user-friendly format.
        
        Args:
            df (DataFrame): The results DataFrame
        """
        if df.empty:
            print("No results found.")
            return
        
        print("\n" + "="*80)
        print(f"BEST DEALS FOR: {self.product_query}")
        print("="*80)
        
        # Find the best deal
        best_deal = df.iloc[0]
        print(f"\nBEST DEAL: {best_deal['title']}")
        print(f"Price: ${best_deal['price']:.2f}")
        print(f"Website: {best_deal['website']}")
        print(f"URL: {best_deal['url']}")
        
        # Display all results
        print("\nALL RESULTS:")
        print("-"*80)
        
        for i, (_, product) in enumerate(df.iterrows(), 1):
            print(f"{i}. {product['title']}")
            print(f"   Price: ${product['price']:.2f}")
            print(f"   Website: {product['website']}")
            print(f"   URL: {product['url']}")
            print("-"*80)


def main():
    """Main function to run the deal finder."""
    parser = argparse.ArgumentParser(description='Find the best deals on technology products.')
    parser.add_argument('product', nargs='?', help='The product to search for')
    parser.add_argument('--max-results', type=int, default=5, help='Maximum number of results per website')
    parser.add_argument('--no-save', action='store_true', help='Do not save results to a file')
    
    args = parser.parse_args()
    
    # If no product is provided via command line, ask for it
    product_query = args.product
    if not product_query:
        product_query = input("What technology product are you looking for? ")
    
    # Create and run the deal finder
    deal_finder = DealFinder(
        product_query=product_query,
        max_results=args.max_results,
        save_results=not args.no_save
    )
    
    results = deal_finder.search_all_websites()
    deal_finder.display_results(results)


if __name__ == "__main__":
    main()
