import tkinter as tk
from tkinter import ttk, messagebox

from matplotlib.pyplot import grid
# Import the logic class from the other file
from columnar_cipher import ColumnarTranspositionCipher

class CipherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Transposition Cipher")
        self.root.geometry("800x600")

        # --- Top Section: Inputs ---
        # LabelFrame creates a box with a title around the inputs
        input_frame = ttk.LabelFrame(root, text="Input Key and Message/Ciphertext", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        # Grid Layout: Row 0 is for Key, Row 1 is for Message
        ttk.Label(input_frame, text="Keyword (Key):").grid(row=0, column=0, sticky="w")
        self.key_entry = ttk.Entry(input_frame, width=30)
        self.key_entry.grid(row=0, column=1, padx=5, pady=5)
        self.key_entry.insert(0, "SAMPLE") # Default text

        ttk.Label(input_frame, text="Message:").grid(row=1, column=0, sticky="w")
        self.msg_entry = ttk.Entry(input_frame, width=70)
        self.msg_entry.grid(row=1, column=1, padx=5, pady=5)
        self.msg_entry.insert(0, "THIS IS A SUPER SAMPLE") # Default text

        # --- Middle Section: Buttons ---
        btn_frame = ttk.Frame(root, padding=10)
        btn_frame.pack(fill="x")
        
        # Buttons trigger the functions (command=self.run_encrypt)
        encrypt_btn = ttk.Button(btn_frame, text="ENCRYPT", command=self.run_encrypt)
        encrypt_btn.pack(side="left", padx=20, expand=True)
        
        decrypt_btn = ttk.Button(btn_frame, text="DECRYPT", command=self.run_decrypt)
        decrypt_btn.pack(side="left", padx=20, expand=True)

        # --- Bottom Section: Results & Visualization ---
        result_frame = ttk.LabelFrame(root, text="Transmission Log & Visualization", padding=10)
        result_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Output box for the final result string
        ttk.Label(result_frame, text="Final Output:").pack(anchor="w")
        self.output_entry = ttk.Entry(result_frame, font=('Courier', 12))
        self.output_entry.pack(fill="x", pady=5)

        # Text box for drawing the grid visualization
        ttk.Label(result_frame, text="Internal Grid View (How it works):").pack(anchor="w", pady=(10, 0))
        self.log_text = tk.Text(result_frame, height=15, font=('Courier', 11), bg="#f0f0f0")
        self.log_text.pack(fill="both", expand=True)

    def run_encrypt(self):
        """
        Gets input, runs logic, and updates UI for Encryption.
        """
        # Get text from input boxes and clean it up
        key = self.key_entry.get().upper().replace(" ", "")
        msg = self.msg_entry.get().upper()
        
        if not key or not msg:
            messagebox.showerror("Error", "Please enter a key and a message.")
            return

        # Initialize the logic class
        cipher = ColumnarTranspositionCipher(key)
        encrypted_text, grid = cipher.encrypt(msg)
        
        # Update the 'Final Output' box
        self.output_entry.delete(0, tk.END)
        self.output_entry.insert(0, encrypted_text)
        
        # Draw the grid in the bottom text box
        self.visualize_encrypt(key, grid, encrypted_text)

    def run_decrypt(self):
        """
        Gets input, runs logic, and updates UI for Decryption.
        """
        key = self.key_entry.get().upper().replace(" ", "")
        ciphertext = self.msg_entry.get().upper()
        
        if not key or not ciphertext:
            messagebox.showerror("Error", "Please enter a key and ciphertext.")
            return

        cipher = ColumnarTranspositionCipher(key)
        try:
            plaintext, grid = cipher.decrypt(ciphertext)
            
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, plaintext)
            
            self.visualize_decrypt(key, grid, ciphertext)
        except Exception as e:
            messagebox.showerror("Decryption Error", str(e))

    def visualize_encrypt(self, key, grid, result):
        """
        Helper to draw the text-based grid in the log window.
        """
        self.log_text.delete(1.0, tk.END) # Clear previous text
        log = []
        
        log.append(f"--- ENCRYPTION PROCESS ---")
        log.append(f"1. Keyword: {key}")
        log.append(f"2. Grid Layout (Written Row-by-Row):")
        log.append("-" * (len(key) * 4 + 1))
        
        # Create Grid Header
        header = "|"
        for char in key:
            header += f" {char} |"
        log.append(header)
        log.append("-" * (len(key) * 4 + 1))
        
        # Create Grid Rows
        for row in grid:
            row_str = "|"
            for char in row:
                row_str += f" {char} |"
            log.append(row_str)
            
        log.append("-" * (len(key) * 4 + 1))
        
        log.append(f"\n3. Read Columns based on Alphabetical Key Order:")
        sorted_key = sorted(list(key))
        log.append(f"   Order: {', '.join(sorted_key)}")
        log.append(f"\n4. Final Packet (Ciphertext):")
        log.append(f"   {result}")
        
        # Insert all lines into the Text widget
        self.log_text.insert(tk.END, "\n".join(log))

    def visualize_decrypt(self, key, grid, original_cipher):
        """
        Helper to draw the text-based grid for decryption.
        """
        self.log_text.delete(1.0, tk.END)
        log = []
        
        log.append(f"--- DECRYPTION PROCESS ---")
        log.append(f"1. Incoming Packet: {original_cipher}")
        log.append(f"2. Reconstructing Grid (Column-by-Column)...")
        log.append(f"   Using Key: {key}")
        
        log.append("\n3. Final Grid State:")
        log.append("-" * (len(key) * 4 + 1))
        
        # Header
        header = "|"
        for char in key:
            header += f" {char} |"
        log.append(header)
        log.append("-" * (len(key) * 4 + 1))
        
        # Rows
        for row in grid:
            row_str = "|"
            for char in row:
                row_str += f" {char} |"
            log.append(row_str)
        log.append("-" * (len(key) * 4 + 1))
        
        # Result
        # Flatten grid to show reading process
        flat = "".join(''.join(row) for row in grid)

        log.append(f"\n4. Read Row-by-Row (Plaintext):")
        log.append(f"   {flat}")
        
        self.log_text.insert(tk.END, "\n".join(log))

if __name__ == "__main__":
    # Create the main window
    root = tk.Tk()
    # Initialize the application
    app = CipherApp(root)
    # Start the event loop (keeps window open)
    root.mainloop()