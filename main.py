import re

# Original code snippet that we want to mutate.
# It contains a variable 'temp_value' that we intend to rename
# within a specific function, but not globally.
original_code = """
def calculate_something(input_data):
    # This is the 'temp_value' we want to rename to 'final_result'
    temp_value = input_data * 2
    if temp_value > 10:
        another_temp_value = temp_value - 5 # This is a different variable, should not be affected by 'temp_value' rename.
        return another_temp_value
    return temp_value

def process_data(data):
    # This 'temp_value' is in a different scope and should NOT be renamed.
    temp_value = data + 100
    print(f"Processing data with local temp_value: {temp_value}")
    return calculate_something(temp_value)
"""

print("--- Original Code ---")
print(original_code)

# --- Naive "RAG-like" Mutation Approach ---
# This simulates a simple Retrieval-Augmented Generation (RAG) approach
# that might retrieve occurrences of a string and generate a replacement
# without deep semantic understanding of code context or scope.
# It performs a global search-and-replace.
naive_mutated_code = original_code.replace("temp_value", "final_result")

print("\n--- Naive (RAG-like) Mutation (Incorrect) ---")
print(naive_mutated_code)
# Observe: The 'temp_value' in 'process_data' was also incorrectly renamed,
# demonstrating a lack of context awareness, a common challenge for basic RAG in code mutation.

# --- "MemStrata-like" Mutation Approach (Context-Aware) ---
# This simulates the *idea* of MemStrata's superior approach by applying
# a mutation with context awareness. Here, we'll only rename 'temp_value'
# within the 'calculate_something' function, understanding its scope.

def apply_memstrata_like_mutation(code_str):
    lines = code_str.split('\n')
    mutated_lines = []
    in_target_function_scope = False
    target_variable = r'\btemp_value\b' # Use regex for whole word matching
    new_variable_name = 'final_result'

    for line in lines:
        # Detect entry into the target function's scope
        if "def calculate_something" in line:
            in_target_function_scope = True
        # Detect exit from any function's scope (simplified for this example)
        elif line.strip().startswith("def") and in_target_function_scope:
            in_target_function_scope = False

        if in_target_function_scope:
            # Apply mutation only if within the target function's scope
            # This represents MemStrata's conceptual ability to understand and act on code context.
            line = re.sub(target_variable, new_variable_name, line)
        mutated_lines.append(line)
    return "\n".join(mutated_lines)

memstrata_mutated_code = apply_memstrata_like_mutation(original_code)

print("\n--- MemStrata-like Mutation (Context-Aware and Correct) ---")
print(memstrata_mutated_code)
# Observe: Only 'temp_value' within 'calculate_something' was renamed.
# The 'temp_value' in 'process_data' remains untouched, demonstrating
# a superior, context-aware approach to code mutation.
