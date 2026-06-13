import customtkinter as ctk
import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import defaultdict

# ── Theme ──────────────────────────────────────────────────────────────────
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

CSV_FILE = "expenses.csv"

CATEGORIES = ["Food & Drink", "Transport", "Shopping", "Health", "Entertainment", "Utilities", "Other"]

# Pink-toned palette for categories
CAT_COLORS = {
    "Food & Drink":  "#e91e8c",
    "Transport":     "#9c27b0",
    "Shopping":      "#f06292",
    "Health":        "#e91e63",
    "Entertainment": "#ba68c8",
    "Utilities":     "#ce93d8",
    "Other":         "#f48fb1",
}

# ── Pink & White color tokens ──────────────────────────────────────────────
PINK_DARK    = "#c2185b"   # deep rose – sidebar bg
PINK_MID     = "#e91e63"   # primary pink – buttons, accents
PINK_SOFT    = "#f06292"   # medium pink – hover, active nav
PINK_PALE    = "#fce4ec"   # blush – page background
PINK_LIGHTER = "#fce4ec"   # very light – alternating rows
WHITE        = "#ffffff"
CARD_BG      = "#ffffff"
BORDER       = "#f8bbd9"
TEXT_DARK    = "#3d0026"   # near-black with pink undertone
TEXT_MID     = "#880e4f"   # muted body text
TEXT_LIGHT   = "#f8bbd9"   # placeholder / secondary in sidebar

# ── Main App ───────────────────────────────────────────────────────────────
class ExpenseApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SpendWise — Expense Tracker")
        self.geometry("1050x660")
        self.minsize(900, 580)
        self.resizable(True, True)
        self.configure(fg_color=PINK_PALE)

        self.expenses = []
        self.load_csv()
        self.current_section = "dashboard"
        self.chart_canvas = None

        self._build_ui()
        self.show_section("dashboard")

    # ── CSV ────────────────────────────────────────────────────────────────
    def load_csv(self):
        if not os.path.exists(CSV_FILE):
            return
        with open(CSV_FILE, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    self.expenses.append({
                        "name":  row["name"],
                        "price": float(row["price"]),
                        "cat":   row["category"],
                        "date":  row.get("date", datetime.today().strftime("%Y-%m-%d")),
                    })
                except (KeyError, ValueError):
                    pass

    def save_csv(self):
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["name", "price", "category", "date"])
            writer.writeheader()
            for e in self.expenses:
                writer.writerow({"name": e["name"], "price": e["price"],
                                 "category": e["cat"], "date": e["date"]})

    # ── UI skeleton ────────────────────────────────────────────────────────
    def _build_ui(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ── Sidebar ──
        self.sidebar = ctk.CTkFrame(self, width=210, corner_radius=0, fg_color=PINK_DARK)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)
        self.sidebar.grid_rowconfigure(10, weight=1)

        # Logo
        logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_frame.grid(row=0, column=0, padx=16, pady=(28, 20), sticky="ew")
        ctk.CTkLabel(logo_frame, text="💗", font=ctk.CTkFont(size=30)).pack(side="left", padx=(0, 10))
        title_col = ctk.CTkFrame(logo_frame, fg_color="transparent")
        title_col.pack(side="left")
        ctk.CTkLabel(title_col, text="SpendWise",
                     font=ctk.CTkFont(size=16, weight="bold"),
                     text_color=WHITE).pack(anchor="w")
        ctk.CTkLabel(title_col, text="Expense Tracker",
                     font=ctk.CTkFont(size=11),
                     text_color=TEXT_LIGHT).pack(anchor="w")

        # Divider
        ctk.CTkFrame(self.sidebar, height=1, fg_color=PINK_SOFT).grid(
            row=1, column=0, sticky="ew", padx=14, pady=(0, 14))

        # Nav buttons
        self.nav_btns = {}
        nav_items = [
            ("dashboard", "📊  Dashboard"),
            ("add",       "➕  Add Expense"),
            ("history",   "📋  All Expenses"),
        ]
        for i, (key, label) in enumerate(nav_items, start=2):
            btn = ctk.CTkButton(
                self.sidebar, text=label, anchor="w",
                font=ctk.CTkFont(size=13),
                fg_color="transparent",
                hover_color=PINK_SOFT,
                text_color=TEXT_LIGHT,
                corner_radius=10, height=40,
                command=lambda k=key: self.show_section(k)
            )
            btn.grid(row=i, column=0, padx=10, pady=3, sticky="ew")
            self.nav_btns[key] = btn

        # Version
        ctk.CTkLabel(self.sidebar, text="v1.0  ·  CustomTkinter",
                     font=ctk.CTkFont(size=10),
                     text_color=PINK_SOFT).grid(row=11, column=0, pady=14)

        # ── Main area ──
        self.main = ctk.CTkFrame(self, fg_color=PINK_PALE, corner_radius=0)
        self.main.grid(row=0, column=1, sticky="nsew")
        self.main.grid_columnconfigure(0, weight=1)
        self.main.grid_rowconfigure(0, weight=1)

        self._build_dashboard()
        self._build_add()
        self._build_history()

    # ── Sidebar nav ────────────────────────────────────────────────────────
    def show_section(self, key):
        self.current_section = key
        for k, btn in self.nav_btns.items():
            if k == key:
                btn.configure(fg_color=PINK_SOFT, text_color=WHITE)
            else:
                btn.configure(fg_color="transparent", text_color=TEXT_LIGHT)

        self.frame_dashboard.grid_remove()
        self.frame_add.grid_remove()
        self.frame_history.grid_remove()

        if key == "dashboard":
            self.frame_dashboard.grid()
            self._refresh_dashboard()
        elif key == "add":
            self.frame_add.grid()
        elif key == "history":
            self.frame_history.grid()
            self._refresh_history()

    # ── Helper: white card ─────────────────────────────────────────────────
    def _card(self, parent, **kwargs):
        return ctk.CTkFrame(parent, corner_radius=14, fg_color=WHITE,
                            border_width=1, border_color=BORDER, **kwargs)

    # ── Dashboard ──────────────────────────────────────────────────────────
    def _build_dashboard(self):
        self.frame_dashboard = ctk.CTkFrame(self.main, fg_color="transparent")
        self.frame_dashboard.grid(row=0, column=0, sticky="nsew", padx=24, pady=20)
        self.frame_dashboard.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.frame_dashboard.grid_rowconfigure(2, weight=1)

        # Title
        ctk.CTkLabel(self.frame_dashboard, text="Dashboard",
                     font=ctk.CTkFont(size=22, weight="bold"),
                     text_color=PINK_DARK).grid(
            row=0, column=0, columnspan=4, sticky="w", pady=(0, 16))

        # Metric cards
        metrics = [
            ("💰", "Total Spent",   "m_total", PINK_MID),
            ("🧾", "Transactions",  "m_count", "#9c27b0"),
            ("📈", "Avg. per Item", "m_avg",   PINK_SOFT),
            ("🏷️", "Top Category", "m_top",   PINK_DARK),
        ]
        self.metric_labels = {}
        for i, (icon, label, attr, color) in enumerate(metrics):
            card = self._card(self.frame_dashboard)
            card.grid(row=1, column=i, padx=(0 if i == 0 else 8, 0), pady=(0, 16), sticky="ew")
            card.grid_columnconfigure(0, weight=1)

            # Top colour stripe
            stripe = ctk.CTkFrame(card, height=4, corner_radius=0, fg_color=color)
            stripe.grid(row=0, column=0, sticky="ew")

            ctk.CTkLabel(card, text=icon, font=ctk.CTkFont(size=24)).grid(row=1, column=0, pady=(12, 2))
            val_lbl = ctk.CTkLabel(card, text="—",
                                   font=ctk.CTkFont(size=21, weight="bold"),
                                   text_color=color)
            val_lbl.grid(row=2, column=0)
            ctk.CTkLabel(card, text=label,
                         font=ctk.CTkFont(size=11),
                         text_color=TEXT_MID).grid(row=3, column=0, pady=(2, 14))
            self.metric_labels[attr] = val_lbl

        # Bottom row
        bottom = ctk.CTkFrame(self.frame_dashboard, fg_color="transparent")
        bottom.grid(row=2, column=0, columnspan=4, sticky="nsew")
        bottom.grid_columnconfigure(0, weight=3)
        bottom.grid_columnconfigure(1, weight=2)
        bottom.grid_rowconfigure(0, weight=1)

        # Chart card
        chart_card = self._card(bottom)
        chart_card.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        chart_card.grid_rowconfigure(1, weight=1)
        chart_card.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(chart_card, text="Spending by Category",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color=PINK_DARK).grid(row=0, column=0, padx=16, pady=(14, 4), sticky="w")
        self.chart_frame = ctk.CTkFrame(chart_card, fg_color="transparent")
        self.chart_frame.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0, 8))

        # Breakdown card
        bk_card = self._card(bottom)
        bk_card.grid(row=0, column=1, sticky="nsew")
        bk_card.grid_columnconfigure(0, weight=1)
        bk_card.grid_rowconfigure(1, weight=1)
        ctk.CTkLabel(bk_card, text="Category Breakdown",
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color=PINK_DARK).grid(row=0, column=0, padx=16, pady=(14, 8), sticky="w")
        self.breakdown_frame = ctk.CTkScrollableFrame(bk_card, fg_color="transparent",
                                                      scrollbar_button_color=PINK_PALE,
                                                      scrollbar_button_hover_color=BORDER)
        self.breakdown_frame.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0, 8))

    def _refresh_dashboard(self):
        total = sum(e["price"] for e in self.expenses)
        count = len(self.expenses)
        avg   = total / count if count else 0

        cats = defaultdict(float)
        for e in self.expenses:
            cats[e["cat"]] += e["price"]
        top = max(cats, key=cats.get) if cats else "—"

        self.metric_labels["m_total"].configure(text=f"${total:,.2f}")
        self.metric_labels["m_count"].configure(text=str(count))
        self.metric_labels["m_avg"].configure(text=f"${avg:,.2f}")
        self.metric_labels["m_top"].configure(text=top.split()[0] if top != "—" else "—")

        self._draw_chart(cats)
        self._draw_breakdown(cats, total)

    def _draw_chart(self, cats):
        for w in self.chart_frame.winfo_children():
            w.destroy()
        if self.chart_canvas:
            plt.close("all")
            self.chart_canvas = None

        if not cats:
            ctk.CTkLabel(self.chart_frame, text="No data yet",
                         text_color=TEXT_MID, font=ctk.CTkFont(size=13)).pack(pady=40)
            return

        sorted_cats = sorted(cats.items(), key=lambda x: x[1], reverse=True)
        labels = [c for c, _ in sorted_cats]
        values = [v for _, v in sorted_cats]
        colors = [CAT_COLORS.get(c, PINK_SOFT) for c in labels]

        fig, ax = plt.subplots(figsize=(5.2, 2.9), facecolor=WHITE)
        ax.set_facecolor(WHITE)
        bars = ax.bar(labels, values, color=colors, width=0.55, zorder=3)
        ax.yaxis.grid(True, color=BORDER, linewidth=0.6, zorder=0)
        ax.set_axisbelow(True)
        ax.spines[:].set_visible(False)
        ax.tick_params(colors=TEXT_MID, labelsize=9)
        ax.set_xticklabels([l.split()[0] for l in labels], color=TEXT_MID, fontsize=9)
        ax.yaxis.set_tick_params(labelcolor=TEXT_MID)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:,.0f}"))
        for bar, val in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + max(values) * 0.02,
                    f"${val:,.0f}", ha="center", va="bottom",
                    color=TEXT_DARK, fontsize=8, fontweight="bold")
        fig.tight_layout(pad=1.0)

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        self.chart_canvas = canvas

    def _draw_breakdown(self, cats, total):
        for w in self.breakdown_frame.winfo_children():
            w.destroy()
        if not cats:
            ctk.CTkLabel(self.breakdown_frame, text="No expenses yet",
                         text_color=TEXT_MID, font=ctk.CTkFont(size=12)).pack(pady=20)
            return

        sorted_cats = sorted(cats.items(), key=lambda x: x[1], reverse=True)
        for cat, val in sorted_cats:
            pct   = (val / total * 100) if total else 0
            color = CAT_COLORS.get(cat, PINK_SOFT)
            row   = ctk.CTkFrame(self.breakdown_frame, fg_color="transparent")
            row.pack(fill="x", pady=5)
            row.grid_columnconfigure(1, weight=1)

            ctk.CTkLabel(row, text=cat, font=ctk.CTkFont(size=12),
                         text_color=TEXT_MID, width=110, anchor="w").grid(row=0, column=0, sticky="w")
            ctk.CTkLabel(row, text=f"${val:,.2f}", font=ctk.CTkFont(size=12, weight="bold"),
                         text_color=color, width=70, anchor="e").grid(row=0, column=2, sticky="e")
            ctk.CTkLabel(row, text=f"{pct:.0f}%", font=ctk.CTkFont(size=10),
                         text_color=TEXT_MID, width=36, anchor="e").grid(row=0, column=3, padx=(4, 0))
            bar = ctk.CTkProgressBar(row, height=6, corner_radius=3,
                                     progress_color=color, fg_color=PINK_PALE)
            bar.set(pct / 100)
            bar.grid(row=1, column=0, columnspan=4, sticky="ew", pady=(3, 0))

    # ── Add Expense ────────────────────────────────────────────────────────
    def _build_add(self):
        self.frame_add = ctk.CTkFrame(self.main, fg_color="transparent")
        self.frame_add.grid(row=0, column=0, sticky="nsew", padx=24, pady=20)
        self.frame_add.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self.frame_add, text="Add Expense",
                     font=ctk.CTkFont(size=22, weight="bold"),
                     text_color=PINK_DARK).pack(anchor="w", pady=(0, 20))

        card = self._card(self.frame_add)
        card.pack(fill="x", pady=(0, 16))

        # Pink top stripe
        ctk.CTkFrame(card, height=4, corner_radius=0, fg_color=PINK_MID).pack(fill="x")

        def field_label(text):
            ctk.CTkLabel(card, text=text, font=ctk.CTkFont(size=12),
                         text_color=TEXT_MID).pack(anchor="w", padx=22, pady=(14, 3))

        field_label("Item name")
        self.f_name = ctk.CTkEntry(card, placeholder_text="e.g. Grocery run",
                                   height=38, corner_radius=8,
                                   border_color=BORDER, fg_color=PINK_PALE,
                                   text_color=TEXT_DARK,
                                   placeholder_text_color=TEXT_MID)
        self.f_name.pack(fill="x", padx=22)

        # Two-column row
        row = ctk.CTkFrame(card, fg_color="transparent")
        row.pack(fill="x", padx=22)
        row.grid_columnconfigure((0, 1), weight=1)

        left = ctk.CTkFrame(row, fg_color="transparent")
        left.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        ctk.CTkLabel(left, text="Amount ($)", font=ctk.CTkFont(size=12),
                     text_color=TEXT_MID).pack(anchor="w", pady=(14, 3))
        self.f_price = ctk.CTkEntry(left, placeholder_text="0.00", height=38, corner_radius=8,
                                    border_color=BORDER, fg_color=PINK_PALE,
                                    text_color=TEXT_DARK,
                                    placeholder_text_color=TEXT_MID)
        self.f_price.pack(fill="x")

        right = ctk.CTkFrame(row, fg_color="transparent")
        right.grid(row=0, column=1, sticky="ew")
        ctk.CTkLabel(right, text="Category", font=ctk.CTkFont(size=12),
                     text_color=TEXT_MID).pack(anchor="w", pady=(14, 3))
        self.f_cat = ctk.CTkOptionMenu(right, values=CATEGORIES, height=38, corner_radius=8,
                                       fg_color=PINK_PALE,
                                       button_color=PINK_MID,
                                       button_hover_color=PINK_DARK,
                                       text_color=TEXT_DARK,
                                       dropdown_fg_color=WHITE,
                                       dropdown_text_color=TEXT_DARK,
                                       dropdown_hover_color=PINK_PALE)
        self.f_cat.pack(fill="x")

        field_label("Date (YYYY-MM-DD)")
        self.f_date = ctk.CTkEntry(card, placeholder_text=datetime.today().strftime("%Y-%m-%d"),
                                   height=38, corner_radius=8,
                                   border_color=BORDER, fg_color=PINK_PALE,
                                   text_color=TEXT_DARK,
                                   placeholder_text_color=TEXT_MID)
        self.f_date.insert(0, datetime.today().strftime("%Y-%m-%d"))
        self.f_date.pack(fill="x", padx=22, pady=(0, 4))

        self.add_status = ctk.CTkLabel(card, text="", font=ctk.CTkFont(size=12))
        self.add_status.pack(pady=(4, 0))

        ctk.CTkButton(card, text="➕  Add Expense", height=44, corner_radius=10,
                      font=ctk.CTkFont(size=14, weight="bold"),
                      fg_color=PINK_MID, hover_color=PINK_DARK, text_color=WHITE,
                      command=self._add_expense).pack(fill="x", padx=22, pady=(10, 22))

    def _add_expense(self):
        name  = self.f_name.get().strip()
        price = self.f_price.get().strip()
        cat   = self.f_cat.get()
        date  = self.f_date.get().strip() or datetime.today().strftime("%Y-%m-%d")

        if not name:
            self.add_status.configure(text="⚠  Item name is required", text_color="#e53935"); return
        try:
            price = float(price)
            if price <= 0: raise ValueError
        except ValueError:
            self.add_status.configure(text="⚠  Enter a valid amount > 0", text_color="#e53935"); return

        self.expenses.append({"name": name, "price": price, "cat": cat, "date": date})
        self.save_csv()
        self.add_status.configure(text=f"✓  '{name}' added!", text_color=PINK_MID)
        self.f_name.delete(0, "end")
        self.f_price.delete(0, "end")
        self.after(2000, lambda: self.add_status.configure(text=""))

    # ── History ────────────────────────────────────────────────────────────
    def _build_history(self):
        self.frame_history = ctk.CTkFrame(self.main, fg_color="transparent")
        self.frame_history.grid(row=0, column=0, sticky="nsew", padx=24, pady=20)
        self.frame_history.grid_columnconfigure(0, weight=1)
        self.frame_history.grid_rowconfigure(1, weight=1)

        # Header
        hdr = ctk.CTkFrame(self.frame_history, fg_color="transparent")
        hdr.grid(row=0, column=0, sticky="ew", pady=(0, 14))
        hdr.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(hdr, text="All Expenses",
                     font=ctk.CTkFont(size=22, weight="bold"),
                     text_color=PINK_DARK).grid(row=0, column=0, sticky="w")

        ctrl = ctk.CTkFrame(hdr, fg_color="transparent")
        ctrl.grid(row=0, column=1)
        self.hist_filter = ctk.CTkOptionMenu(ctrl, values=["All"] + CATEGORIES,
                                             width=155, height=34, corner_radius=8,
                                             fg_color=WHITE,
                                             button_color=PINK_MID,
                                             button_hover_color=PINK_DARK,
                                             text_color=TEXT_DARK,
                                             dropdown_fg_color=WHITE,
                                             dropdown_text_color=TEXT_DARK,
                                             dropdown_hover_color=PINK_PALE,
                                             command=lambda _: self._refresh_history())
        self.hist_filter.pack(side="left", padx=(0, 8))
        ctk.CTkButton(ctrl, text="🗑  Clear All", width=110, height=34, corner_radius=8,
                      fg_color="#e91e63", hover_color=PINK_DARK, text_color=WHITE,
                      command=self._clear_all).pack(side="left")

        # List card
        card = self._card(self.frame_history)
        card.grid(row=1, column=0, sticky="nsew")
        card.grid_columnconfigure(0, weight=1)
        card.grid_rowconfigure(0, weight=1)

        self.hist_scroll = ctk.CTkScrollableFrame(card, fg_color="transparent",
                                                  scrollbar_button_color=PINK_PALE,
                                                  scrollbar_button_hover_color=BORDER)
        self.hist_scroll.grid(row=0, column=0, sticky="nsew", padx=4, pady=4)
        self.hist_scroll.grid_columnconfigure(0, weight=1)

        self.hist_status = ctk.CTkLabel(self.frame_history, text="",
                                        font=ctk.CTkFont(size=12), text_color=PINK_MID)
        self.hist_status.grid(row=2, column=0, pady=(8, 0))

    def _refresh_history(self):
        for w in self.hist_scroll.winfo_children():
            w.destroy()

        flt  = self.hist_filter.get()
        data = [e for e in self.expenses if flt == "All" or e["cat"] == flt]

        if not data:
            ctk.CTkLabel(self.hist_scroll, text="No expenses found.",
                         text_color=TEXT_MID, font=ctk.CTkFont(size=13)).pack(pady=30)
            return

        # Column headers
        hdr = ctk.CTkFrame(self.hist_scroll, fg_color="transparent")
        hdr.pack(fill="x", padx=8, pady=(4, 2))
        for text, w in [("#", 32), ("Item", 0), ("Category", 130), ("Date", 100), ("Amount", 80), ("", 36)]:
            ctk.CTkLabel(hdr, text=text, font=ctk.CTkFont(size=11, weight="bold"),
                         text_color=TEXT_MID, width=w, anchor="w").pack(side="left", padx=4)
            if text == "Item":
                ctk.CTkLabel(hdr, text="", width=0).pack(side="left", expand=True)

        ctk.CTkFrame(self.hist_scroll, height=1, fg_color=BORDER).pack(fill="x", padx=8, pady=2)

        for i, e in enumerate(reversed(data)):
            real_idx = self.expenses.index(e)
            color    = CAT_COLORS.get(e["cat"], PINK_SOFT)
            row_bg   = PINK_PALE if i % 2 == 0 else WHITE
            row = ctk.CTkFrame(self.hist_scroll, fg_color=row_bg, corner_radius=6)
            row.pack(fill="x", padx=8, pady=1)

            ctk.CTkLabel(row, text=str(i + 1), font=ctk.CTkFont(size=12),
                         text_color=TEXT_MID, width=32).pack(side="left", padx=6, pady=8)
            ctk.CTkLabel(row, text=e["name"], font=ctk.CTkFont(size=13),
                         text_color=TEXT_DARK, anchor="w").pack(side="left", expand=True, fill="x")
            ctk.CTkLabel(row, text=e["cat"], font=ctk.CTkFont(size=11),
                         text_color=color, width=130, anchor="w").pack(side="left")
            ctk.CTkLabel(row, text=e["date"], font=ctk.CTkFont(size=11),
                         text_color=TEXT_MID, width=100).pack(side="left")
            ctk.CTkLabel(row, text=f"${e['price']:,.2f}",
                         font=ctk.CTkFont(size=13, weight="bold"),
                         text_color=color, width=80, anchor="e").pack(side="left")
            ctk.CTkButton(row, text="✕", width=28, height=26, corner_radius=6,
                          fg_color="transparent", hover_color="#fce4ec",
                          text_color=TEXT_MID,
                          command=lambda idx=real_idx: self._delete(idx)).pack(side="left", padx=6)

    def _delete(self, idx):
        self.expenses.pop(idx)
        self.save_csv()
        self._refresh_history()
        self.hist_status.configure(text="✓  Deleted")
        self.after(1800, lambda: self.hist_status.configure(text=""))

    def _clear_all(self):
        from tkinter import messagebox
        if not messagebox.askyesno("Clear all", "Delete ALL expenses? This cannot be undone."):
            return
        self.expenses.clear()
        self.save_csv()
        self._refresh_history()


# ── Entry ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = ExpenseApp()
    app.mainloop()
