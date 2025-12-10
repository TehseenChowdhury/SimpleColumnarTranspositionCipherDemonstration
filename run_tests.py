from columnar_cipher import ColumnarTranspositionCipher

def presentation_demo():
    print("CIPHER DEMONSTRATION")

    # 1. Configuration
    my_key = "CYBER"  # I switched this back to CYBER for you since you liked that example
    my_message = "DEFEND THE CASTLE AT DAWN"
    
    cipher = ColumnarTranspositionCipher(my_key)

    print(f"KEY:     {my_key}")
    print(f"MESSAGE: {my_message}")
    print("-" * 40)

    # 2. Encryption Demo
    # The encrypt function now returns TWO things: (ciphertext, grid).
    # We use 'encrypted_text' for the message, and '_' to ignore the grid for this text-only demo.
    encrypted_text, _ = cipher.encrypt(my_message)
    
    print(f"Step 1: Encryption")
    print(f"RESULT (Ciphertext): {encrypted_text}")
    
    print("-" * 40)

    # 3. Decryption Demo
    # CRITICAL: We pass ONLY the 'encrypted_text' string, not the tuple.
    decrypted_text, _ = cipher.decrypt(encrypted_text)
    
    print(f"Step 2: Decryption")
    print(f"RESULT (Plaintext):  {decrypted_text}")

    # 4. Verification
    if my_message == decrypted_text:
        print("\n[SUCCESS] Decrypted message matches original.")
    else:
        print("\n[FAIL] Messages do not match.")

if __name__ == "__main__":
    presentation_demo()