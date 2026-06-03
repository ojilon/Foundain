import os
import re

# File extensions to look for
EXTENSIONS = ('.java', '.kt', '.cpp', '.h', '.xml', '.properties')
# Folders to completely ignore
IGNORE_FOLDERS = {'build', 'gradle', '.git', 'node_modules', '.idea', 'obj'}

def strip_comments(text, ext):
    """Removes single-line and multi-line comments from code to save tokens."""
    if ext in ('.java', '.kt', '.cpp', '.h'):
        # Strip multi-line /* ... */ comments
        text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
        # Strip single-line // comments
        text = re.sub(r'//.*$', '', text, flags=M)
    elif ext == '.xml':
        # Strip XML <!-- ... --> comments
        text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
    return text

def main():
    output_file = "packed_code.txt"
    total_files = 0
    
    with open(output_file, "w", encoding="utf-8") as out:
        for root, dirs, files in os.walk("."):
            # Skip build and hidden directories
            dirs[:] = [d for d in dirs if d not in IGNORE_FOLDERS and not d.startswith('.')]
            
            for file in files:
                if file.endswith(EXTENSIONS):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()
                        
                        # Apply token-saving compressions
                        ext = os.path.splitext(file)[1]
                        content = strip_comments(content, ext)
                        
                        # Split lines to clean up whitespace
                        clean_lines = []
                        for line in content.splitlines():
                            line_stripped = line.strip()
                            if line_stripped:  # Skip completely empty lines
                                clean_lines.append(line)
                                
                        if clean_lines:
                            out.write(f'<file path="{file_path}">\n')
                            out.write("\n".join(clean_lines) + "\n")
                            out.write("</file>\n\n")
                            total_files += 1
                    except Exception as e:
                        print(f"Skipping {file_path} due to error: {e}")
                        
    print(f"Done! Packed {total_files} files into {output_file}.")

if __name__ == "__main__":
    main()
