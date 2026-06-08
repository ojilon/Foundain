import os
import re

EXTENSIONS = ('.java', '.kt', '.cpp', '.h', '.xml')
IGNORE_FOLDERS = {'build', 'gradle', '.git', 'node_modules', '.idea', 'obj'}

def extract_skeleton(text, ext):
    """Extracts only layout structures or class/method definitions to save massive token counts."""
    if ext in ('.java', '.kt'):
        # Keep class, interface, package, imports, and method signatures
        lines = []
        for line in text.splitlines():
            line_stripped = line.strip()
            # Match imports, packages, annotations, class declarations, and method/variable declarations
            if any(x in line_stripped for x in ['package ', 'import ', 'class ', 'interface ', 'public ', 'private ', 'protected ']):
                # If it's a method body line without signatures, skip it
                if '{' in line_stripped or '}' in line_stripped or ';' in line_stripped:
                    lines.append(line)
        return "\n".join(lines)
        
    elif ext in ('.cpp', '.h'):
        # Keep class, structural namespaces, and function signatures
        lines = []
        for line in text.splitlines():
            line_stripped = line.strip()
            if any(x in line_stripped for x in ['#include', 'namespace', 'class ', 'struct ', 'void ', 'int ', 'bool ', 'char ']) or line_stripped.endswith(';'):
                lines.append(line)
        return "\n".join(lines)
        
    elif ext == '.xml':
        # Strip all heavy strings and descriptions, keep only layout/theme tag hierarchies
        # Remove android:text and android:title attributes which take up a lot of room
        text = re.sub(r'android:(text|title|summary|description)="[^"]*"', '', text)
        lines = [line for line in text.splitlines() if line.strip()]
        return "\n".join(lines)
        
    return text

def main():
    output_file = "context.txt"
    total_files = 0
    
    with open(output_file, "w", encoding="utf-8") as out:
        for root, dirs, files in os.walk("."):
            dirs[:] = [d for d in dirs if d not in IGNORE_FOLDERS and not d.startswith('.')]
            
            for file in files:
                if file.endswith(EXTENSIONS):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()
                        
                        ext = os.path.splitext(file)[1]
                        skeleton_content = extract_skeleton(content, ext)
                        
                        if skeleton_content.strip():
                            out.write(f'<file path="{file_path}">\n')
                            out.write(skeleton_content + "\n")
                            out.write("</file>\n\n")
                            total_files += 1
                    except Exception as e:
                        pass
                        
    print(f"Done! Structural skeleton generated for {total_files} files into {output_file}.")

if __name__ == "__main__":
    main()
