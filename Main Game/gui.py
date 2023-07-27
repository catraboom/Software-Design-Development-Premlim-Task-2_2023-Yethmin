import tkinter as tk
from tkinter import ttk
import subprocess

def start_game(opponent, root):
    if opponent == "AI":
        root.destroy()  # Close the Tkinter window
        subprocess.Popen(["python", "Main Game\Pygame\maingameai.py"])  # Path to the AI version of the game
    elif opponent == "Player":
        root.destroy()  # Close the Tkinter window
        subprocess.Popen(["python", "Main Game\Pygame\maingame2p.py"])  # Path to the 2-player version of the game 
    else:
        pass

def create_menu_screen():
    root = tk.Tk()
    root.title("Game Menu")

    # Set the size and center the window
    window_width = 400
    window_height = 400
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Load and resize the custom image background
    custom_image = tk.PhotoImage(file="Main Game\Backgrounds\DALL·E 2023-07-15 21.20.00 - digital art depicting a hexagon background with various shades of green.png")  # Custom background image
    bg_label = tk.Label(root, image=custom_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=2)  # Set the image as the background

    # Configure the style for buttons with the custom font
    style = ttk.Style()
    style.configure("Custom.TButton")
    style.map("Custom.TButton", background=[("active", "white"), ("!active", "white")], foreground=[("active", "gray"), ("!active", "black")])

    def on_opponent_selection(opponent):
        start_game(opponent, root)  # Pass the root window to the start_game function

    ai_button = ttk.Button(root, text="AI Opponent", style="Custom.TButton", width=20, command=lambda: on_opponent_selection("AI"))
    ai_button.pack(pady=10)

    player_button = ttk.Button(root, text="2 Player", style="Custom.TButton", width=20, command=lambda: on_opponent_selection("Player"))
    player_button.pack(pady=10)

    root.mainloop()

create_menu_screen()
