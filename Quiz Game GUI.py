import tkinter as tk
from tkinter import font
import time
import threading

# ── Questions ──────────────────────────────────────────────────────────────
questions = [
    {
        "question": "What is the capital of Pakistan?",
        "options": ["Lahore", "Karachi", "Islamabad", "Multan"],
        "answer": "C",
    },
    {
        "question": "What is 2 + 2?",
        "options": ["2", "4", "6", "8"],
        "answer": "B",
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Venus", "Jupiter", "Mars", "Saturn"],
        "answer": "C",
    },
    {
        "question": "How many sides does a hexagon have?",
        "options": ["5", "6", "7", "8"],
        "answer": "B",
    },
    {
        "question": "What is the largest ocean on Earth?",
        "options": ["Atlantic", "Indian", "Arctic", "Pacific"],
        "answer": "D",
    },
]

# ── Palette ─────────────────────────────────────────────────────────────────
BG        = "#1a0a2e"   # deep indigo-black
CARD      = "#2d1b4e"   # purple card
ACCENT    = "#e63946"   # vivid red
GOLD      = "#ffd166"   # warm gold
GREEN     = "#06d6a0"   # correct green
WHITE     = "#f8f9fa"
MUTED     = "#a89bc2"   # soft lavender
BTN_HOVER = "#c1121f"

LETTERS = ["A", "B", "C", "D"]


class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎯  BrainBlast Quiz")
        self.root.geometry("780x680")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)

        self.q_index = 0
        self.score = 0
        self.answered = False
        self.streak = 0

        # fonts
        self.f_title  = font.Font(family="Helvetica", size=22, weight="bold")
        self.f_body   = font.Font(family="Helvetica", size=13)
        self.f_btn    = font.Font(family="Helvetica", size=12, weight="bold")
        self.f_small  = font.Font(family="Helvetica", size=10)
        self.f_mascot = font.Font(family="Helvetica", size=48)
        self.f_badge  = font.Font(family="Helvetica", size=11, weight="bold")

        self._build_ui()
        self._load_question()

    # ── UI skeleton ──────────────────────────────────────────────────────────
    def _build_ui(self):
        # Header bar
        hdr = tk.Frame(self.root, bg=ACCENT, height=56)
        hdr.pack(fill="x")
        tk.Label(hdr, text="🎯  BrainBlast Quiz", bg=ACCENT, fg=WHITE,
                 font=self.f_title).pack(side="left", padx=18, pady=10)

        self.score_lbl = tk.Label(hdr, text="⭐ 0", bg=ACCENT, fg=GOLD,
                                  font=self.f_btn)
        self.score_lbl.pack(side="right", padx=18)

        self.streak_lbl = tk.Label(hdr, text="🔥 0", bg=ACCENT, fg=WHITE,
                                   font=self.f_badge)
        self.streak_lbl.pack(side="right", padx=4)

        # Progress bar
        prog_frame = tk.Frame(self.root, bg=BG)
        prog_frame.pack(fill="x", padx=20, pady=(14, 0))

        self.prog_lbl = tk.Label(prog_frame, text="Question 1 / 5",
                                 bg=BG, fg=MUTED, font=self.f_small)
        self.prog_lbl.pack(side="left")

        bar_bg = tk.Frame(prog_frame, bg=CARD, height=8, bd=0)
        bar_bg.pack(side="right", fill="x", expand=True, padx=(12, 0))
        self.prog_bar = tk.Frame(bar_bg, bg=GOLD, height=8)
        self.prog_bar.place(relwidth=0.0, relheight=1.0)

        # Mascot + speech bubble
        mascot_row = tk.Frame(self.root, bg=BG)
        mascot_row.pack(fill="x", padx=20, pady=(10, 0))

        self.mascot_lbl = tk.Label(mascot_row, text="🤖", bg=BG,
                                   font=self.f_mascot)
        self.mascot_lbl.pack(side="left")

        bubble_frame = tk.Frame(mascot_row, bg=CARD, bd=0,
                                highlightbackground=ACCENT,
                                highlightthickness=2)
        bubble_frame.pack(side="left", padx=(10, 0), pady=6)

        self.bubble_lbl = tk.Label(bubble_frame,
                                   text="Ready? Let's go! 🚀",
                                   bg=CARD, fg=GOLD,
                                   font=self.f_btn, wraplength=480,
                                   justify="left", padx=14, pady=8)
        self.bubble_lbl.pack()

        # Question card
        q_card = tk.Frame(self.root, bg=CARD, bd=0,
                          highlightbackground=ACCENT,
                          highlightthickness=2)
        q_card.pack(fill="x", padx=20, pady=14)

        self.q_lbl = tk.Label(q_card, text="",
                              bg=CARD, fg=WHITE,
                              font=font.Font(family="Helvetica", size=15, weight="bold"),
                              wraplength=700, justify="left",
                              padx=18, pady=18)
        self.q_lbl.pack(anchor="w")

        # Option buttons
        self.btn_frame = tk.Frame(self.root, bg=BG)
        self.btn_frame.pack(fill="x", padx=20)

        self.opt_btns = []
        self.opt_vars = []
        for i in range(4):
            row = tk.Frame(self.btn_frame, bg=BG)
            row.pack(fill="x", pady=5)

            badge = tk.Label(row, text=LETTERS[i], bg=ACCENT, fg=WHITE,
                             font=self.f_btn, width=3, pady=6)
            badge.pack(side="left")

            btn = tk.Button(row, text="", bg=CARD, fg=WHITE,
                            font=self.f_body, anchor="w",
                            activebackground=BTN_HOVER,
                            activeforeground=WHITE,
                            relief="flat", bd=0,
                            padx=14, pady=10, cursor="hand2",
                            command=lambda l=LETTERS[i]: self._answer(l))
            btn.pack(side="left", fill="x", expand=True)
            btn.bind("<Enter>", lambda e, b=btn: self._hover_on(b))
            btn.bind("<Leave>", lambda e, b=btn: self._hover_off(b))

            self.opt_btns.append((badge, btn))

        # Next button
        self.next_btn = tk.Button(self.root, text="Next  ➜",
                                  bg=ACCENT, fg=WHITE,
                                  font=self.f_btn,
                                  relief="flat", padx=28, pady=10,
                                  cursor="hand2",
                                  command=self._next_question,
                                  state="disabled")
        self.next_btn.pack(anchor="e", padx=24, pady=(14, 0))

        # Timer bar
        timer_frame = tk.Frame(self.root, bg=BG)
        timer_frame.pack(fill="x", padx=20, pady=(10, 0))
        tk.Label(timer_frame, text="⏱", bg=BG, fg=MUTED,
                 font=self.f_small).pack(side="left")
        bar_bg2 = tk.Frame(timer_frame, bg=CARD, height=6)
        bar_bg2.pack(side="left", fill="x", expand=True, padx=(6, 0))
        self.timer_bar = tk.Frame(bar_bg2, bg=GREEN, height=6)
        self.timer_bar.place(relwidth=1.0, relheight=1.0)

        self.timer_seconds = 15
        self._start_timer()

    # ── Timer ────────────────────────────────────────────────────────────────
    def _start_timer(self):
        self.timer_seconds = 15
        self._tick()

    def _tick(self):
        if self.answered:
            return
        self.timer_seconds -= 1
        frac = max(self.timer_seconds / 15, 0)
        self.timer_bar.place(relwidth=frac, relheight=1.0)
        color = GREEN if frac > 0.4 else (GOLD if frac > 0.2 else ACCENT)
        self.timer_bar.configure(bg=color)
        if self.timer_seconds <= 0:
            self._answer(None, timeout=True)
        else:
            self.root.after(1000, self._tick)

    # ── Question loading ──────────────────────────────────────────────────────
    def _load_question(self):
        self.answered = False
        q = questions[self.q_index]
        total = len(questions)

        self.prog_lbl.config(text=f"Question {self.q_index+1} / {total}")
        frac = (self.q_index) / total
        self.prog_bar.place(relwidth=frac, relheight=1.0)

        self.q_lbl.config(text=f"Q{self.q_index+1}. {q['question']}")

        for i, (badge, btn) in enumerate(self.opt_btns):
            badge.config(bg=ACCENT, fg=WHITE)
            btn.config(text=q['options'][i], bg=CARD, fg=WHITE,
                       state="normal")

        self.next_btn.config(state="disabled")
        self.bubble_lbl.config(text="Choose wisely! 🤔", fg=GOLD)
        self.mascot_lbl.config(text="🤖")
        self._start_timer()

    # ── Answer handling ───────────────────────────────────────────────────────
    def _answer(self, letter, timeout=False):
        if self.answered:
            return
        self.answered = True
        q = questions[self.q_index]
        correct = q['answer']

        for badge, btn in self.opt_btns:
            btn.config(state="disabled")

        for i, (badge, btn) in enumerate(self.opt_btns):
            if LETTERS[i] == correct:
                badge.config(bg=GREEN)
                btn.config(bg="#0a3d2e", fg=GREEN)
            elif letter and LETTERS[i] == letter and letter != correct:
                badge.config(bg=ACCENT)
                btn.config(bg="#3d0a0a", fg=ACCENT)

        if timeout:
            self._mascot_say("Time's up! ⏰", "😅", GOLD)
        elif letter == correct:
            self.score += 1
            self.streak += 1
            self.score_lbl.config(text=f"⭐ {self.score}")
            self.streak_lbl.config(text=f"🔥 {self.streak}")
            msg = "Brilliant! 🎉" if self.streak < 3 else f"🔥 {self.streak} streak!!"
            self._mascot_say(msg, "🥳", GREEN)
            self._flash_popup("✅  CORRECT!", GREEN)
        else:
            self.streak = 0
            self.streak_lbl.config(text="🔥 0")
            self._mascot_say(f"Oops! It was {correct}.", "😬", ACCENT)
            self._flash_popup("❌  WRONG!", ACCENT)

        self.next_btn.config(state="normal")

    # ── Popup overlay ─────────────────────────────────────────────────────────
    def _flash_popup(self, text, color):
        popup = tk.Toplevel(self.root)
        popup.overrideredirect(True)
        popup.attributes("-topmost", True)
        popup.configure(bg=color)

        rx = self.root.winfo_x() + self.root.winfo_width()  // 2
        ry = self.root.winfo_y() + self.root.winfo_height() // 2
        popup.geometry(f"320x100+{rx-160}+{ry-50}")

        tk.Label(popup, text=text, bg=color, fg=WHITE,
                 font=font.Font(family="Helvetica", size=22, weight="bold")
                 ).pack(expand=True)

        def close_popup():
            try:
                popup.destroy()
            except Exception:
                pass

        self.root.after(1100, close_popup)

    # ── Mascot speech ─────────────────────────────────────────────────────────
    def _mascot_say(self, msg, face, color):
        self.mascot_lbl.config(text=face)
        self.bubble_lbl.config(text=msg, fg=color)

    # ── Next question / final score ───────────────────────────────────────────
    def _next_question(self):
        self.q_index += 1
        if self.q_index >= len(questions):
            self._show_final()
        else:
            self._load_question()

    # ── Final score screen ────────────────────────────────────────────────────
    def _show_final(self):
        for w in self.root.winfo_children():
            w.destroy()

        total = len(questions)
        pct   = int(self.score / total * 100)

        if pct == 100:
            face, tag, color = "🏆", "PERFECT SCORE!", GOLD
        elif pct >= 60:
            face, tag, color = "🎉", "Great Job!", GREEN
        else:
            face, tag, color = "💪", "Keep Practicing!", ACCENT

        self.root.configure(bg=BG)
        tk.Frame(self.root, bg=ACCENT, height=56).pack(fill="x")

        frame = tk.Frame(self.root, bg=BG)
        frame.pack(expand=True)

        tk.Label(frame, text=face, bg=BG,
                 font=font.Font(family="Helvetica", size=80)).pack(pady=(30, 0))

        tk.Label(frame, text="Quiz Complete!", bg=BG, fg=WHITE,
                 font=font.Font(family="Helvetica", size=26, weight="bold")
                 ).pack(pady=(10, 0))

        tk.Label(frame, text=tag, bg=BG, fg=color,
                 font=font.Font(family="Helvetica", size=18, weight="bold")
                 ).pack()

        # Score ring (simple canvas circle)
        c = tk.Canvas(frame, width=180, height=180, bg=BG, highlightthickness=0)
        c.pack(pady=20)
        c.create_oval(10, 10, 170, 170, outline=CARD, width=14)
        extent = int(359 * pct / 100)
        c.create_arc(10, 10, 170, 170, start=90, extent=-extent,
                     outline=color, width=14, style="arc")
        c.create_text(90, 82, text=f"{self.score}/{total}",
                      fill=WHITE, font=font.Font(family="Helvetica", size=28, weight="bold"))
        c.create_text(90, 112, text=f"{pct}%", fill=MUTED,
                      font=font.Font(family="Helvetica", size=14))

        # Play again
        tk.Button(frame, text="🔄  Play Again", bg=ACCENT, fg=WHITE,
                  font=font.Font(family="Helvetica", size=13, weight="bold"),
                  relief="flat", padx=28, pady=12, cursor="hand2",
                  command=self._restart).pack(pady=10)

    # ── Restart ───────────────────────────────────────────────────────────────
    def _restart(self):
        self.q_index = 0
        self.score   = 0
        self.streak  = 0
        for w in self.root.winfo_children():
            w.destroy()
        self._build_ui()
        self._load_question()

    # ── Hover helpers ──────────────────────────────────────────────────────────
    def _hover_on(self, btn):
        if btn.cget("state") == "normal":
            btn.config(bg="#3d2a5e")

    def _hover_off(self, btn):
        if btn.cget("state") == "normal":
            btn.config(bg=CARD)


if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()