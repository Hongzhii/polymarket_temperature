import sys

def print_surrounding_area(filepath, target_line, target_col, context_lines=5, context_chars=20):
    """
    Print the surrounding area of a specific line and column in a text file.
    
    Args:
        filepath (str): Path to the text file
        target_line (int): Line number (1-indexed)
        target_col (int): Column number (1-indexed)
        context_lines (int): Number of lines to show before and after target line
        context_chars (int): Number of characters to show before and after target column
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        # Convert to 0-indexed
        target_line_idx = target_line - 1
        target_col_idx = target_col - 1
        
        # Validate line number
        if target_line_idx < 0 or target_line_idx >= len(lines):
            print(f"Error: Line {target_line} is out of range (file has {len(lines)} lines)")
            return
        
        # Calculate line range
        start_line = max(0, target_line_idx - context_lines)
        end_line = min(len(lines), target_line_idx + context_lines + 1)
        
        print(f"File: {filepath}")
        print(f"Target: Line {target_line}, Column {target_col}")
        print("=" * 60)
        
        for i in range(start_line, end_line):
            line = lines[i].rstrip('\n')
            line_num = i + 1
            
            # Mark the target line
            marker = ">>>" if i == target_line_idx else "   "
            
            print(f"{marker} {line_num:3d}: {line}")
            
            # Show column pointer for target line
            if i == target_line_idx:
                if target_col_idx < len(line):
                    # Show character context around target column
                    start_col = max(0, target_col_idx - context_chars)
                    end_col = min(len(line), target_col_idx + context_chars + 1)
                    
                    pointer_line = " " * 8  # Align with line number
                    for j in range(start_col, end_col):
                        if j == target_col_idx:
                            pointer_line += "^"
                        else:
                            pointer_line += " "
                    
                    print(f"     COL: {pointer_line}")
                    print(f"          {line[start_col:end_col]}")
                    print(f"          Column {target_col} ('{line[target_col_idx] if target_col_idx < len(line) else 'EOF'}')")
                else:
                    print(f"     COL: Column {target_col} is beyond line end (line length: {len(line)})")
        
        print("=" * 60)
        
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found")
    except Exception as e:
        print(f"Error reading file: {e}")