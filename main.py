import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class PythonLearningApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Learning App")
        self.root.geometry("800x600")

        # Load data
        self.lessons = self.load_lessons()
        self.quizzes = self.load_quizzes()
        self.progress = self.load_progress()

        # Create notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Lessons tab
        self.lessons_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.lessons_frame, text="Lessons")
        self.create_lessons_tab()

        # Quizzes tab
        self.quizzes_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.quizzes_frame, text="Quizzes")
        self.create_quizzes_tab()

        # Examples tab
        self.examples_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.examples_frame, text="Examples")
        self.create_examples_tab()

        # Progress tab
        self.progress_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.progress_frame, text="Progress")
        self.create_progress_tab()

    def load_lessons(self):
        # Load lessons from json
        try:
            with open("data/lessons/lessons.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def load_quizzes(self):
        # Load quizzes from json
        try:
            with open("data/quizzes/quizzes.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def load_progress(self):
        # Load from file
        if os.path.exists("data/progress/progress.json"):
            with open("data/progress/progress.json", "r") as f:
                return json.load(f)
        return {}

    def save_progress(self):
        os.makedirs("data/progress", exist_ok=True)
        with open("data/progress/progress.json", "w") as f:
            json.dump(self.progress, f)

    def create_lessons_tab(self):
        # Listbox for lessons
        self.lessons_list = tk.Listbox(self.lessons_frame)
        for lid, lesson in self.lessons.items():
            self.lessons_list.insert(tk.END, lesson["title"])
        self.lessons_list.pack(side=tk.LEFT, fill=tk.Y)
        self.lessons_list.bind("<<ListboxSelect>>", self.show_lesson)

        # Text area for content
        self.lesson_text = tk.Text(self.lessons_frame, wrap=tk.WORD)
        self.lesson_text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def show_lesson(self, event):
        selection = self.lessons_list.curselection()
        if selection:
            idx = selection[0]
            lid = list(self.lessons.keys())[idx]
            content = self.lessons[lid]["content"]
            self.lesson_text.delete(1.0, tk.END)
            self.lesson_text.insert(tk.END, content)
            self.progress[lid] = True
            self.save_progress()

    def create_quizzes_tab(self):
        # Similar to lessons
        self.quiz_list = tk.Listbox(self.quizzes_frame)
        for qid, quiz in self.quizzes.items():
            self.quiz_list.insert(tk.END, quiz["question"])
        self.quiz_list.pack(side=tk.LEFT, fill=tk.Y)
        self.quiz_list.bind("<<ListboxSelect>>", self.show_quiz)

        self.quiz_frame = ttk.Frame(self.quizzes_frame)
        self.quiz_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def show_quiz(self, event):
        selection = self.quiz_list.curselection()
        if selection:
            idx = selection[0]
            qid = list(self.quizzes.keys())[idx]
            quiz = self.quizzes[qid]
            # Clear previous
            for widget in self.quiz_frame.winfo_children():
                widget.destroy()
            tk.Label(self.quiz_frame, text=quiz["question"]).pack()
            self.var = tk.IntVar()
            for i, opt in enumerate(quiz["options"]):
                tk.Radiobutton(self.quiz_frame, text=opt, variable=self.var, value=i).pack()
            tk.Button(self.quiz_frame, text="Submit", command=lambda: self.check_answer(qid)).pack()

    def check_answer(self, qid):
        if self.var.get() == self.quizzes[qid]["answer"]:
            messagebox.showinfo("Correct!", "Well done!")
        else:
            messagebox.showerror("Wrong", "Try again.")

    def show_example(self, event):
        selection = self.examples_list.curselection()
        if selection:
            idx = selection[0]
            eid = list(self.examples.keys())[idx]
            code = self.examples[eid]["code"]
            self.example_text.delete(1.0, tk.END)
            self.example_text.insert(tk.END, code)

    def run_example(self):
        code = self.example_text.get(1.0, tk.END).strip()
        if code:
            try:
                exec(code)
                messagebox.showinfo("Output", "Code executed successfully. Check console for output.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def create_examples_tab(self):
        # Load examples
        try:
            with open("data/examples/examples.json", "r") as f:
                self.examples = json.load(f)
        except FileNotFoundError:
            self.examples = {}

        self.examples_list = tk.Listbox(self.examples_frame)
        for eid, ex in self.examples.items():
            self.examples_list.insert(tk.END, ex["title"])
        self.examples_list.pack(side=tk.LEFT, fill=tk.Y)
        self.examples_list.bind("<<ListboxSelect>>", self.show_example)

        self.example_text = tk.Text(self.examples_frame, wrap=tk.WORD)
        self.example_text.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        tk.Button(self.examples_frame, text="Run Code", command=self.run_example).pack(side=tk.BOTTOM)

    def create_progress_tab(self):
        tk.Label(self.progress_frame, text="Progress tracking.").pack()
        # Show completed lessons
        for lid, completed in self.progress.items():
            if completed:
                tk.Label(self.progress_frame, text=f"Lesson {lid}: Completed").pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = PythonLearningApp(root)
    root.mainloop()