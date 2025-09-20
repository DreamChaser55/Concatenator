import os
import sys
import locale
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

try:
    from natsort import natsorted
except ImportError:
    raise ImportError("The 'natsort' library is required for natural sorting. Install it with: pip install natsort")

# Allowed plaintext file types (extensions must be lowercase and include the dot)
ALLOWED_EXTS = {
    '.txt', '.md', '.markdown', '.rst', '.html', '.htm', '.xml', '.csv', '.tsv',
    '.ini', '.cfg', '.conf', '.properties', '.env',
    '.json', '.yaml', '.yml', '.toml',
    '.py', '.js', '.jsx', '.ts', '.tsx',
    '.java', '.c', '.cpp', '.h', '.hpp', '.cs', '.go', '.rb', '.php', '.swift', '.kt',
    '.sh', '.bash', '.zsh', '.fish', '.ps1', '.bat',
    '.sql', '.pl', '.lua', '.r', '.scala', '.clj', '.groovy', '.dart',
    '.css', '.scss', '.less'
}
# Special file names that should be treated as text even without an extension
ALLOWED_NAMES = {
    'license', 'makefile', 'dockerfile',
    '.editorconfig', '.gitattributes', '.gitignore', '.dockerignore'
}

def is_allowed(path):
    """Return True if the file path has an allowed extension or is an allowed special name."""
    name = os.path.basename(path)
    lower_name = name.lower()
    if lower_name in ALLOWED_NAMES:
        return True
    _, ext = os.path.splitext(lower_name)
    return ext in ALLOWED_EXTS

def concatenate_text_files(folder_path, output_path='concatenated.txt'):
    """
    Concatenates all text files in the given folder into a single text file,
    prepending each file's content with its filename. Files are sorted in natural order.
    
    Args:
        folder_path (str): Path to the folder containing text files.
        output_path (str): Path to the output file (default: 'concatenated.txt' in the current directory).
    """
    # Validate that the folder exists
    if not os.path.isdir(folder_path):
        raise ValueError(f"Folder does not exist or is not a directory: {folder_path}")
    
    # Get the list of allowed plain-text files and sort them naturally
    files = [f for f in os.listdir(folder_path) if is_allowed(f) and os.path.isfile(os.path.join(folder_path, f))]
    files = natsorted(files)
    
    # Convert to full paths
    file_paths = [os.path.join(folder_path, f) for f in files]
    
    # Use the common concatenation function
    concatenate_file_list(file_paths, output_path)

def concatenate_file_list(file_paths, output_path='concatenated.txt'):
    """
    Concatenates a list of files into a single text file.
    
    Args:
        file_paths (list): List of file paths to concatenate.
        output_path (str): Path to the output file.
    """
    if not file_paths:
        raise ValueError("No files to concatenate.")
    
    output_content = []
    
    # Iterate over files
    for file_path in file_paths:
        filename = os.path.basename(file_path)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            # Prepend filename and append text with separators for clarity
            output_content.append(f"--- File: {filename} ---\n\n")
            output_content.append(text)
            output_content.append("\n\n")
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            # Continue to next file instead of crashing
    
    # Save the concatenated content to the output file
    try:
        with open(output_path, 'w', encoding='utf-8') as out:
            out.write(''.join(output_content))
        print(f"Concatenated file saved to: {output_path}")
    except Exception as e:
        raise IOError(f"Error writing to {output_path}: {e}")

# GUI Implementation
class TextFileConcatenatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Text File Concatenator")
        self.root.geometry("600x500")
        
        self.selected_files = []
        
        self.setup_ui()
        
    def setup_ui(self):
        # Mode selection
        mode_frame = ttk.Frame(self.root, padding="10")
        mode_frame.pack(fill=tk.X)
        
        ttk.Label(mode_frame, text="Select Mode:").pack(anchor=tk.W)
        
        self.mode_var = tk.StringVar(value="folder")
        ttk.Radiobutton(mode_frame, text="All files in folder", 
                       variable=self.mode_var, value="folder",
                       command=self.on_mode_change).pack(anchor=tk.W)
        ttk.Radiobutton(mode_frame, text="Select specific files", 
                       variable=self.mode_var, value="files",
                       command=self.on_mode_change).pack(anchor=tk.W)
        
        # Separator
        ttk.Separator(self.root, orient='horizontal').pack(fill=tk.X, pady=5)
        
        # Folder selection frame (for folder mode)
        self.folder_frame = ttk.Frame(self.root, padding="10")
        self.folder_frame.pack(fill=tk.X)
        
        ttk.Label(self.folder_frame, text="Folder Path:").pack(anchor=tk.W)
        folder_entry_frame = ttk.Frame(self.folder_frame)
        folder_entry_frame.pack(fill=tk.X, pady=5)
        self.folder_entry = ttk.Entry(folder_entry_frame, width=50)
        self.folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(folder_entry_frame, text="Browse", 
                  command=self.browse_folder).pack(side=tk.LEFT, padx=(5, 0))
        
        # File selection frame (for files mode)
        self.files_frame = ttk.Frame(self.root, padding="10")
        
        # File list controls
        list_controls = ttk.Frame(self.files_frame)
        list_controls.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Button(list_controls, text="Add Files", 
                  command=self.add_files).pack(side=tk.LEFT, padx=2)
        ttk.Button(list_controls, text="Add From List...", 
                  command=self.add_files_from_list).pack(side=tk.LEFT, padx=2)
        ttk.Button(list_controls, text="Remove Selected", 
                  command=self.remove_selected).pack(side=tk.LEFT, padx=2)
        ttk.Button(list_controls, text="Clear All", 
                  command=self.clear_all).pack(side=tk.LEFT, padx=2)
        ttk.Button(list_controls, text="Move Up", 
                  command=self.move_up).pack(side=tk.LEFT, padx=2)
        ttk.Button(list_controls, text="Move Down", 
                  command=self.move_down).pack(side=tk.LEFT, padx=2)
        ttk.Button(list_controls, text="Sort", 
                  command=self.sort_files).pack(side=tk.LEFT, padx=2)
        
        # File listbox with scrollbar
        list_frame = ttk.Frame(self.files_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.file_listbox = tk.Listbox(list_frame, 
                                       yscrollcommand=scrollbar.set,
                                       selectmode=tk.EXTENDED,
                                       height=10,
                                       activestyle='none')
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.file_listbox.yview)
        
        # Output file section
        output_frame = ttk.Frame(self.root, padding="10")
        output_frame.pack(fill=tk.X)
        
        ttk.Label(output_frame, text="Output File:").pack(anchor=tk.W)
        self.output_entry = ttk.Entry(output_frame, width=50)
        self.output_entry.insert(0, 'concatenated.txt')
        self.output_entry.pack(fill=tk.X, pady=5)
        
        # Concatenate button
        ttk.Button(self.root, text="Concatenate Files", 
                  command=self.run_concatenation,
                  style='Accent.TButton').pack(pady=10)
        
        # Status label
        self.status_label = ttk.Label(self.root, text="", foreground="gray")
        self.status_label.pack(pady=5)
        
        # Initialize view based on default mode
        self.on_mode_change()
    
    def on_mode_change(self):
        """Handle mode change between folder and files selection."""
        if self.mode_var.get() == "folder":
            # Switching to Folder Mode
            # Clear the file selection data
            self.file_listbox.delete(0, tk.END)
            self.selected_files = []
            
            # Hide the file selection frame
            self.files_frame.pack_forget()
            
            # Hide the status label (not needed in folder mode)
            self.status_label.pack_forget()
            
            # Show the folder selection frame
            self.folder_frame.pack(fill=tk.X, after=self.root.children['!separator'])
        else:
            # Switching to File Selection Mode
            # Hide the folder frame
            self.folder_frame.pack_forget()
            
            # Show the file selection frame
            self.files_frame.pack(fill=tk.BOTH, expand=True, after=self.root.children['!separator'])
            
            # Show and update the status label
            self.status_label.pack(pady=5)
            self.update_file_count()
    
    def browse_folder(self):
        """Browse and select a folder."""
        folder = filedialog.askdirectory()
        if folder:
            self.folder_entry.delete(0, tk.END)
            self.folder_entry.insert(0, folder)
    
    def add_files(self):
        """Add files to the selection list."""
        # Build a file dialog filter pattern from allowed extensions (special names aren't represented here)
        patterns = " ".join(f"*{ext}" for ext in sorted(ALLOWED_EXTS))
        files = filedialog.askopenfilenames(
            title="Select files",
            filetypes=[("Allowed text files", patterns), ("All files", "*.*")]
        )
        
        skipped = 0
        for file_path in files:
            if not is_allowed(file_path):
                skipped += 1
                continue
            if file_path not in self.selected_files:
                self.selected_files.append(file_path)
                # Display full path in the listbox
                self.file_listbox.insert(tk.END, file_path)
        
        self.update_file_count()
        if skipped:
            messagebox.showinfo("Some files skipped", f"Skipped {skipped} file(s) not in allowed types.")
    
    def add_files_from_list(self):
        """Add files from a list file containing full paths."""
        list_path = filedialog.askopenfilename(
            title="Select list file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if not list_path:
            return

        result = self.parse_file_list(list_path)

        # Apply additions to UI/state
        for p in result["added_paths"]:
            self.selected_files.append(p)
            self.file_listbox.insert(tk.END, p)

        self.update_file_count()

        # Build summary message
        added = len(result["added_paths"])
        already = len(result["already_present"])
        not_found = len(result["not_found"])
        skipped_not_allowed = len(result["skipped_not_allowed"])

        summary = (
            f"Added: {added}\n"
            f"Already present: {already}\n"
            f"Not found: {not_found}\n"
            f"Skipped (not allowed type): {skipped_not_allowed}"
        )

        # Show some details for small error lists
        details_lines = []
        for label, items in (
            ("Not found", result["not_found"]),
            ("Skipped (not allowed type)", result["skipped_not_allowed"]),
        ):
            if items:
                preview = items[:5]
                more = len(items) - len(preview)
                details_lines.append(label + " examples:\n  - " + "\n  - ".join(preview))
                if more > 0:
                    details_lines.append(f"  ... and {more} more")
        details = "\n\n".join(details_lines)
        if details:
            summary = summary + "\n\n" + details

        messagebox.showinfo("Import summary", summary)

    def parse_file_list(self, list_path):
        """
        Parse a text file containing file paths (one per line).
        Supports comments (#, ;) and blank lines. Relative paths are resolved
        relative to the list file's directory. Environment variables and user
        (~) are expanded. Only allowed plain-text types are accepted.
        Returns a dict with added_paths, already_present, not_found, skipped_not_allowed.
        """
        # Build a set of normalized existing selections for fast duplicate checks
        def norm(p):
            return os.path.normcase(os.path.normpath(os.path.abspath(p)))

        existing = {norm(p) for p in self.selected_files}
        base_dir = os.path.dirname(list_path)

        lines = []
        # Try UTF-8 with BOM first, then fall back to preferred encoding
        preferred = locale.getpreferredencoding(False) or "cp1252"
        encodings = ["utf-8-sig", preferred, "cp1252", "latin-1"]
        last_err = None
        for enc in encodings:
            try:
                with open(list_path, "r", encoding=enc) as f:
                    lines = f.readlines()
                last_err = None
                break
            except UnicodeDecodeError as e:
                last_err = e
                continue
            except Exception:
                # Other errors (e.g., file access) — rethrow
                raise

        if last_err is not None and not lines:
            # If still failing due to decode, surface a clear error
            messagebox.showerror("Error", f"Could not decode list file using common encodings. Last error: {last_err}")
            return {"added_paths": [], "already_present": [], "not_found": [], "skipped_not_allowed": []}

        added_paths = []
        already_present = []
        not_found = []
        skipped_not_allowed = []

        for raw in lines:
            line = raw.strip()
            if not line:
                continue
            if line.startswith("#") or line.startswith(";"):
                continue

            # Strip surrounding quotes if present
            if (line.startswith('"') and line.endswith('"')) or (line.startswith("'") and line.endswith("'")):
                line = line[1:-1]

            # Expand env vars and ~
            line = os.path.expandvars(os.path.expanduser(line))

            # If relative, resolve relative to list file's directory
            if not os.path.isabs(line):
                candidate = os.path.join(base_dir, line)
            else:
                candidate = line

            candidate = os.path.abspath(os.path.normpath(candidate))

            # Filter to allowed file types only (by extension or special name)
            if not is_allowed(candidate):
                skipped_not_allowed.append(line)
                continue

            # Existence check
            if not os.path.isfile(candidate):
                not_found.append(line)
                continue

            n = norm(candidate)
            if n in existing or any(norm(p) == n for p in added_paths):
                already_present.append(candidate)
                continue

            added_paths.append(candidate)

        return {
            "added_paths": added_paths,
            "already_present": already_present,
            "not_found": not_found,
            "skipped_not_allowed": skipped_not_allowed,
        }

    def remove_selected(self):
        """Remove selected files from the list."""
        selected_indices = list(self.file_listbox.curselection())
        # Remove in reverse order to maintain correct indices
        for index in reversed(selected_indices):
            self.file_listbox.delete(index)
            del self.selected_files[index]
        
        self.update_file_count()
    
    def clear_all(self):
        """Clear all files from the list."""
        self.file_listbox.delete(0, tk.END)
        self.selected_files = []
        self.update_file_count()
    
    def move_up(self):
        """Move selected file(s) up in the list."""
        selected_indices = list(self.file_listbox.curselection())
        if not selected_indices or selected_indices[0] == 0:
            return
        
        for index in selected_indices:
            # Swap with previous item
            self.selected_files[index], self.selected_files[index-1] = \
                self.selected_files[index-1], self.selected_files[index]
            
            # Update listbox
            item = self.file_listbox.get(index)
            self.file_listbox.delete(index)
            self.file_listbox.insert(index-1, item)
            
            # Update selection
            self.file_listbox.selection_clear(index)
            self.file_listbox.selection_set(index-1)
    
    def move_down(self):
        """Move selected file(s) down in the list."""
        selected_indices = list(self.file_listbox.curselection())
        if not selected_indices or selected_indices[-1] == len(self.selected_files) - 1:
            return
        
        for index in reversed(selected_indices):
            # Swap with next item
            self.selected_files[index], self.selected_files[index+1] = \
                self.selected_files[index+1], self.selected_files[index]
            
            # Update listbox
            item = self.file_listbox.get(index)
            self.file_listbox.delete(index)
            self.file_listbox.insert(index+1, item)
            
            # Update selection
            self.file_listbox.selection_clear(index)
            self.file_listbox.selection_set(index+1)
    
    def sort_files(self):
        """Sort files in the list using natural ordering."""
        if not self.selected_files:
            return
        
        # Sort the files list using natural sorting
        self.selected_files = natsorted(self.selected_files)
        
        # Clear and repopulate the listbox with sorted items
        self.file_listbox.delete(0, tk.END)
        for file_path in self.selected_files:
            self.file_listbox.insert(tk.END, file_path)
        
        # Clear all selections as requested
        self.file_listbox.selection_clear(0, tk.END)
    
    def update_file_count(self):
        """Update the status label with file count."""
        count = len(self.selected_files)
        if count == 0:
            self.status_label.config(text="No files selected")
        elif count == 1:
            self.status_label.config(text="1 file selected")
        else:
            self.status_label.config(text=f"{count} files selected")
    
    def run_concatenation(self):
        """Run the concatenation based on the selected mode."""
        output_path = self.output_entry.get() or 'concatenated.txt'
        
        try:
            if self.mode_var.get() == "folder":
                folder_path = self.folder_entry.get()
                if not folder_path:
                    messagebox.showerror("Error", "Please select a folder.")
                    return
                concatenate_text_files(folder_path, output_path)
            else:
                if not self.selected_files:
                    messagebox.showerror("Error", "Please select files to concatenate.")
                    return
                concatenate_file_list(self.selected_files, output_path)
            
            messagebox.showinfo("Success", f"Files concatenated successfully to:\n{output_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

def create_gui():
    root = tk.Tk()
    app = TextFileConcatenatorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # If arguments are provided, run in CLI mode
        folder_path = sys.argv[1]
        output_path = sys.argv[2] if len(sys.argv) > 2 else 'concatenated.txt'
        
        try:
            concatenate_text_files(folder_path, output_path)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    else:
        # No arguments: Launch GUI
        create_gui()
