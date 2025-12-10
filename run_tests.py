from columnar_cipher import ColumnarTranspositionCipher

def run_demo():
    print("=== Cyber Security Project: Columnar Transposition Cipher ===")
    print("-----------------------------------------------------------")

    # 1. Setup
    my_key = "CYBER"
    cipher = ColumnarTranspositionCipher(my_key)
    
    # 2. Define a message
    original_message = "DEFEND THE CASTLE AT DAWN"
    print(f"Key:              {my_key}")
    print(f"Original Message: {original_message}")

    # 3. Encrypt
    encrypted_msg = cipher.encrypt(original_message)
    print(f"Encrypted (Ciphertext): {encrypted_msg}")
    
    # Explain what just happened for the demo
    print("\n[Explanation]:")
    print(f"The key '{my_key}' has length {len(my_key)}.")
    print(f"The message was padded and written into rows of {len(my_key)}.")
    print("Then we read the columns in alphabetical order of the key (B, C, E, R, Y).")

    # 4. Decrypt
    decrypted_msg = cipher.decrypt(encrypted_msg)
    print(f"\nDecrypted (Plaintext):  {decrypted_msg}")

    # 5. Verification
    if original_message == decrypted_msg:
        print("\n[SUCCESS] Decryption matches original message.")
    else:
        print("\n[FAIL] Decryption did not match.")

    print("-----------------------------------------------------------")

def run_custom_test():
    """
    Small helper to let you type in your own inputs during the presentation if asked.
    """
    print("\n--- Interactive Mode ---")
    k = input("Enter a keyword (e.g., SECRET): ").strip()
    m = input("Enter a message to encrypt: ").strip()
    
    c = ColumnarTranspositionCipher(k)
    enc = c.encrypt(m)
    dec = c.decrypt(enc)
    
    print(f"\nCiphertext: {enc}")
    print(f"Decrypted:  {dec}")

if __name__ == "__main__":
    run_demo()
    # Uncomment the line below if you want to type inputs manually
    # run_custom_test()