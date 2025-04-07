import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PyPDF2  # For PDF handling
# from your_llm_module import LLM  # Import your LLM class/functions.  Replace this.
import io
import os

class FinancialAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Financial Statement Analyzer")
        self.root.geometry("800x600")  # Increased size for better layout
        self.root.resizable(True, True) #Make it resizable

        self.create_widgets()
        self.llm = None # Placeholder for LLM instance

    def create_widgets(self):
        # Main Frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # File Upload Section
        file_frame = ttk.Frame(self.main_frame)
        file_frame.pack(fill=tk.X, pady=10)

        ttk.Label(file_frame, text="Financial Document:").pack(side=tk.LEFT, padx=5)
        self.file_path_label = ttk.Label(file_frame, text="No file selected")
        self.file_path_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.upload_button = ttk.Button(file_frame, text="Browse", command=self.upload_file)
        self.upload_button.pack(side=tk.RIGHT)

        ttk.Label(file_frame, text="Projected Story (Optional):").pack(side=tk.LEFT, padx=5)
        self.story_path_label = ttk.Label(file_frame, text="No file selected")
        self.story_path_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.upload_story_button = ttk.Button(file_frame, text="Browse", command=self.upload_story_file)
        self.upload_story_button.pack(side=tk.RIGHT)

        # Analysis and Output Section
        output_frame = ttk.Frame(self.main_frame)
        output_frame.pack(fill=tk.BOTH, expand=True)

        self.analyze_button = ttk.Button(output_frame, text="Analyze", command=self.analyze_data)
        self.analyze_button.pack(pady=10)

        self.notebook = ttk.Notebook(output_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Summary Tab
        self.summary_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.summary_tab, text="Summary")
        self.summary_text = tk.Text(self.summary_tab, height=10, width=80, wrap=tk.WORD)
        self.summary_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.summary_text.config(state=tk.DISABLED)  # Make it read-only

        # Comparison Tab
        self.comparison_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.comparison_tab, text="Comparison")
        self.comparison_text = tk.Text(self.comparison_tab, height=10, width=80, wrap=tk.WORD)
        self.comparison_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.comparison_text.config(state=tk.DISABLED)

        # Visualization Tab
        self.visualization_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.visualization_tab, text="Visualization")
        self.fig, self.ax = plt.subplots(figsize=(6, 4))  # Set figure size
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.visualization_tab)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.ax.tick_params(axis='x', labelsize=8)  # Adjust tick label size

        # Q&A Tab
        self.q_and_a_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.q_and_a_tab, text="Q & A")
        question_frame = ttk.Frame(self.q_and_a_tab)
        question_frame.pack(pady=10, padx=10, fill=tk.X)
        ttk.Label(question_frame, text="Ask a Question:").pack(side=tk.LEFT, padx=5)
        self.question_entry = ttk.Entry(question_frame, width=50)
        self.question_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.answer_button = ttk.Button(question_frame, text="Get Answer", command=self.get_answer)
        self.answer_button.pack(side=tk.RIGHT)
        self.answer_text = tk.Text(self.q_and_a_tab, height=5, width=80, wrap=tk.WORD)
        self.answer_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.answer_text.config(state=tk.DISABLED)

        # Education Tab
        self.education_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.education_tab, text="Education")
        self.education_text = tk.Text(self.education_tab, height=10, width=80, wrap=tk.WORD)
        self.education_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.education_text.config(state=tk.DISABLED)

        # Status Bar
        self.status_label = ttk.Label(self.main_frame, text="Ready", anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Initialize LLM (Replace with your actual LLM initialization)
        # try:
        #     self.llm = LLM()  # Replace LLM with the actual name of your LLM class/instance
        #     self.status_label.config(text="LLM Initialized")
        # except Exception as e:
        #     messagebox.showerror("LLM Error", f"Failed to initialize LLM: {e}")
        #     self.status_label.config(text="LLM Initialization Failed")

    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            self.file_path_label.config(text=os.path.basename(file_path))
            self.financial_data_path = file_path
            self.status_label.config(text=f"File selected: {os.path.basename(file_path)}")

    def upload_story_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("PDF Files", "*.pdf")])
        if file_path:
            self.story_path_label.config(text=os.path.basename(file_path))
            self.story_data_path = file_path
            self.status_label.config(text=f"Story file selected: {os.path.basename(file_path)}")

    def analyze_data(self):
        if not hasattr(self, 'financial_data_path'):
            messagebox.showerror("Error", "Please upload a financial document first.")
            self.status_label.config(text="Error: No financial document uploaded")
            return

        self.status_label.config(text="Analyzing data...")
        self.root.update_idletasks()  # Force GUI update

        try:
            # 1. Extract data from the financial document
            financial_text = self.extract_text_from_file(self.financial_data_path)
            if not financial_text:
                raise ValueError("No text extracted from financial document.")

            # 2. Extract text from the story file, if provided
            story_text = ""
            if hasattr(self, 'story_data_path'):
                story_text = self.extract_text_from_file(self.story_data_path)

            # 3. Process the data with the LLM (Replace with your actual LLM call)
            # if self.llm:
            #     summary, comparison = self.llm.analyze_financial_data(financial_text, story_text)
            # else:
            #     raise ValueError("LLM is not initialized.")
            # Placeholder LLM output:
            summary = "Placeholder summary: Analysis of the financial data."
            comparison = "Placeholder comparison: Comparison between financial data and provided story."

            # 4. Generate a placeholder visualization
            visualization_data = {'Metric1': [10, 20, 15, 25], 'Metric2': [5, 10, 8, 12], 'Year': [2020, 2021, 2022, 2023]}
            # 5. Update the GUI with the results
            self.update_summary(summary)
            self.update_comparison(comparison)
            self.update_visualization(visualization_data)

            # 6. Enable the question and answer section after successful analysis
            self.question_entry.config(state=tk.NORMAL)
            self.answer_button.config(state=tk.NORMAL)
            self.update_education("Here's a basic explanation of a financial ratio...")
            self.status_label.config(text="Analysis complete.")

        except Exception as e:
            messagebox.showerror("Analysis Error", f"An error occurred during analysis: {e}")
            self.status_label.config(text=f"Error: {e}")

    def extract_text_from_file(self, file_path):
        """Extracts text from a PDF or TXT file."""
        try:
            if file_path.lower().endswith(".pdf"):
                with open(file_path, "rb") as file:
                    reader = PyPDF2.PdfReader(file)
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text() or ""  # Handle None
                    return text
            elif file_path.lower().endswith(".txt"):
                with open(file_path, "r", encoding="utf-8") as file:
                    return file.read()
            else:
                raise ValueError(f"Unsupported file type: {file_path}")
        except Exception as e:
            messagebox.showerror("File Error", f"Error reading file: {e}")
            self.status_label.config(text=f"Error reading file")
            return ""  # Important: Return empty string on error to avoid further errors

    def update_summary(self, summary):
        self.summary_text.config(state=tk.NORMAL)  # Make it editable
        self.summary_text.delete("1.0", tk.END)
        self.summary_text.insert(tk.END, summary)
        self.summary_text.config(state=tk.DISABLED)  # Make it read-only

    def update_comparison(self, comparison):
        self.comparison_text.config(state=tk.NORMAL)
        self.comparison_text.delete("1.0", tk.END)
        self.comparison_text.insert(tk.END, comparison)
        self.comparison_text.config(state=tk.DISABLED)

    def update_visualization(self, data):
        self.ax.clear()
        if data:  # Check if data is not None or empty
            if len(data.keys()) == 3:
                # Example: Create a bar chart with two metrics over years
                self.ax.bar(data['Year'], data['Metric1'], label='Metric1', width=0.4)
                self.ax.bar([x + 0.4 for x in data['Year']], data['Metric2'], label='Metric2', width=0.4)
                self.ax.set_xlabel('Year')
                self.ax.set_ylabel('Value')
                self.ax.set_title('Financial Metrics Over Time')
                self.ax.legend()
                self.ax.tick_params(axis='x', labelsize=8)
            elif len(data.keys()) == 2:
                 # Example: Create a pie chart
                labels = list(data.keys())
                sizes = list(data.values())
                self.ax.pie(sizes, labels=labels, autopct='%1.1f%%')
                self.ax.set_title('Data Distribution')
            else:
                self.ax.text(0.5, 0.5, "Unsupported data format for plotting", ha='center', va='center')

        else:
             self.ax.text(0.5, 0.5, "No data to display", ha='center', va='center')
        self.canvas.draw()

    def get_answer(self):
        question = self.question_entry.get()
        if not question:
            messagebox.showwarning("Warning", "Please enter a question.")
            return
        self.answer_text.config(state=tk.NORMAL)
        self.answer_text.delete("1.0", tk.END)
        # if self.llm:
        #     answer = self.llm.get_answer(question) #  Get answer from LLM
        # else:
        #     answer = "LLM not available."
        answer = "Placeholder answer from the LLM: " + question
        self.answer_text.insert(tk.END, answer)
        self.answer_text.config(state=tk.DISABLED)

    def update_education(self, text):
        self.education_text.config(state=tk.NORMAL)
        self.education_text.delete("1.0", tk.END)
        self.education_text.insert(tk.END, text)
        self.education_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = FinancialAnalysisApp(root)
    root.mainloop()

