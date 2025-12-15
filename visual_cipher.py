import tkinter as tk
from tkinter import ttk, messagebox

from columnar_cipher import ColumnarTranspositionCipher


class CipherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Transposition Cipher")
        self.root.geometry("800x600")

        input_frame = ttk.LabelFrame(
            root, text="Input Key and Message/Ciphertext", padding=10
        )
        input_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(input_frame, text="Keyword (Key):").grid(
            row=0, column=0, sticky="w"
        )
        self.key_entry = ttk.Entry(input_frame, width=30)
        self.key_entry.grid(row=0, column=1, padx=5, pady=5)
        self.key_entry.insert(0, "SAMPLE")

        ttk.Label(input_frame, text="Message / Ciphertext:").grid(
            row=1, column=0, sticky="w"
        )
        self.msg_entry = ttk.Entry(input_frame, width=70)
        self.msg_entry.grid(row=1, column=1, padx=5, pady=5)
        self.msg_entry.insert(0, "THIS IS A SUPER SAMPLE")

        btn_frame = ttk.Frame(root, padding=10)
        btn_frame.pack(fill="x")

        encrypt_btn = ttk.Button(btn_frame, text="ENCRYPT", command=self.run_encrypt)
        encrypt_btn.pack(side="left", padx=20, expand=True)

        decrypt_btn = ttk.Button(btn_frame, text="DECRYPT", command=self.run_decrypt)
        decrypt_btn.pack(side="left", padx=20, expand=True)

        result_frame = ttk.LabelFrame(root, text="Transmission Log & Visualization", padding=10)
        result_frame.pack(fill="both", expand=True, padx=10, pady=5)

        ttk.Label(result_frame, text="Final Output:").pack(anchor="w")
        self.output_entry = ttk.Entry(result_frame, font=("Courier", 12))
        self.output_entry.pack(fill="x", pady=5)

        ttk.Label(result_frame, text="Internal Grid View (How it works):").pack(
            anchor="w", pady=(10, 0)
        )
        self.log_text = tk.Text(result_frame, height=15, font=("Courier", 11), bg="#f0f0f0")
        self.log_text.pack(fill="both", expand=True)

    def run_encrypt(self):
        key = self.key_entry.get().upper().replace(" ", "")
        msg = self.msg_entry.get().upper()

        if not key or not msg:
            messagebox.showerror("Error", "Please enter a key and a message.")
            return

        cipher = ColumnarTranspositionCipher(key)
        encrypted_text, grid = cipher.encrypt(msg)

        self.output_entry.delete(0, tk.END)
        self.output_entry.insert(0, encrypted_text)

        self.msg_entry.delete(0, tk.END)
        self.msg_entry.insert(0, encrypted_text)

        self.visualize_encrypt(key, grid, encrypted_text)

    def run_decrypt(self):
        key = self.key_entry.get().upper().replace(" ", "")
        ciphertext = self.msg_entry.get().upper()

        if not key or not ciphertext:
            messagebox.showerror("Error", "Please enter a key and ciphertext.")
            return

        if len(ciphertext) % len(key) != 0:
            messagebox.showerror(
                "Invalid Ciphertext",
                "Ciphertext length must be a multiple of the key length.\n"
                "Make sure you encrypt first, then decrypt the output."
            )
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
        self.log_text.delete(1.0, tk.END)
        log = []

        log.append("--- ENCRYPTION PROCESS ---")
        log.append(f"1. Keyword: {key}")
        log.append("2. Grid Layout (Written Row-by-Row):")
        log.append("-" * (len(key) * 4 + 1))

        header = "|"
        for char in key:
            header += f" {char} |"
        log.append(header)
        log.append("-" * (len(key) * 4 + 1))

        for row in grid:
            row_str = "|"
            for char in row:
                row_str += f" {char} |"
            log.append(row_str)

        log.append("-" * (len(key) * 4 + 1))

        log.append("\n3. Read Columns based on Alphabetical Key Order:")
        sorted_key = sorted(list(key))
        log.append(f"   Order: {', '.join(sorted_key)}")
        log.append("\n4. Final Packet (Ciphertext):")
        log.append(f"   {result}")

        self.log_text.insert(tk.END, "\n".join(log))

    def visualize_decrypt(self, key, grid, original_cipher):
        self.log_text.delete(1.0, tk.END)
        log = []

        log.append("--- DECRYPTION PROCESS ---")
        log.append(f"1. Incoming Packet: {original_cipher}")
        log.append("2. Reconstructing Grid (Column-by-Column)...")
        log.append(f"   Using Key: {key}")

        log.append("\n3. Final Grid State:")
        log.append("-" * (len(key) * 4 + 1))

        header = "|"
        for char in key:
            header += f" {char} |"
        log.append(header)
        log.append("-" * (len(key) * 4 + 1))

        for row in grid:
            row_str = "|"
            for char in row:
                row_str += f" {char} |"
            log.append(row_str)

        log.append("-" * (len(key) * 4 + 1))

        flat = "".join("".join(row) for row in grid)
        log.append("\n4. Read Row-by-Row (Plaintext):")
        log.append(f"   {flat}")

        self.log_text.insert(tk.END, "\n".join(log))


if __name__ == "__main__":
    root = tk.Tk()
    app = CipherApp(root)
    root.mainloop()
