import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import os
import sys
from main import summarize_textrank
import re

class TextSummarizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Summarizer")
        self.root.geometry("800x600")
        self.root.minsize(600, 500)
        
        # Theme and font settings
        self.theme_mode = tk.StringVar(value="light")
        self.font_size = tk.IntVar(value=11)
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Arial', 10))
        self.style.configure('TLabel', font=('Arial', 11))
        
        # Word count variables
        self.input_word_count = tk.StringVar(value="Words: 0")
        self.output_word_count = tk.StringVar(value="Words: 0")
        self.compression_ratio = tk.StringVar(value="Compression: 0%")
        
        self.create_widgets()
        self.apply_theme("light")
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Settings bar
        settings_frame = ttk.Frame(main_frame)
        settings_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Theme selection
        theme_frame = ttk.Frame(settings_frame)
        theme_frame.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(theme_frame, text="Theme:").pack(side=tk.LEFT)
        theme_combo = ttk.Combobox(theme_frame, values=["Light", "Dark"], 
                                  width=6, state="readonly", textvariable=self.theme_mode)
        theme_combo.pack(side=tk.LEFT, padx=5)
        theme_combo.bind("<<ComboboxSelected>>", lambda e: self.apply_theme(self.theme_mode.get().lower()))
        
        # Font size
        font_frame = ttk.Frame(settings_frame)
        font_frame.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(font_frame, text="Font Size:").pack(side=tk.LEFT)
        font_spin = ttk.Spinbox(font_frame, from_=8, to=24, width=3, 
                               textvariable=self.font_size, command=self.update_font_size)
        font_spin.pack(side=tk.LEFT, padx=5)
        
        # Created by section
        created_by_frame = ttk.Frame(settings_frame)
        created_by_frame.pack(side=tk.RIGHT, padx=5)
        ttk.Label(created_by_frame, text="Created by: SURYA, MONISHKA, DIYA", 
                 font=("Arial", 9, "italic")).pack(side=tk.RIGHT)
        
        # Title
        title_label = ttk.Label(main_frame, text="Text Summarizer", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Input section
        input_frame = ttk.LabelFrame(main_frame, text="Input Text", padding="10")
        input_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.input_text = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, height=10, 
                                                  font=("Arial", self.font_size.get()))
        self.input_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.input_text.bind("<<Modified>>", self.update_input_stats)
        
        # Input stats
        input_stats_frame = ttk.Frame(input_frame)
        input_stats_frame.pack(fill=tk.X, padx=5)
        ttk.Label(input_stats_frame, textvariable=self.input_word_count).pack(side=tk.LEFT)
        
        # Control section
        control_frame = ttk.Frame(main_frame, padding="5")
        control_frame.pack(fill=tk.X, expand=False, padx=5, pady=5)
        
        # Number of sentences to include
        sentences_frame = ttk.Frame(control_frame)
        sentences_frame.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(sentences_frame, text="Number of sentences:").pack(side=tk.LEFT)
        self.sentences_var = tk.StringVar(value="2")
        sentences_spin = ttk.Spinbox(sentences_frame, from_=1, to=10, width=3, 
                                     textvariable=self.sentences_var)
        sentences_spin.pack(side=tk.LEFT, padx=5)
        
        # Buttons
        buttons_frame = ttk.Frame(control_frame)
        buttons_frame.pack(side=tk.RIGHT, padx=5)
        
        self.load_btn = ttk.Button(buttons_frame, text="Load File", command=self.load_file)
        self.load_btn.pack(side=tk.LEFT, padx=5)
        
        self.summarize_btn = ttk.Button(buttons_frame, text="Summarize", command=self.summarize)
        self.summarize_btn.pack(side=tk.LEFT, padx=5)
        
        self.save_btn = ttk.Button(buttons_frame, text="Save Summary", command=self.save_summary)
        self.save_btn.pack(side=tk.LEFT, padx=5)
        
        # Output section
        output_frame = ttk.LabelFrame(main_frame, text="Summary Output", padding="10")
        output_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, height=8, 
                                                   font=("Arial", self.font_size.get()))
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Output stats
        output_stats_frame = ttk.Frame(output_frame)
        output_stats_frame.pack(fill=tk.X, padx=5)
        ttk.Label(output_stats_frame, textvariable=self.output_word_count).pack(side=tk.LEFT)
        ttk.Label(output_stats_frame, textvariable=self.compression_ratio).pack(side=tk.LEFT, padx=15)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, padx=5, pady=5)
    
    def apply_theme(self, theme_name):
        if theme_name == "dark":
            self.root.configure(bg="#2d2d30")
            text_bg = "#1e1e1e"
            text_fg = "#e0e0e0"
            frame_bg = "#2d2d30"
            self.style.configure('TFrame', background=frame_bg)
            self.style.configure('TLabelframe', background=frame_bg)
            self.style.configure('TLabelframe.Label', background=frame_bg, foreground=text_fg)
            self.style.configure('TLabel', background=frame_bg, foreground=text_fg)
            self.style.configure('TButton', background=frame_bg)
            self.input_text.config(bg=text_bg, fg=text_fg, insertbackground=text_fg)
            self.output_text.config(bg=text_bg, fg=text_fg, insertbackground=text_fg)
        else:  # light
            self.root.configure(bg="#f0f0f0")
            text_bg = "white"
            text_fg = "black"
            frame_bg = "#f0f0f0"
            self.style.configure('TFrame', background=frame_bg)
            self.style.configure('TLabelframe', background=frame_bg)
            self.style.configure('TLabelframe.Label', background=frame_bg, foreground=text_fg)
            self.style.configure('TLabel', background=frame_bg, foreground=text_fg)
            self.style.configure('TButton', background=frame_bg)
            self.input_text.config(bg=text_bg, fg=text_fg, insertbackground=text_fg)
            self.output_text.config(bg=text_bg, fg=text_fg, insertbackground=text_fg)
    
    def update_font_size(self):
        size = self.font_size.get()
        self.input_text.config(font=("Arial", size))
        self.output_text.config(font=("Arial", size))
    
    def update_input_stats(self, event=None):
        if self.input_text:
            text = self.input_text.get(1.0, tk.END).strip()
            word_count = len(re.findall(r'\b\w+\b', text))
            self.input_word_count.set(f"Words: {word_count}")
            self.input_text.edit_modified(False)  # Reset the modified flag
        
    def update_output_stats(self):
        input_text = self.input_text.get(1.0, tk.END).strip()
        output_text = self.output_text.get(1.0, tk.END).strip()
        
        input_word_count = len(re.findall(r'\b\w+\b', input_text))
        output_word_count = len(re.findall(r'\b\w+\b', output_text))
        
        self.output_word_count.set(f"Words: {output_word_count}")
        
        if input_word_count > 0:
            compression = ((input_word_count - output_word_count) / input_word_count) * 100
            self.compression_ratio.set(f"Compression: {compression:.1f}%")
        else:
            self.compression_ratio.set("Compression: 0%")
    
    def load_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Text File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                    self.input_text.delete(1.0, tk.END)
                    self.input_text.insert(tk.END, content)
                    self.update_input_stats()
                    self.status_var.set(f"Loaded file: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")
    
    def summarize(self):
        text = self.input_text.get(1.0, tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "Please enter some text to summarize.")
            return
        
        try:
            num_sentences = int(self.sentences_var.get())
            if num_sentences < 1:
                num_sentences = 1
                
            self.status_var.set("Summarizing...")
            self.root.update_idletasks()
            
            summary = summarize_textrank(text, num_sentences=num_sentences)
            
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, summary)
            self.status_var.set(f"Summary complete. Used {num_sentences} sentences.")
            
            # Update statistics
            self.update_output_stats()
            
            # Also save to output.txt for compatibility
            with open("output.txt", "w", encoding="utf-8") as outfile:
                outfile.write(summary)
                
        except Exception as e:
            messagebox.showerror("Error", f"Summarization failed: {e}")
            self.status_var.set("Error during summarization")
    
    def save_summary(self):
        summary = self.output_text.get(1.0, tk.END).strip()
        if not summary:
            messagebox.showwarning("Warning", "No summary to save.")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Save Summary",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(summary)
                self.status_var.set(f"Summary saved to: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TextSummarizerApp(root)
    root.mainloop()