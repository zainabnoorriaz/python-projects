import tkinter as tk

# ---------------- DATA ----------------
questions = [
    ["What is the capital of Pakistan?", "Islamabad"],
    ["What is 2 + 2?", "4"],
    ["What language is used in CS50?", "Python"]
]

score = 0
current_q = 0

# ---------------- COLORS (PINK THEME) ----------------
BG = "#ffe6f0"
BTN = "#ff66b2"
BTN_HOVER = "#ff4da6"
TEXT = "#4d004d"

# ---------------- FUNCTIONS ----------------
def check_answer():
    global score, current_q

    user_answer = entry.get().strip()
    correct_answer = questions[current_q][1]

    if user_answer.lower() == correct_answer.lower():
        result_label.config(text="Correct 🎉", fg="green")
        score += 1
    else:
        result_label.config(text=f"Wrong ❌ (Ans: {correct_answer})", fg="red")

    current_q += 1
    entry.delete(0, tk.END)

    if current_q < len(questions):
        question_label.config(text=questions[current_q][0])
        score_label.config(text=f"Score: {score}")
    else:
        question_label.config(text="🎀 Quiz Finished! 🎀")
        entry.config(state="disabled")
        submit_btn.config(state="disabled")
        score_label.config(text=f"Final Score: {score}/{len(questions)}")

# ---------------- WINDOW ----------------
window = tk.Tk()
window.title("💖 Pink Quiz Game 💖")
window.geometry("450x350")
window.config(bg=BG)

# ---------------- UI ELEMENTS ----------------
title = tk.Label(
    window,
    text="💖 Quiz Game 💖",
    font=("Arial", 18, "bold"),
    bg=BG,
    fg=TEXT
)
title.pack(pady=10)

question_label = tk.Label(
    window,
    text=questions[0][0],
    font=("Arial", 12),
    bg=BG,
    fg=TEXT,
    wraplength=400
)
question_label.pack(pady=20)

entry = tk.Entry(window, font=("Arial", 12), justify="center")
entry.pack(pady=10)

submit_btn = tk.Button(
    window,
    text="Submit 💕",
    command=check_answer,
    bg=BTN,
    fg="white",
    font=("Arial", 12, "bold"),
    activebackground=BTN_HOVER,
    activeforeground="white",
    width=15
)
submit_btn.pack(pady=10)

result_label = tk.Label(window, text="", bg=BG, font=("Arial", 12))
result_label.pack(pady=10)

score_label = tk.Label(
    window,
    text="Score: 0",
    bg=BG,
    fg=TEXT,
    font=("Arial", 12, "bold")
)
score_label.pack(pady=10)

# ---------------- RUN ----------------
window.mainloop()