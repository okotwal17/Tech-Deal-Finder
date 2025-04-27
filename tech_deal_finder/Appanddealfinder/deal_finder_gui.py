#!/usr/bin/env python3
"""
Tech Deal Finder GUI - A graphical interface for the Tech Deal Finder.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import sys
import io
import contextlib
from deal_finder import DealFinder
import pandas as pd
import webbrowser

class RedirectText:
    """Class to redirect stdout to a tkinter Text widget."""    
    def __init__(self, text_widget):
        """Initialize with the text widget to redirect to."""
        self.text_widget = text_widget
        self.buffer = ""
        
    def write(self, string):
        """Write to the text widget."""
        self.buffer += string
        self.text_widget.configure(state="normal")
        self.text_widget.insert(tk.END, string)
        self.text_widget.see(tk.END)
        self.text_widget.configure(state="disabled")
        
    def flush(self):
        """Flush the buffer."""
        self.text_widget.configure(state="normal")
        self.text_widget.insert(tk.END, self.buffer)
        self.buffer = ""
        self.text_widget.see(tk.END)
        self.text_widget.configure(state="disabled")


class DealFinderGUI:
    """GUI for the Tech Deal Finder."""
    

    def __init__(self, root):
        self.root = root
        self.root.title("Tech Deal Finder")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)

        # Create style object for customizations
        self.style = ttk.Style()
        self.style.configure("TButton", padding=6, relief="flat", background="#4CAF50", foreground="white")
        self.style.configure("TLabel", background="#f0f0f0", font=("Arial", 12, "bold"))
        self.style.configure("TFrame", background="#f0f0f0")

        # Set background color for main window
        self.root.configure(bg="#F0F0F0")

        # Create the main frame
        self.main_frame = ttk.Frame(self.root, padding="10", style="TFrame")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Create search frame with padding
        self.search_frame = ttk.Frame(self.main_frame, padding="10")
        self.search_frame.pack(fill=tk.X, pady=(10, 10))

        # Create search label with custom styling
        self.search_label = ttk.Label(self.search_frame, text="What technology product are you looking for?")
        self.search_label.pack(side=tk.LEFT, padx=(0, 10))

        # Search entry and button with styling
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(self.search_frame, textvariable=self.search_var, width=40)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.search_button = ttk.Button(self.search_frame, text="Search", command=self.search)
        self.search_button.pack(side=tk.LEFT, padx=(10, 0))

        # Create output and results tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Set status bar
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def __init__(self, root):
        """Initialize the GUI."""
        self.root = root
        self.root.title("Tech Deal Finder")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # Set icon (if available)
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
        
        # Create the main frame
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create the search frame
        self.search_frame = ttk.Frame(self.main_frame)
        self.search_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Create the search label
        self.search_label = ttk.Label(self.search_frame, text="What technology product are you looking for?", font=("Arial", 12, "bold"))
        self.search_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Create the search entry
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(self.search_frame, textvariable=self.search_var, width=40, font=("Arial", 12))
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.search_entry.bind("<Return>", self.search)
        
        # Create the search button
        self.search_button = ttk.Button(self.search_frame, text="Search", command=self.search, width=12)
        self.search_button.pack(side=tk.LEFT, padx=(10, 0))
        
        # Create the options frame
        self.options_frame = ttk.Frame(self.main_frame)
        self.options_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Create the max results label
        self.max_results_label = ttk.Label(self.options_frame, text="Max results per website:", font=("Arial", 10))
        self.max_results_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Create the max results spinbox
        self.max_results_var = tk.IntVar(value=5)
        self.max_results_spinbox = ttk.Spinbox(self.options_frame, from_=1, to=20, textvariable=self.max_results_var, width=5)
        self.max_results_spinbox.pack(side=tk.LEFT)
        
        # Create the save results checkbox
        self.save_results_var = tk.BooleanVar(value=True)
        self.save_results_checkbox = ttk.Checkbutton(self.options_frame, text="Save results to file", variable=self.save_results_var, font=("Arial", 10))
        self.save_results_checkbox.pack(side=tk.LEFT, padx=(20, 0))
        
        # Create the notebook for output and results
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create the output tab
        self.output_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.output_frame, text="Output")
        
        # Create the output text
        self.output_text = scrolledtext.ScrolledText(self.output_frame, wrap=tk.WORD, state="disabled", font=("Courier", 10))
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Create the results tab
        self.results_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.results_frame, text="Results")
        
        # Create the results treeview
        self.results_tree = ttk.Treeview(self.results_frame, columns=("price", "website"), show="headings", height=8)
        self.results_tree.heading("price", text="Price", anchor="center")
        self.results_tree.heading("website", text="Website", anchor="center")
        self.results_tree.column("price", width=100, anchor="center")
        self.results_tree.column("website", width=200, anchor="center")
        self.results_tree.pack(fill=tk.BOTH, expand=True)
        
        # Add a scrollbar to the treeview
        self.results_scrollbar = ttk.Scrollbar(self.results_tree, orient="vertical", command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=self.results_scrollbar.set)
        self.results_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind double-click on treeview to open URL
        self.results_tree.bind("<Double-1>", self.open_url)
        
        # Create the status bar
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W, font=("Arial", 10))
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Set the status
        self.status_var.set("Ready")
        
        # Store the results
        self.results_df = None
        
        # Redirect stdout to the output text
        self.redirect = RedirectText(self.output_text)
        
    def search(self, event=None):
        """Search for the product."""
        # Get the search query
        product_query = self.search_var.get().strip()
        
        # Check if the search query is empty
        if not product_query:
            messagebox.showerror("Error", "Please enter a product to search for.")
            return
        
        # Clear the output text
        self.output_text.configure(state="normal")
        self.output_text.delete(1.0, tk.END)
        self.output_text.configure(state="disabled")
        
        # Clear the results treeview
        self.results_tree.delete(*self.results_tree.get_children())
        
        # Set the status
        self.status_var.set("Searching...")
        
        # Disable the search button
        self.search_button.configure(state="disabled")
        
        # Switch to the output tab
        self.notebook.select(0)
        
        # Start the search in a separate thread
        threading.Thread(target=self._search_thread, args=(product_query,), daemon=True).start()
        
    def _search_thread(self, product_query):
        """Run the search in a separate thread."""
        try:
            # Redirect stdout to the output text
            old_stdout = sys.stdout
            sys.stdout = self.redirect
            
            # Create the deal finder
            deal_finder = DealFinder(
                product_query=product_query,
                max_results=self.max_results_var.get(),
                save_results=self.save_results_var.get()
            )
            
            # Search for the product
            self.results_df = deal_finder.search_all_websites()
            
            # Display the results
            deal_finder.display_results(self.results_df)
            
            # Restore stdout
            sys.stdout = old_stdout
            
            # Update the results treeview
            self.root.after(0, self._update_results)
            
        except Exception as e:
            # Show the error
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            
        finally:
            # Enable the search button
            self.root.after(0, lambda: self.search_button.configure(state="normal"))
            
            # Set the status
            self.root.after(0, lambda: self.status_var.set("Ready"))
    
    def _update_results(self):
        """Update the results treeview."""
        # Check if there are results
        if self.results_df is None or self.results_df.empty:
            return
        
        # Clear the results treeview
        self.results_tree.delete(*self.results_tree.get_children())
        
        # Add the results to the treeview
        for _, row in self.results_df.iterrows():
            self.results_tree.insert("", "end", text=row["title"], values=(f"${row['price']:.2f}", row["website"]), tags=(row["url"],))
        
        # Switch to the results tab
        self.notebook.select(1)
    
    def open_url(self, event):
        """Open the URL of the selected result."""
        # Get the selected item
        item = self.results_tree.selection()[0]
        
        # Get the URL
        url = self.results_tree.item(item, "tags")[0]
        
        # Open the URL in the default browser
        webbrowser.open(url)


def main():
    """Main function to run the GUI."""
    root = tk.Tk()
    app = DealFinderGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
