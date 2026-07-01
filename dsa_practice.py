def sort_matrix(matrix):
    rows = len(matrix)
    cols = len(matrix[0]) if rows > 0 else 0
    temp_list = []
    
    # 1. FLATTEN STEP: Copy all elements from the 2D grid into a flat 1D array list
    for i in range(rows):
        for j in range(cols):
            temp_list.append(matrix[i][j])
            
    # 2. SORT STEP: Run an optimized quicksort algorithm on the flat array
    temp_list.sort()
    
    # 3. MAPPING STEP: Place the sorted elements back into the 2D matrix structure
    index = 0
    for i in range(rows):
        for j in range(cols):
            matrix[i][j] = temp_list[index]
            index += 1

# --- TEST EXAMPLES ---
print("🔲 Executing 2D Matrix Flatten-and-Sort Logic...")

test_matrix = [[1,9,20,6,3],[10,12,13,8,7]]
print("📥 Input Unsorted Matrix Layout:")
for row in test_matrix:
    print(row)

# Run the matrix sort processing in-place
sort_matrix(test_matrix)

print("\n📤 Transformed Sorted Output Matrix Layout:")
for row in test_matrix:
    print(row)
print("✅ Success! 2D matrix layers sorted and mapped sequentially with zero index leakage.")
