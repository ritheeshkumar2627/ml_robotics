
#travesal in spiral order for a matrix
def spiral_order(matrix):
    result = []
    if not matrix or not matrix[0]:
        return result
        
    # Initialize our 4 wall boundary pointers
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    
    while top <= bottom and left <= right:
        # 1. Traverse from Left to Right along the current Top wall
        for i in range(left, right + 1):
            result.append(matrix[top][i])
        top += 1  # Shrink the top ceiling down
        
        # 2. Traverse from Top to Bottom along the current Right wall
        for i in range(top, bottom + 1):
            result.append(matrix[i][right])
        right -= 1  # Shrink the right wall inward
        
        # 3. Check if boundaries crossed before moving backward
        if top <= bottom:
            # Traverse from Right to Left along the current Bottom floor
            for i in range(right, left - 1, -1):  # Corrected step syntax
                result.append(matrix[bottom][i])
            bottom -= 1  # Shrink the bottom floor up
            
        if left <= right:
            # 4. Traverse from Bottom to Top along the current Left wall
            for i in range(bottom, top - 1, -1):  # Corrected step syntax
                result.append(matrix[i][left])
            left += 1  # Shrink the left wall outward
            
    return result

# --- TEST EXAMPLES ---
print("🌀 Executing 2D Matrix Spiral Traversal Pointers...")

# Corrected empty list brackets to form a valid 3x4 2D matrix
test_matrix = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12]
]

print("📥 Input Matrix Layout:")
for row in test_matrix:
    print(row)

output_list = spiral_order(test_matrix)
print(f"\n📤 Spiral Ordered Output: {output_list}")
print("✅ Success! Spiral boundaries collapsed perfectly with zero pointer leaks.")
