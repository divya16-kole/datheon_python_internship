import tkinter as tk
import random

# ==================== NEON COLOURS ====================
BG = "#10051F"
PANEL = "#241044"
PURPLE = "#A855F7"
PINK = "#FF3CAC"
CYAN = "#00E5FF"
YELLOW = "#FFE45E"
WHITE = "#FFFFFF"
MUTED = "#D8C8F5"
GREEN = "#48FFB1"
RED = "#FF5577"
DARK_BUTTON = "#39205F"

WORDS = {
    "PYTHON": ("PROGRAMMING", "A popular programming language"),
    "VARIABLE": ("PROGRAMMING", "Stores a value in a program"),
    "FUNCTION": ("PROGRAMMING", "Reusable block of code"),
    "ALGORITHM": ("PROGRAMMING", "Steps to solve a problem"),
    "DATABASE": ("TECHNOLOGY", "Organized collection of data"),
    "KEYBOARD": ("TECHNOLOGY", "Used to type on a computer"),
    "INTERNET": ("TECHNOLOGY", "Connects computers worldwide"),
    "SOFTWARE": ("TECHNOLOGY", "Programs running on a computer"),
    "NETWORK": ("TECHNOLOGY", "Connected computers and devices"),
    "ROBOT": ("TECHNOLOGY", "A machine that performs tasks"),
    "ENGINEERING": ("COLLEGE", "Designing and building things"),
    "STUDENT": ("COLLEGE", "A person who studies"),
    "LIBRARY": ("EDUCATION", "A place to borrow books"),
    "SCIENCE": ("EDUCATION", "Study of the natural world"),
    "BUTTERFLY": ("NATURE", "An insect with colorful wings"),
    "MOUNTAIN": ("NATURE", "A very high area of land"),
    "SUNSHINE": ("NATURE", "Light from the sun"),
    "CHOCOLATE": ("FOOD", "A sweet treat made from cocoa"),
    "ELEPHANT": ("ANIMALS", "A large animal with a trunk"),
    "JAVASCRIPT": ("PROGRAMMING", "A language used on websites"),
    "COMPILER": ("PROGRAMMING", "Translates source code"),
    "DEBUGGING": ("PROGRAMMING", "Finding and fixing code errors"),
    "CLOUD": ("TECHNOLOGY", "Online computing and storage"),
    "GRADUATION": ("EDUCATION", "Completion of a course of study"),
    "FRIEND": ("EVERYDAY", "Someone you trust and enjoy"),
    "RAINBOW": ("NATURE", "Colorful arc in the sky"),
    "APPLICATION": ("TECHNOLOGY", "A program designed for a task"),
    "INNOVATION": ("TECHNOLOGY", "A new idea or improvement"),
    "AUTOMATION": ("TECHNOLOGY", "Machines performing tasks"),
    "PORTFOLIO": ("CAREER", "A collection showcasing your work"),
}

LEVELS = {
    "Easy": 8,
    "Medium": 6,
    "Hard": 4,
}


class HangmanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HANGMAN | Neon Word Challenge")
        self.root.geometry("1000x740")
        self.root.minsize(850, 680)
        self.root.configure(bg=BG)

        self.difficulty = tk.StringVar(value="Medium")
        self.sound_enabled = tk.BooleanVar(value=False)
        self.hints_enabled = tk.BooleanVar(value=True)

        self.total_wins = 0
        self.total_losses = 0
        self.streak = 0
        self.level = 1

        self.show_welcome()
        self.root.bind("<KeyPress>", self.on_key)

    # ==================== COMMON HELPERS ====================

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.letter_buttons = {}

    def button(self, parent, text, command, color=PURPLE, width=22):
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            font=("Segoe UI", 12, "bold"),
            bg=color,
            fg=WHITE,
            activebackground=CYAN,
            activeforeground=BG,
            relief="flat",
            bd=0,
            padx=18,
            pady=12,
            width=width,
            cursor="hand2"
        )

        btn.bind(
            "<Enter>",
            lambda event: btn.config(bg=PINK, fg=WHITE)
            if btn["state"] != "disabled" else None
        )

        btn.bind(
            "<Leave>",
            lambda event: btn.config(bg=color, fg=WHITE)
            if btn["state"] != "disabled" else None
        )

        return btn

    def title(self, parent, text, size=30):
        tk.Label(
            parent,
            text=text,
            font=("Segoe UI", size, "bold"),
            bg=BG,
            fg=WHITE
        ).pack(pady=8)

    def make_card(self, parent, padx=25, pady=22):
        return tk.Frame(
            parent,
            bg=PANEL,
            padx=padx,
            pady=pady,
            highlightbackground=PURPLE,
            highlightthickness=2
        )

    # ==================== ANIMATED BACKGROUND ====================

    def create_stars(self, canvas, amount=120):
        stars = []
        width = max(self.root.winfo_width(), 850)
        height = max(self.root.winfo_height(), 680)

        for _ in range(amount):
            x = random.randint(0, width)
            y = random.randint(0, height)
            size = random.randint(2, 5)
            speed = random.uniform(0.5, 2.0)
            drift = random.choice([-1, 0, 1])
            color = random.choice(
                [PURPLE, CYAN, PINK, WHITE, YELLOW]
            )

            star = canvas.create_oval(
                x, y, x + size, y + size,
                fill=color,
                outline=color
            )

            stars.append((star, speed, drift))

        self.animate_stars(canvas, stars)

    def animate_stars(self, canvas, stars):
        if not canvas.winfo_exists():
            return

        width = max(canvas.winfo_width(), 850)
        height = max(canvas.winfo_height(), 680)

        for star, speed, drift in stars:
            canvas.move(star, drift, speed)

            coords = canvas.coords(star)
            if not coords:
                continue

            x1, y1, x2, y2 = coords

            if y1 > height:
                x = random.randint(0, width)
                canvas.coords(star, x, -6, x + 4, -2)

            elif x1 > width:
                canvas.move(star, -width, 0)

            elif x2 < 0:
                canvas.move(star, width, 0)

        canvas.after(
            40,
            lambda: self.animate_stars(canvas, stars)
        )

    # ==================== PAGE 1: WELCOME ====================

    def show_welcome(self):
        self.clear()

        canvas = tk.Canvas(
            self.root,
            bg=BG,
            highlightthickness=0
        )
        canvas.place(relwidth=1, relheight=1)

        self.create_stars(canvas, 120)

        card = tk.Frame(self.root, bg=BG)
        card.place(relx=0.5, rely=0.49, anchor="center")

        tk.Label(
            card,
            text="✦  WELCOME TO  ✦",
            font=("Segoe UI", 14, "bold"),
            bg=BG,
            fg=CYAN
        ).pack(pady=8)

        tk.Label(
            card,
            text="HANGMAN",
            font=("Segoe UI", 48, "bold"),
            bg=BG,
            fg=WHITE
        ).pack()

        tk.Label(
            card,
            text="N E O N   W O R D   C H A L L E N G E",
            font=("Segoe UI", 15, "bold"),
            bg=BG,
            fg=PINK
        ).pack(pady=8)

        tk.Label(
            card,
            text="THINK SMART  •  GUESS LETTERS  •  WIN BIG",
            font=("Segoe UI", 11, "bold"),
            bg=BG,
            fg=YELLOW
        ).pack(pady=10)

        tk.Label(
            card,
            text="Can you discover every hidden word?",
            font=("Segoe UI", 12),
            bg=BG,
            fg=MUTED
        ).pack(pady=5)

        self.button(
            card,
            "▶   PLAY NOW",
            self.start_game,
            PURPLE,
            24
        ).pack(pady=12)

        self.button(
            card,
            "⚙   SETTINGS",
            self.show_settings,
            "#56358C",
            24
        ).pack(pady=5)

        tk.Label(
            card,
            text=(
                f"🏆 WINS: {self.total_wins}    "
                f"🔥 STREAK: {self.streak}"
            ),
            font=("Segoe UI", 12, "bold"),
            bg=BG,
            fg=YELLOW
        ).pack(pady=18)

    # ==================== PAGE 2: SETTINGS ====================

    def show_settings(self):
        self.clear()

        self.title(self.root, "⚙  GAME SETTINGS", 30)

        panel = self.make_card(self.root, 35, 25)
        panel.pack(padx=45, pady=12)

        tk.Label(
            panel,
            text="CHOOSE YOUR CHALLENGE",
            font=("Segoe UI", 15, "bold"),
            bg=PANEL,
            fg=CYAN
        ).pack(pady=12)

        for name, lives in LEVELS.items():
            tk.Radiobutton(
                panel,
                text=f"  {name.upper()}  —  {lives} mistakes allowed",
                variable=self.difficulty,
                value=name,
                font=("Segoe UI", 12, "bold"),
                bg=PANEL,
                fg=WHITE,
                selectcolor="#56358C",
                activebackground=PANEL,
                activeforeground=CYAN,
                cursor="hand2"
            ).pack(anchor="w", pady=7)

        tk.Frame(panel, bg=PURPLE, height=2).pack(
            fill="x", pady=12
        )

        tk.Checkbutton(
            panel,
            text="💡  Enable hint button",
            variable=self.hints_enabled,
            font=("Segoe UI", 11, "bold"),
            bg=PANEL,
            fg=WHITE,
            selectcolor="#56358C",
            activebackground=PANEL,
            activeforeground=CYAN,
            cursor="hand2"
        ).pack(anchor="w", pady=7)

        tk.Checkbutton(
            panel,
            text="♫  Enable sound effects",
            variable=self.sound_enabled,
            font=("Segoe UI", 11, "bold"),
            bg=PANEL,
            fg=WHITE,
            selectcolor="#56358C",
            activebackground=PANEL,
            activeforeground=CYAN,
            cursor="hand2"
        ).pack(anchor="w", pady=7)

        tk.Label(
            panel,
            text="Sound toggle is a setting only; audio is not implemented.",
            font=("Segoe UI", 9),
            bg=PANEL,
            fg=MUTED
        ).pack(pady=8)

        self.button(
            panel,
            "✓   SAVE & PLAY",
            self.start_game,
            PURPLE,
            24
        ).pack(pady=10)

        self.button(
            panel,
            "←   BACK HOME",
            self.show_welcome,
            "#56358C",
            24
        ).pack(pady=5)

    # ==================== START / NEW GAME ====================

    def start_game(self):
        self.word = random.choice(list(WORDS.keys()))
        self.category, self.hint = WORDS[self.word]

        self.guessed = set()
        self.wrong = 0
        self.max_wrong = LEVELS[self.difficulty.get()]
        self.hint_used = False
        self.game_over = False
        self.message = "Choose a letter and start guessing!"

        self.show_game()

    # ==================== PAGE 3: GAMEPLAY ====================

    def show_game(self):
        self.clear()

        header = tk.Frame(self.root, bg=BG)
        header.pack(fill="x", pady=(10, 5))

        tk.Label(
            header,
            text="✦ H A N G M A N ✦",
            font=("Segoe UI", 27, "bold"),
            bg=BG,
            fg=WHITE
        ).pack()

        tk.Label(
            header,
            text=(
                f"LEVEL {self.level}   •   "
                f"{self.difficulty.get().upper()} MODE"
            ),
            font=("Segoe UI", 11, "bold"),
            bg=BG,
            fg=CYAN
        ).pack(pady=3)

        body = tk.Frame(self.root, bg=BG)
        body.pack(
            fill="both",
            expand=True,
            padx=22,
            pady=8
        )

        left = tk.Frame(
            body,
            bg=PANEL,
            padx=12,
            pady=12,
            highlightbackground=PURPLE,
            highlightthickness=2
        )
        left.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10)
        )

        self.canvas = tk.Canvas(
            left,
            bg=PANEL,
            width=300,
            height=330,
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

        self.wrong_label = tk.Label(
            left,
            text="",
            font=("Segoe UI", 11, "bold"),
            bg=PANEL,
            fg=YELLOW
        )
        self.wrong_label.pack(pady=8)

        right = tk.Frame(
            body,
            bg=PANEL,
            padx=15,
            pady=12,
            highlightbackground=CYAN,
            highlightthickness=2
        )
        right.pack(
            side="right",
            fill="both",
            expand=True
        )

        tk.Label(
            right,
            text="GUESS THE WORD",
            font=("Segoe UI", 14, "bold"),
            bg=PANEL,
            fg=WHITE
        ).pack(anchor="w")

        self.category_label = tk.Label(
            right,
            text="",
            font=("Segoe UI", 10, "bold"),
            bg=PANEL,
            fg=CYAN
        )
        self.category_label.pack(anchor="w", pady=(8, 0))

        self.word_label = tk.Label(
            right,
            text="",
            font=("Consolas", 21, "bold"),
            bg=PANEL,
            fg=WHITE,
            wraplength=420
        )
        self.word_label.pack(anchor="w", pady=12)

        self.lives_label = tk.Label(
            right,
            text="",
            font=("Segoe UI", 12, "bold"),
            bg=PANEL,
            fg=PINK
        )
        self.lives_label.pack(anchor="w")

        self.hint_label = tk.Label(
            right,
            text="Hint available!",
            font=("Segoe UI", 10),
            bg=PANEL,
            fg=MUTED,
            wraplength=400
        )
        self.hint_label.pack(anchor="w", pady=8)

        if self.hints_enabled.get():
            self.hint_button = self.button(
                right,
                "💡  USE HINT",
                self.use_hint,
                "#56358C",
                12
            )
            self.hint_button.pack(anchor="w", pady=4)

        tk.Label(
            right,
            text="CLICK A LETTER",
            font=("Segoe UI", 10, "bold"),
            bg=PANEL,
            fg=CYAN
        ).pack(anchor="w", pady=(10, 6))

        self.letters = tk.Frame(right, bg=PANEL)
        self.letters.pack(anchor="w")

        self.letter_buttons = {}

        for i, letter in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            btn = tk.Button(
                self.letters,
                text=letter,
                font=("Segoe UI", 10, "bold"),
                width=3,
                pady=4,
                bg=DARK_BUTTON,
                fg=WHITE,
                activebackground=PINK,
                activeforeground=WHITE,
                relief="flat",
                bd=0,
                cursor="hand2",
                # command=lambda ch=letter: self.guess(ch)
                command=lambda ch=letter:
                print("Clicked:",ch)

            )

            btn.grid(
                row=i // 7,
                column=i % 7,
                padx=3,
                pady=3
            )

            btn.bind(
                "<Enter>",
                lambda event, b=btn: b.config(bg=CYAN, fg=BG)
                if b["state"] != "disabled" else None
            )

            btn.bind(
                "<Leave>",
                lambda event, b=btn, ch=letter: b.config(
                    bg=GREEN if ch in self.word else "#672D51",
                    fg=BG if ch in self.word else WHITE
                ) if ch in self.guessed else b.config(
                    bg=DARK_BUTTON, fg=WHITE
                )
            )

            self.letter_buttons[letter] = btn

        self.message_label = tk.Label(
            right,
            text="",
            font=("Segoe UI", 10, "bold"),
            bg=PANEL,
            fg=YELLOW,
            wraplength=410
        )
        self.message_label.pack(anchor="w", pady=10)

        footer = tk.Frame(self.root, bg=BG)
        footer.pack(fill="x", padx=24, pady=10)

        self.button(
            footer,
            "⌂  HOME",
            self.show_welcome,
            "#56358C",
            10
        ).pack(side="left")

        self.button(
            footer,
            "↻  NEW GAME",
            self.start_game,
            PURPLE,
            13
        ).pack(side="left", padx=12)

        self.update_game()

    # ==================== HANGMAN DRAWING ====================

    def draw_hangman(self):
        self.canvas.delete("all")
        c = self.canvas
        wood = "#C3B6FF"

        c.create_text(
            150, 15,
            text="MISTAKES",
            fill=CYAN,
            font=("Segoe UI", 10, "bold")
        )

        c.create_line(
            35, 300, 270, 300,
            fill=wood, width=5
        )
        c.create_line(
            85, 300, 85, 35,
            fill=wood, width=5
        )
        c.create_line(
            85, 35, 215, 35,
            fill=wood, width=5
        )
        c.create_line(
            215, 35, 215, 65,
            fill=wood, width=5
        )

        parts = [
            lambda: c.create_oval(
                190, 65, 240, 115,
                outline=PINK, width=4
            ),
            lambda: c.create_line(
                215, 115, 215, 190,
                fill=CYAN, width=4
            ),
            lambda: c.create_line(
                215, 135, 180, 165,
                fill=CYAN, width=4
            ),
            lambda: c.create_line(
                215, 135, 250, 165,
                fill=CYAN, width=4
            ),
            lambda: c.create_line(
                215, 190, 185, 240,
                fill=PURPLE, width=4
            ),
            lambda: c.create_line(
                215, 190, 245, 240,
                fill=PURPLE, width=4
            ),
            lambda: c.create_oval(
                202, 80, 208, 86,
                fill=WHITE, outline=WHITE
            ),
            lambda: c.create_oval(
                222, 80, 228, 86,
                fill=WHITE, outline=WHITE
            ),
        ]

        count = round(
            self.wrong * len(parts) / self.max_wrong
        )

        for part in parts[:min(count, len(parts))]:
            part()

        c.create_text(
            150, 320,
            text="GUESS • THINK • WIN",
            fill=CYAN,
            font=("Segoe UI", 10, "bold")
        )

        self.wrong_label.config(
            text=f"✖  MISTAKES: {self.wrong}/{self.max_wrong}"
        )

    # ==================== GUESS LOGIC ====================

    def guess(self, letter):
        if self.game_over or letter in self.guessed:
            return

        self.guessed.add(letter)

        if letter in self.word:
            self.message = f"✨ Great guess! {letter} is correct."
        else:
            self.wrong += 1
            self.message = (
                f"Not this time! {letter} is not in the word."
            )

        if all(ch in self.guessed for ch in self.word):
            self.game_over = True
            self.total_wins += 1
            self.streak += 1
            self.show_result(True)
            return

        if self.wrong >= self.max_wrong:
            self.game_over = True
            self.total_losses += 1
            self.streak = 0
            self.show_result(False)
            return

        self.update_game()

    def use_hint(self):
        if self.game_over or self.hint_used:
            return

        self.hint_used = True
        self.wrong += 1
        self.hint_label.config(text=f"💡 CLUE: {self.hint}")
        self.message = "Hint used! It costs one mistake."

        if hasattr(self, "hint_button"):
            self.hint_button.config(
                text="✓  HINT USED",
                state="disabled",
                bg="#672D51"
            )

        if self.wrong >= self.max_wrong:
            self.game_over = True
            self.total_losses += 1
            self.streak = 0
            self.show_result(False)
            return

        self.update_game()

    def update_game(self):
        shown = "  ".join(
            ch if ch in self.guessed else "_"
            for ch in self.word
        )

        self.word_label.config(text=shown)

        self.category_label.config(
            text=f"✦ CATEGORY: {self.category}"
        )

        remaining = self.max_wrong - self.wrong

        self.lives_label.config(
            text=f"♥ LIVES LEFT: {remaining}",
            fg=GREEN if remaining > 2 else RED
        )

        self.message_label.config(text=self.message)
        self.draw_hangman()

        for letter, btn in self.letter_buttons.items():
            if letter in self.guessed:
                if letter in self.word:
                    btn.config(
                        state="disabled",
                        bg=GREEN,
                        fg=BG
                    )
                else:
                    btn.config(
                        state="disabled",
                        bg="#672D51",
                        fg=WHITE
                    )
            else:
                btn.config(
                    state="normal",
                    bg=DARK_BUTTON,
                    fg=WHITE
                )

    def on_key(self, event):
     letter = event.char.upper()

    # Ignore keyboard input outside the gameplay screen
     if not hasattr(self, "word_label"):
        return

     if not self.word_label.winfo_exists():
        return

     if (
        len(letter) == 1
        and letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        and letter in self.letter_buttons
    ):
        self.guess(letter)
    # ==================== RESULT ANIMATIONS ====================

    def animate_confetti(self, canvas, particles):
        if not canvas.winfo_exists():
            return

        width = max(canvas.winfo_width(), 850)
        height = max(canvas.winfo_height(), 680)

        for particle, speed, drift in particles:
            canvas.move(particle, drift, speed)
            coords = canvas.coords(particle)

            if not coords:
                continue

            x1, y1, x2, y2 = coords

            if y1 > height:
                x = random.randint(0, width)
                size = max(x2 - x1, 4)
                canvas.coords(
                    particle, x, -10, x + size, -10 + size
                )

            elif x1 > width:
                canvas.move(particle, -width, 0)

            elif x2 < 0:
                canvas.move(particle, width, 0)

        canvas.after(
            30,
            lambda: self.animate_confetti(canvas, particles)
        )

    def pulse_title(self, label, colors, index=0):
        if not label.winfo_exists():
            return

        label.config(fg=colors[index % len(colors)])

        label.after(
            350,
            lambda: self.pulse_title(
                label, colors, index + 1
            )
        )

    # ==================== PAGE 4: RESULT ====================

    def show_result(self, won):
        self.clear()

        confetti = tk.Canvas(
            self.root,
            bg=BG,
            highlightthickness=0
        )
        confetti.place(relwidth=1, relheight=1)

        self.root.update_idletasks()

        width = max(self.root.winfo_width(), 850)
        height = max(self.root.winfo_height(), 680)

        particles = []

        for _ in range(150):
            x = random.randint(0, width)
            y = random.randint(0, height)
            size = random.randint(4, 9)

            color = random.choice(
                [PURPLE, PINK, CYAN, YELLOW, GREEN]
            )

            particle = confetti.create_oval(
                x, y, x + size, y + size,
                fill=color,
                outline=color
            )

            particles.append((
                particle,
                random.uniform(2, 6),
                random.uniform(-1.5, 1.5)
            ))

        self.animate_confetti(confetti, particles)

        panel = tk.Frame(self.root, bg=BG)
        panel.place(relx=0.5, rely=0.48, anchor="center")

        if won:
            heading = "✦ LEVEL COMPLETED! ✦"
            color = GREEN
            subtitle = "Amazing! You guessed the hidden word."
        else:
            heading = "GAME OVER!"
            color = PINK
            subtitle = "Keep practising. You can do it!"

        heading_label = tk.Label(
            panel,
            text=heading,
            font=("Segoe UI", 29, "bold"),
            bg=BG,
            fg=color
        )
        heading_label.pack(pady=12)

        if won:
            self.pulse_title(
                heading_label,
                [GREEN, CYAN, YELLOW, PINK, PURPLE]
            )
        else:
            self.pulse_title(
                heading_label,
                [PINK, RED, YELLOW, PURPLE]
            )

        tk.Label(
            panel,
            text=subtitle,
            font=("Segoe UI", 13, "bold"),
            bg=BG,
            fg=WHITE
        ).pack(pady=6)

        tk.Label(
            panel,
            text=f"THE WORD WAS: {self.word}",
            font=("Segoe UI", 18, "bold"),
            bg=BG,
            fg=CYAN
        ).pack(pady=12)

        tk.Label(
            panel,
            text=(
                f"🏆 WINS: {self.total_wins}     "
                f"✖ LOSSES: {self.total_losses}\n"
                f"🔥 STREAK: {self.streak}"
            ),
            font=("Segoe UI", 12, "bold"),
            bg=BG,
            fg=YELLOW
        ).pack(pady=10)

        if won:
            self.level += 1

            self.button(
                panel,
                "★   NEXT LEVEL",
                self.start_game,
                PURPLE,
                24
            ).pack(pady=8)

        self.button(
            panel,
            "↻   PLAY AGAIN",
            self.start_game,
            "#56358C",
            24
        ).pack(pady=8)

        self.button(
            panel,
            "⌂   HOME",
            self.show_welcome,
            "#30204B",
            24
        ).pack(pady=8)


# ==================== RUN THE GAME ====================

if __name__ == "__main__":
    root = tk.Tk()
    app = HangmanApp(root)
    root.mainloop()