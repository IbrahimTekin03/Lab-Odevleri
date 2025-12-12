import tkinter as tk
import random


class Ball:
    def __init__(self, canvas, x, y, size, color, dx, dy):
        self.canvas = canvas
        self.size = size
        self.color = color
        self.dx = dx
        self.dy = dy
        self.ball = canvas.create_oval(
            x, y, x + size, y + size, fill=color, outline=color
        )

    def move(self):
        coords = self.canvas.coords(self.ball)
        x1, y1, x2, y2 = coords
        if x1 <= 0 or x2 >= self.canvas.winfo_width():
            self.dx = -self.dx
        if y1 <= 0 or y2 >= self.canvas.winfo_height():
            self.dy = -self.dy
        self.canvas.move(self.ball, self.dx, self.dy)


class BallSimulator:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, bg="lightgray", width=800, height=500)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.balls = []
        self.running = False
        self.speed = 1
        self.selected_color = "red"

        self.create_controls()

    def create_controls(self):
        control_frame = tk.Frame(self.root, bg="white")
        control_frame.pack(fill=tk.X, side=tk.BOTTOM, anchor="w")


        size_frame = tk.Frame(control_frame, bg="white")
        size_frame.pack(side=tk.TOP, pady=5, anchor="w")
        sizes = [(20, 2), (40, 4), (60, 6)]
        for size, pad in sizes:
            size_button = tk.Canvas(size_frame, width=60, height=60, bg="white", highlightthickness=0)
            size_button.create_oval(
                30 - size / 2, 30 - size / 2, 30 + size / 2, 30 + size / 2, fill="gray"
            )
            size_button.bind("<Button-1>", lambda event, s=size: self.add_ball(s))
            size_button.pack(side=tk.LEFT, padx=10)


        color_frame = tk.Frame(control_frame, bg="white")
        color_frame.pack(side=tk.TOP, pady=5, anchor="w")
        colors = ["red", "blue", "yellow"]
        for color in colors:
            color_button = tk.Button(
                color_frame,
                bg=color,
                width=4,
                height=2,
                command=lambda c=color: self.select_color(c),
            )
            color_button.pack(side=tk.LEFT, padx=10)


        action_frame = tk.Frame(control_frame, bg="white")
        action_frame.pack(side=tk.TOP, pady=5, anchor="w")  # Sola hizalama
        tk.Button(action_frame, text="START", command=self.start).pack(side=tk.LEFT, padx=5)
        tk.Button(action_frame, text="STOP", command=self.stop).pack(side=tk.LEFT, padx=5)
        tk.Button(action_frame, text="RESET", command=self.reset).pack(side=tk.LEFT, padx=5)
        tk.Button(action_frame, text="Speed Up", command=self.speed_up).pack(side=tk.LEFT, padx=5)

    def select_color(self, color):
        self.selected_color = color

    def add_ball(self, size):
        x = random.randint(0, self.canvas.winfo_width() - size)
        y = random.randint(0, self.canvas.winfo_height() - size)
        dx = random.choice([-2, 2])
        dy = random.choice([-2, 2])
        ball = Ball(self.canvas, x, y, size, self.selected_color, dx, dy)
        self.balls.append(ball)

    def move_balls(self):
        if self.running:
            for ball in self.balls:
                ball.move()
            self.root.after(int(20 / self.speed), self.move_balls)

    def start(self):
        if not self.running:
            self.running = True
            self.move_balls()

    def stop(self):
        self.running = False

    def reset(self):
        self.stop()
        for ball in self.balls:
            self.canvas.delete(ball.ball)
        self.balls.clear()

    def speed_up(self):
        self.speed += 1


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Ball Animation")
    app = BallSimulator(root)
    root.mainloop()
