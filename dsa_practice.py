# row with max ones
def row_with_max_1s(matrix):
    rows = len(matrix)
    cols = len(matrix[0]) if rows > 0 else 0
    
    max_row_index = -1
    # Start at the top-right corner of the matrix layout grid
    current_col = cols - 1
    current_row = 0
    
    while current_row < rows and current_col >= 0:
        # If we spot a 1, move left to check for a better maximum count
        if matrix[current_row][current_col] == 1:
            max_row_index = current_row
            current_col -= 1
        else:
            # If we spot a 0, this row can't beat our current run. Step down!
            current_row += 1
            
    return max_row_index

# --- TEST EXAMPLES ---
print("🧱 Running Problem 1: Row with Max 1s...")
matrix = [
    [0, 0, 1, 1], # Row 0
    [0, 0, 0, 1], # Row 1
    [1, 1, 1, 1], # Row 2
    [0, 0, 0, 0]  # Row 3
]

print(f"📤 Row Index with most 1s: {row_with_max_1s(matrix)} (Expected: 2)")


#find target in 2d matrix

def search_matrix(matrix, target):
    if not matrix or not matrix[0]:
        return False
        
    rows = len(matrix)
    cols = len(matrix[0])
    
    # Define binary search pointers as if it's a flat 1D array list bound
    low = 0
    high = (rows * cols) - 1
    
    while low <= high:
        mid = (low + high) // 2
        # Virtual mapping trick: Convert 1D index back to 2D coordinates [row][col]
        mid_val = matrix[mid // cols][mid % cols]
        
        if mid_val == target:
            return True
        elif mid_val < target:
            low = mid + 1
        else:
            high = mid - 1
            
    return False

# --- TEST EXAMPLES ---
print("\n🔍 Running Problem 2: Search in Sorted 2D Matrix...")
test_matrix_2 = [[1,2,3,4],[6,7,8,9]]

target_num = 3
print(f"📤 Found target {target_num}?: {search_matrix(test_matrix_2, target_num)} (Expected: True)")

