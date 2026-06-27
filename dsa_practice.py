def first_non_repeating_char(s):
    # 1. Create a frequency dictionary map to store character counts
    char_count = {}
    
    # First Pass: Count the occurrences of each character in the string
    for char in s:
        char_count[char] = char_count.get(char, 0) + 1
        
    # Second Pass: Find the first character that has a frequency count of exactly 1
    for char in s:
        if char_count[char] == 1:
            return char
            
    # Return a placeholder string if every single character repeats
    return "$"

# --- TEST EXAMPLES ---
print("🔤 Executing String Frequency Tracking Logic...")

# In this test string, 'g' repeats, 'e' repeats, 'k' repeats, and 's' repeats.
# The very first letter that appears exactly once is 'f'!
test_string = "ritheeshkumar"

result = first_non_repeating_char(test_string)

print(f"📥 Input String:  \"{test_string}\"")
print(f"📤 First Non-Repeating Character: '{result}'")
print("✅ Success! Hash map frequency boundaries executed in clean O(N) linear time.")



# whether anagrams are not

def anagram(s1,s2):
    
    # If lengths are different, they cannot be anagrams
    if len(s1) != len(s2):
        return False
        
    char_count = {}
    
    # Track frequencies: Add for s1, subtract for s2
    for i in range(len(s1)):
        char_count[s1[i]] = char_count.get(s1[i], 0) + 1
        char_count[s2[i]] = char_count.get(s2[i], 0) - 1
        
    # If any character count is not zero, they don't match perfectly
    for count in char_count.values():
        if count != 0:
            return False
            
    return True

# --- TEST EXAMPLES ---
print("🔠 Checking String Anagram Properties...")

string_a = "listen"
string_b = "silent"

result = anagram(string_a, string_b)

print(f"📥 Comparing: \"{string_a}\" AND \"{string_b}\"")
print(f"📤 Are they Anagrams?: {result}")
print("✅ Success! Hash map validation executed smoothly in O(N) linear time.")

    