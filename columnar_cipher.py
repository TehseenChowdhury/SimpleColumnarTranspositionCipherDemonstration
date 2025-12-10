import math

class ColumnarTranspositionCipher:
    def __init__(self, key):
        self.key = key
        # Calculate the order immediately.
        # Example: "ZEBRA" -> [5, 2, 1, 4, 3]
        self.key_order = self._get_key_order(key)

    def _get_key_order(self, key):
        """
        The "Decorate-Sort-Undecorate" pattern.
        1. Pair each letter with its index: ('Z', 0), ('E', 1)...
        2. Sort by letter: ('A', 4), ('B', 2), ('E', 1)...
        3. Extract the indices: [4, 2, 1...]
        """
        key_indexed = [(char, i) for i, char in enumerate(key)]
        key_indexed.sort(key=lambda x: x[0])
        return [item[1] for item in key_indexed]

    def encrypt(self, message):
        """
        Writes message in Rows, reads out in Columns.
        """
        col_count = len(self.key)
        
        # 1. Padding: Add '_' until message fits the grid perfectly
        while len(message) % col_count != 0:
            message += "_"
            
        row_count = len(message) // col_count
        
        # 2. Create the Grid (Row by Row)
        grid = []
        for i in range(row_count):
            # Slice the string to get the next row
            row = message[i * col_count : (i + 1) * col_count]
            grid.append(list(row))
            
        # 3. Read Columns (in Key Order)
        ciphertext = ""
        for k in self.key_order:
            # Go down the rows for column 'k'
            for row in grid:
                ciphertext += row[k]
                
        return ciphertext, grid

    def decrypt(self, ciphertext):
        """
        Writes message in Columns, reads out in Rows.
        """
        col_count = len(self.key)
        row_count = len(ciphertext) // col_count
        
        # 1. Create an empty grid (Matrix of placeholders)
        grid = [['' for _ in range(col_count)] for _ in range(row_count)]
        
        # 2. Fill the columns based on Key Order
        msg_index = 0
        for k in self.key_order:
            # Fill down the column 'k'
            for r in range(row_count):
                grid[r][k] = ciphertext[msg_index]
                msg_index += 1
                
        # 3. Read the grid Row by Row
        plaintext = ""
        for row in grid:
            plaintext += "".join(row)
            
        # 4. Clean up padding
        return plaintext.rstrip("_"), grid