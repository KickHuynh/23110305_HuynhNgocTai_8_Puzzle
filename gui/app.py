import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading
import random
from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.ucs import ucs
from algorithms.ids import ids
from algorithms.greedy import greedy
from algorithms.a_star import a_star
from algorithms.ida_star import ida_star
from algorithms.simple_hill_climbing import simple_hill_climbing
from algorithms.steepest_ascent_hill_climbing import steepest_ascent_hill_climbing
from algorithms.stochastic_hill_climbing import stochastic_hill_climbing
from algorithms.simulated_annealing import simulated_annealing
from algorithms.beam_search import beam_search
from algorithms.and_or_search import and_or_search # Assuming this is the module
from algorithms.genetic_algorithm import genetic_algorithm
# Import GOAL_STATE and and_or_search_path from belief_runner
from gui.belief_runner import test_beliefs, GOAL_STATE as BELIEF_MODE_GOAL_STATE, and_or_search_path
from algorithms.belief_state_search import belief_state_search
from algorithms.partially_observable_search import partially_observable_search
from algorithms.q_learning import q_learning_train, q_learning_solve
from algorithms.backtracking import forward_checking_search, is_solvable


# Thay đổi trạng thái đầu vào thành trạng thái có thể giải được
INITIAL_STATE = ((1, 2, 3),
                (5, 0, 6),
                (4, 7, 8))

# Các trạng thái niềm tin (CHỈ CÒN 2)
BELIEF_STATES = [
    ((1, 2, 3), (4, 5, 6), (0, 7, 8)), # Belief State 1
    # ((1, 2, 3), (4, 5, 6), (7, 0, 8)), # Middle one removed
    ((1, 2, 3), (4, 0, 6), (7, 5, 8)), # Belief State 2 (was 3)
]
NUM_BELIEF_DISPLAYS = len(BELIEF_STATES) # Should be 2

# Goal state for normal mode (can be same as BELIEF_MODE_GOAL_STATE if desired)
NORMAL_MODE_GOAL_STATE = (
    (1, 2, 3),
    (4, 5, 6),
    (7, 8, 0)
)

class PuzzleApp:
    def __init__(self, root):
        self.root = root
        self.root.title('BÀI TOÁN 8-PUZZLE')
        self.root.geometry('1000x750')
        self.root.configure(bg='#ffe0f0')

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()

        self.algorithm_var = tk.StringVar(value='BFS')
        self.mode_var = tk.StringVar(value='Normal')
        self.mode_var.trace_add('write', self.on_mode_change)
        
        self.tiles = []
        self.move_count = 0
        self.start_time = 0
        self.time_results = {}
        self.is_solving = False
        self.pause_event = threading.Event()
        self.pause_event.set()
        self.steps = [] # For normal mode
        self.belief_steps = [] # For belief mode, list of paths
        self.current_step_index = 0
        self.speed = tk.DoubleVar(value=0.5)
        self.puzzle_state = INITIAL_STATE
        self.current_initial_state = INITIAL_STATE


        self.algorithms = {
            "BFS": bfs,
            "DFS": dfs,
            "UCS": ucs,
            "IDS": ids,
            "Greedy": greedy,
            "A*": a_star, 
            "IDA*": ida_star,
            "Simple Hill Climbing": simple_hill_climbing,
            "Steepest Ascent Hill Climbing": steepest_ascent_hill_climbing,
            "Stochastic Hill Climbing": stochastic_hill_climbing,
            "Simulated Annealing": simulated_annealing,
            "Beam Search": beam_search,
            "And-Or Search": and_or_search_path, # Use the wrapper from belief_runner
            "Belief State Search": belief_state_search,
            "Partially Observable Search": partially_observable_search,
            "Genetic Algorithm": genetic_algorithm,
            "CSP Forward Checking": lambda initial, goal: forward_checking_search(goal, is_solvable)[0],
            "Q-Learning": q_learning_solve
        }

        self.create_widgets() 
        self.reset_board()   


    def configure_styles(self):
        self.style.configure('TFrame', background='#F5F7FA')
        self.style.configure('Header.TLabel', background='#F5F7FA', foreground='#3498DB', font=('Helvetica', 24, 'bold'), padding=20)
        self.style.configure('Title.TLabel', font=('Helvetica', 14, 'bold'), background='#F5F7FA', foreground='#2C3E50')
        self.style.configure('Board.TFrame', background='#FFFFFF', relief='solid', borderwidth=2)
        self.style.configure('Tile.TLabel', font=('Helvetica', 24, 'bold'), background='#4A90E2', foreground='white', width=3, padding=15, relief='raised', borderwidth=1)
        self.style.configure('Empty.TLabel', background='#DDE6ED', relief='sunken', width=4, padding=20, borderwidth=1)
        self.style.configure('TRadiobutton', font=('Helvetica', 11), background='#F5F7FA', foreground='#2C3E50')
        self.style.configure('TButton', font=('Helvetica', 12, 'bold'), padding=8)
        self.style.map('TButton', foreground=[('active', 'white'), ('!active', 'white')], background=[('active', '#2980B9'), ('!active', '#3498DB')])
        self.style.configure('Time.TLabel', font=('Helvetica', 13, 'bold'), foreground='#2980B9', background='#F5F7FA')
        self.style.configure('TScale', troughcolor='#cce5ff', background='#3498DB')

    def create_widgets(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = int(screen_width * 0.9)
        window_height = int(screen_height * 0.9)
        self.root.geometry(f"{window_width}x{window_height}")

        header = ttk.Frame(self.root)
        header.pack(fill=tk.X, pady=(10, 0))
        ttk.Label(header, text='BÀI TOÁN 8 - PUZZLE', style='Header.TLabel').pack(anchor='center')

        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        main_container.columnconfigure(0, weight=1)
        main_container.columnconfigure(1, weight=3) # Middle panel gets more space
        main_container.columnconfigure(2, weight=1)

        panel_width = 250

        left_panel = ttk.Frame(main_container, width=panel_width)
        left_panel.grid(row=0, column=0, sticky='nsew')
        left_panel.grid_propagate(False)

        ttk.Label(left_panel, text='Thuật toán:', style='Title.TLabel').pack(anchor=tk.W, padx=10, pady=(10, 5))
        self.algo_combobox = ttk.Combobox(
            left_panel,
            values=list(self.algorithms.keys()),
            textvariable=self.algorithm_var,
            state="readonly"
        )
        self.algo_combobox.pack(fill=tk.X, padx=10, pady=(0, 10))
        self.algo_combobox.current(0)
        
        ttk.Label(left_panel, text='Running Mode:', style='Title.TLabel').pack(anchor=tk.W, padx=10, pady=(10, 0))
        ttk.Radiobutton(left_panel, text='Normal', variable=self.mode_var, value='Normal').pack(anchor=tk.W, padx=20)
        ttk.Radiobutton(left_panel, text='Belief', variable=self.mode_var, value='Belief').pack(anchor=tk.W, padx=20)

        for text, cmd in [
            ('Solve Puzzle', self.start_solving),
            ('Train Q-learning', self.train_q_learning),
            ('Random Board', self.set_random_state),
            ('Create Board', self.create_custom_board),
            ('Reset Board', self.reset_board),
            ('Export Step', self.export_steps)
        ]:
            ttk.Button(left_panel, text=text, command=cmd).pack(fill=tk.X, padx=10, pady=4)

        ttk.Label(left_panel, text="Speed (s/step):", font=("Arial", 15, "bold")).pack(pady=(20, 5))
        self.speed_value_label = ttk.Label(left_panel, text=f"{self.speed.get():.1f} s/step")
        self.speed_value_label.pack(pady=(0, 5))
        self.speed_scale = ttk.Scale(
            left_panel, from_=0.1, to=2.0, orient=tk.HORIZONTAL,
            variable=self.speed, length=panel_width - 40, style="TScale",
            command=lambda val: self.speed_value_label.config(text=f"{float(val):.1f} s/step")
        )
        self.speed_scale.pack(pady=(0, 10))

        right_panel = ttk.Frame(main_container, width=panel_width)
        right_panel.grid(row=0, column=2, sticky='nsew')
        right_panel.grid_propagate(False)
        ttk.Label(right_panel, text='Timing:', style='Title.TLabel').pack(anchor=tk.W, padx=10, pady=(5, 0))
        self.time_display = ttk.Label(right_panel, text='0.0000 seconds', style='Time.TLabel')
        self.time_display.pack(anchor=tk.W, padx=10, pady=(0, 10))

        ttk.Label(right_panel, text='Step:', style='Title.TLabel').pack(anchor=tk.W, padx=10, pady=(0, 5))
        self.steps_frame = ttk.Frame(right_panel, height=200)
        self.steps_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.steps_frame.pack_propagate(False)
        self.steps_scroll = ttk.Scrollbar(self.steps_frame)
        self.steps_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.steps_display = tk.Text(
            self.steps_frame, height=10, width=30, font=('Consolas', 11),
            wrap=tk.WORD, yscrollcommand=self.steps_scroll.set, bg='#FFFFFF', fg='#2C3E50'
        )
        self.steps_display.pack(fill=tk.BOTH, expand=True)
        self.steps_scroll.config(command=self.steps_display.yview)

        for text, command in [
            ('← Previous', self.previous_step), ('→ Next', self.next_step),
            ('⏹ Stop', self.stop_solving), ('▶ Resume', self.resume_solving)
        ]:
            ttk.Button(right_panel, text=text, command=command, style='TButton').pack(fill=tk.X, padx=10, pady=3)

        middle_panel = ttk.Frame(main_container)
        middle_panel.grid(row=0, column=1, sticky='nsew')
        # Configure middle_panel columns for belief mode layout
        middle_panel.columnconfigure(0, weight=1) # Left belief/goal
        middle_panel.columnconfigure(1, weight=1) # Right belief


        self.normal_board_frame = ttk.Frame(middle_panel)
        # self.normal_board_frame.pack(pady=10) # Will be managed by grid
        # Normal mode uses grid within its own frame which is then packed
        self.normal_board_frame.grid(row=0, column=0, columnspan=2, sticky='nsew')


        state_label_frame = ttk.Frame(self.normal_board_frame)
        state_label_frame.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        ttk.Label(state_label_frame, text='Initial State', style='Title.TLabel').grid(row=0, column=0, padx=15)
        ttk.Label(state_label_frame, text='Goal State', style='Title.TLabel').grid(row=0, column=1, padx=15)
        self.initial_frame = ttk.Frame(self.normal_board_frame)
        self.initial_frame.grid(row=1, column=0, padx=15)
        self.goal_frame = ttk.Frame(self.normal_board_frame)
        self.goal_frame.grid(row=1, column=1, padx=15)
        current_frame_normal = ttk.Frame(self.normal_board_frame)
        current_frame_normal.grid(row=2, column=0, columnspan=2, pady=(30, 0))
        ttk.Label(current_frame_normal, text='Current State', style='Title.TLabel').pack(pady=5)
        self.step_label = ttk.Label(current_frame_normal, text='Step 0 of 0', style='Title.TLabel')
        self.step_label.pack()
        self.board_container = ttk.Frame(current_frame_normal)
        self.board_container.pack()
        for i in range(3):
            row_tiles = []
            for j in range(3):
                label = ttk.Label(self.board_container, style='Tile.TLabel', anchor='center')
                label.grid(row=i, column=j, padx=2, pady=2)
                row_tiles.append(label)
            self.tiles.append(row_tiles)

        # Frame cho chế độ niềm tin - will use grid directly in middle_panel
        self.belief_board_frame = ttk.Frame(middle_panel)
        # self.belief_board_frame.pack_forget() # Managed by grid_remove/grid
        self.belief_board_frame.grid(row=0, column=0, columnspan=2, sticky='nsew')


        # Container for initial belief states (top row, 2 states)
        init_states_outer_frame = ttk.Frame(self.belief_board_frame)
        init_states_outer_frame.pack(pady=10, fill=tk.X)
        ttk.Label(init_states_outer_frame, text='Initial Belief States', style='Title.TLabel').pack(pady=5)
        
        self.belief_init_frames = []
        # This container will hold the 2 initial belief state frames side-by-side
        init_states_container = ttk.Frame(init_states_outer_frame)
        init_states_container.pack() # Will use grid for its children

        for i in range(NUM_BELIEF_DISPLAYS): # Loop for 2 belief states
            frame = ttk.Frame(init_states_container)
            # Place them side-by-side in init_states_container
            frame.grid(row=0, column=i, padx=20, pady=5, sticky='n') 
            init_states_container.columnconfigure(i, weight=1) # Make columns expand

            ttk.Label(frame, text=f'Belief {i+1}', style='Title.TLabel').pack(pady=2)
            board_frame = ttk.Frame(frame)
            board_frame.pack()
            self.belief_init_frames.append(board_frame)
        

        # Container for goal state and current belief states (bottom row)
        # This will be a 2-column layout: Goal on left, Current Beliefs on right
        bottom_belief_area_frame = ttk.Frame(self.belief_board_frame)
        bottom_belief_area_frame.pack(pady=10, fill=tk.X, expand=True)
        bottom_belief_area_frame.columnconfigure(0, weight=1) # Goal State
        bottom_belief_area_frame.columnconfigure(1, weight=1) # Current Belief States (which has 2 sub-frames)

        # Goal state (bottom left)
        goal_frame_belief = ttk.Frame(bottom_belief_area_frame)
        goal_frame_belief.grid(row=0, column=0, padx=10, pady=5, sticky='n')
        ttk.Label(goal_frame_belief, text='Goal State', style='Title.TLabel').pack(pady=5)
        self.belief_goal_frame = ttk.Frame(goal_frame_belief)
        self.belief_goal_frame.pack()

        # Current belief states (bottom right, containing 2 boards)
        current_belief_outer_frame = ttk.Frame(bottom_belief_area_frame)
        current_belief_outer_frame.grid(row=0, column=1, padx=10, pady=5, sticky='n')
        ttk.Label(current_belief_outer_frame, text='Current Belief States', style='Title.TLabel').pack(pady=5)
        self.belief_step_label = ttk.Label(current_belief_outer_frame, text='Step 0 of 0', style='Title.TLabel')
        self.belief_step_label.pack()

        self.belief_current_frames = []
        # This container will hold the 2 current belief state frames side-by-side
        current_belief_display_container = ttk.Frame(current_belief_outer_frame)
        current_belief_display_container.pack() # Will use grid for its children

        for i in range(NUM_BELIEF_DISPLAYS): # Loop for 2 belief states
            frame = ttk.Frame(current_belief_display_container)
            # Place them side-by-side
            frame.grid(row=0, column=i, padx=10, pady=5, sticky='n')
            current_belief_display_container.columnconfigure(i, weight=1)

            # No individual "Current State i+1" label needed if parent has "Current Belief States"
            board_frame = ttk.Frame(frame)
            board_frame.pack()
            self.belief_current_frames.append(board_frame)

        # Initially hide one of the frames based on mode
        self.on_mode_change()


    def create_custom_board(self):
        popup = tk.Toplevel(self.root)
        popup.title("Nhập trạng thái 8-puzzle")
        entries = []
        for i in range(3):
            row_entries = []
            for j in range(3):
                e = ttk.Entry(popup, width=3, font=('Helvetica', 18))
                e.grid(row=i, column=j, padx=5, pady=5)
                row_entries.append(e)
            entries.append(row_entries)

        def submit():
            try:
                state_list = []
                nums = []
                for r_idx in range(3):
                    row_list = []
                    for c_idx in range(3):
                        val_str = entries[r_idx][c_idx].get()
                        if not val_str:
                             messagebox.showerror("Lỗi", "Vui lòng nhập đủ các ô.")
                             return
                        val = int(val_str)
                        row_list.append(val)
                        nums.append(val)
                    state_list.append(tuple(row_list))
                
                if sorted(nums) != list(range(9)):
                    messagebox.showerror("Lỗi", "Nhập đủ các số từ 0 đến 8, không trùng lặp.")
                    return
                
                custom_state = tuple(state_list)
                if not self.is_solvable(custom_state):
                    messagebox.showerror("Lỗi", "Trạng thái này không giải được. Vui lòng nhập trạng thái khác.")
                    return

                self.current_initial_state = custom_state
                self.puzzle_state = self.current_initial_state
                self.reset_board() 
                popup.destroy()
            except ValueError:
                messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ (0-8) cho từng ô.")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {e}")
        ttk.Button(popup, text="OK", command=submit).grid(row=3, column=0, columnspan=3, pady=10)

    def update_board(self, state): 
        for i in range(3):
            for j in range(3):
                value = state[i][j]
                label = self.tiles[i][j]
                if value in (0, None, -1): 
                    label.config(text='', style='Empty.TLabel')
                else:
                    label.config(text=str(value), style='Tile.TLabel')
        
        if self.mode_var.get() == 'Normal' and self.steps:
            step_text = f"Step {self.current_step_index} of {len(self.steps)}" 
            self.step_label.config(text=step_text)
       
    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def draw_static_board(self, parent_frame, state):
        self.clear_frame(parent_frame) 
        board_frame = ttk.Frame(parent_frame, style='Board.TFrame')
        board_frame.pack(padx=5, pady=5)
        for r, row_data in enumerate(state):
            for c, value in enumerate(row_data):
                style = 'Empty.TLabel' if value in (0, None, -1) else 'Tile.TLabel'
                text = '' if value == 0 else str(value)
                tile = ttk.Label(board_frame, text=text, style=style, anchor='center')
                tile.grid(row=r, column=c, padx=1, pady=1, sticky='nsew')
        for i in range(3): 
            board_frame.grid_columnconfigure(i, weight=1, minsize=40) 
            board_frame.grid_rowconfigure(i, weight=1, minsize=40)

    def start_solving(self):
        if self.is_solving:
            messagebox.showinfo("Info", "Solver is already running.")
            return
            
        self.puzzle_state = self.current_initial_state 
        
        self.steps = []
        self.belief_steps = []
        self.current_step_index = 0 
        self.steps_display.delete('1.0', tk.END)
        self.time_display.config(text='Solving...')
        self.step_label.config(text='Step 0 of 0')
        self.belief_step_label.config(text='Step 0 of 0')
        
        self.is_solving = True
        self.pause_event.set() 
        threading.Thread(target=self.solve, daemon=True).start()

    def is_valid(self, state):
        if not isinstance(state, tuple) or len(state) != 3: return False
        flat = []
        for row in state:
            if not isinstance(row, tuple) or len(row) != 3: return False
            flat.extend(row)
        return sorted(flat) == list(range(9))
    
    def is_solvable(self, state):
        flat_state = [item for sublist in state for item in sublist if item != 0]
        inversions = 0
        for i in range(len(flat_state)):
            for j in range(i + 1, len(flat_state)):
                if flat_state[i] > flat_state[j]:
                    inversions += 1
        return inversions % 2 == 0

    def solve(self):
        try:
            algorithm_name = self.algorithm_var.get()
            algorithm_function = self.algorithms.get(algorithm_name)

            if not algorithm_function:
                messagebox.showerror('Error', f'Algorithm "{algorithm_name}" not found')
                self.is_solving = False
                return

            self.start_time = time.time()

            if self.mode_var.get() == 'Belief':
                print(f"Solving Belief States with {algorithm_name} towards {BELIEF_MODE_GOAL_STATE}")
                # Ensure BELIEF_STATES (now 2) is passed
                self.belief_steps = test_beliefs(BELIEF_STATES, BELIEF_MODE_GOAL_STATE, algorithm_function)
                elapsed_time = time.time() - self.start_time
                self.time_display.config(text=f'{elapsed_time:.4f} s')
                
                if not any(self.belief_steps): 
                    messagebox.showinfo('Info', f'{algorithm_name} found no solution for any belief state.')
                
                self.current_step_index = 0 
                self.root.after(0, self.play_belief_steps) 
            
            else: 
                initial_state = self.get_puzzle_state() 
                print(f"Solving Normal State: {initial_state} with {algorithm_name} towards {NORMAL_MODE_GOAL_STATE}")

                if not initial_state or not self.is_valid(initial_state):
                    messagebox.showerror("Lỗi", "Trạng thái đầu vào không hợp lệ.")
                    self.is_solving = False
                    return

                if not self.is_solvable(initial_state) and algorithm_name not in ["CSP Forward Checking"]: 
                    messagebox.showerror("Lỗi", "Trạng thái đầu vào không giải được.")
                    self.is_solving = False
                    return

                result = algorithm_function(initial_state, NORMAL_MODE_GOAL_STATE)
                elapsed_time = time.time() - self.start_time
                self.time_display.config(text=f'{elapsed_time:.4f} s')

                # Xử lý riêng cho Genetic Algorithm (trả về tuple)
                if (algorithm_name == "Genetic Algorithm" or algorithm_name == "Simulated Annealing"):
                    if result is None or not result or result[0] is None:
                        messagebox.showinfo('Info', f'{algorithm_name} không tìm thấy lời giải.')
                        self.steps = []
                    else:
                        self.steps = result[0]  # Lấy path
                        self.current_step_index = 0 
                        self.steps_display.delete('1.0', tk.END)
                        self.root.after(0, self.play_from_current)
                else:
                    if result is None or not result:
                        messagebox.showinfo('Info', f'{algorithm_name} không tìm thấy lời giải.')
                        self.steps = []
                    else:
                        self.steps = result
                        self.current_step_index = 0 
                        self.steps_display.delete('1.0', tk.END)
                        self.root.after(0, self.play_from_current) 
        except Exception as e:
            messagebox.showerror("Giải lỗi", f"Lỗi xảy ra trong quá trình giải: {e}")
            print(f"Error during solve: {e}")
            import traceback
            traceback.print_exc()
        finally:
            if not (self.steps or any(bs for bs in self.belief_steps if bs)): 
                 self.is_solving = False 

    def get_puzzle_state(self):
        return self.current_initial_state 

    def stop_solving(self):
        self.is_solving = False
        self.pause_event.set() 

    def resume_solving(self):
        if not self.is_solving: 
            self.is_solving = True
            self.pause_event.set()
            if self.mode_var.get() == 'Belief':
                if self.belief_steps and any(bs for bs in self.belief_steps if bs):
                    self.root.after(0, self.play_belief_steps)
            else: 
                if self.steps:
                    self.root.after(0, self.play_from_current)
        else: 
             self.pause_event.set()


    def play_from_current(self): 
        if not self.is_solving: return
        self.pause_event.wait()
        if not self.is_solving: return 

        if self.current_step_index < len(self.steps):
            step_data = self.steps[self.current_step_index]
            self.update_board(step_data) 
            self.steps_display.insert(tk.END, f'Step {self.current_step_index + 1}: {step_data}\n')
            self.steps_display.see(tk.END)
            self.step_label.config(text=f"Step {self.current_step_index + 1} of {len(self.steps)}")
            self.current_step_index += 1
            self.root.after(int(self.speed.get() * 1000), self.play_from_current)
        else:
            self.is_solving = False
            if self.steps: 
                 self.update_board(self.steps[-1])
                 self.step_label.config(text=f"Finished: {len(self.steps)} steps")
            else:
                 self.step_label.config(text="Finished (No solution)")


    def play_belief_steps(self):
        if not self.is_solving: return
        self.pause_event.wait()
        if not self.is_solving: return

        max_len = 0
        if self.belief_steps: # self.belief_steps should have 2 lists of paths
            path_lengths = [len(p) for p in self.belief_steps if isinstance(p, list) and p]
            if path_lengths:
                max_len = max(path_lengths)
        
        if self.current_step_index < max_len :
            for i in range(NUM_BELIEF_DISPLAYS): # Loop for 2 displays
                frame = self.belief_current_frames[i]
                state_to_display = BELIEF_STATES[i] 

                if i < len(self.belief_steps): # Should always be true if belief_steps has 2 elements
                    current_path = self.belief_steps[i]
                    if isinstance(current_path, list) and current_path: 
                        if self.current_step_index < len(current_path):
                            state_to_display = current_path[self.current_step_index]
                        else: 
                            state_to_display = current_path[-1]
                
                self.draw_static_board(frame, state_to_display)
            
            self.belief_step_label.config(text=f"Step {self.current_step_index + 1} of {max_len}")
            self.steps_display.insert(tk.END, f'Belief Step {self.current_step_index + 1}\n') 
            self.steps_display.see(tk.END)
            self.current_step_index += 1
            self.root.after(int(self.speed.get() * 1000), self.play_belief_steps)
        else:
            self.is_solving = False
            for i in range(NUM_BELIEF_DISPLAYS):
                frame = self.belief_current_frames[i]
                state_to_display = BELIEF_STATES[i]
                if i < len(self.belief_steps):
                    current_path = self.belief_steps[i]
                    if isinstance(current_path, list) and current_path:
                        state_to_display = current_path[-1]
                self.draw_static_board(frame, state_to_display)
            if max_len > 0:
                self.belief_step_label.config(text=f"Finished: {max_len} steps")
            else:
                self.belief_step_label.config(text="Finished (No solution/steps)")


    def next_step(self):
        self.pause_event.set() 
        if self.mode_var.get() == 'Belief':
            max_len = 0
            if self.belief_steps:
                path_lengths = [len(p) for p in self.belief_steps if isinstance(p, list) and p]
                if path_lengths: max_len = max(path_lengths)
            
            if self.current_step_index < max_len:
                for i in range(NUM_BELIEF_DISPLAYS):
                    frame = self.belief_current_frames[i]
                    state_to_display = BELIEF_STATES[i]
                    if i < len(self.belief_steps):
                        current_path = self.belief_steps[i]
                        if isinstance(current_path, list) and current_path:
                            if self.current_step_index < len(current_path):
                                state_to_display = current_path[self.current_step_index]
                            else: state_to_display = current_path[-1]
                    self.draw_static_board(frame, state_to_display)
                self.belief_step_label.config(text=f"Step {self.current_step_index + 1} of {max_len}")
                self.current_step_index += 1
        else: 
            if self.current_step_index < len(self.steps):
                step_data = self.steps[self.current_step_index]
                self.update_board(step_data)
                self.steps_display.insert(tk.END, f'Step {self.current_step_index + 1}: {step_data}\n')
                self.steps_display.see(tk.END)
                self.step_label.config(text=f"Step {self.current_step_index + 1} of {len(self.steps)}")
                self.current_step_index += 1
        if not self.is_solving: 
            self.is_solving = False 

    def previous_step(self):
        self.pause_event.set() 
        if self.current_step_index > 0:
            self.current_step_index -= 1 
            if self.mode_var.get() == 'Belief':
                max_len = 0
                if self.belief_steps:
                    path_lengths = [len(p) for p in self.belief_steps if isinstance(p, list) and p]
                    if path_lengths: max_len = max(path_lengths)

                for i in range(NUM_BELIEF_DISPLAYS):
                    frame = self.belief_current_frames[i]
                    state_to_display = BELIEF_STATES[i]
                    if i < len(self.belief_steps):
                        current_path = self.belief_steps[i]
                        if isinstance(current_path, list) and current_path:
                            if self.current_step_index < len(current_path): 
                                state_to_display = current_path[self.current_step_index]
                    self.draw_static_board(frame, state_to_display)
                self.belief_step_label.config(text=f"Step {self.current_step_index + 1} of {max_len}")

            else: 
                if self.current_step_index < len(self.steps): 
                    step_data = self.steps[self.current_step_index]
                    self.update_board(step_data)
                    self.step_label.config(text=f"Step {self.current_step_index + 1} of {len(self.steps)}")
            if self.current_step_index == 0 and self.mode_var.get() == "Normal":
                self.update_board(self.current_initial_state) 
                self.step_label.config(text=f"Initial State (Before Step 1)")

        if not self.is_solving: self.is_solving = False 

    def reset_board(self):
        self.stop_solving() 
        self.steps = []
        self.belief_steps = []
        self.current_step_index = 0
        self.move_count = 0 

        self.puzzle_state = self.current_initial_state 
        
        self.update_puzzle_display() 
        
        self.on_mode_change() 

        self.steps_display.delete('1.0', tk.END)
        self.time_display.config(text='0.0000 seconds')
        self.step_label.config(text='Step 0 of 0')
        self.belief_step_label.config(text='Step 0 of 0')

    def export_steps(self):
        steps_text = self.steps_display.get("1.0", tk.END).strip()
        if not steps_text:
            messagebox.showinfo('Info', 'No steps to export!')
            return
        try:
            with open("steps_output.txt", "w", encoding="utf-8") as file:
                file.write(steps_text)
            messagebox.showinfo('Success', 'Steps exported to steps_output.txt')
        except Exception as e:
            messagebox.showerror('Error', f'Could not export steps: {e}')

    def generate_solvable_state(self):
        numbers = list(range(9))
        while True:
            random.shuffle(numbers)
            state = tuple(tuple(numbers[i:i+3]) for i in range(0, 9, 3))
            if self.is_solvable(state):
                return state

    def set_random_state(self):
        self.stop_solving()
        self.current_initial_state = self.generate_solvable_state()
        self.puzzle_state = self.current_initial_state
        self.reset_board() 
        messagebox.showinfo("Thông báo", f"Đã tạo trạng thái ngẫu nhiên mới: {self.current_initial_state}")

    def update_puzzle_display(self): 
        self.draw_static_board(self.initial_frame, self.current_initial_state)
        self.draw_static_board(self.goal_frame, NORMAL_MODE_GOAL_STATE)
        self.update_board(self.puzzle_state) 

    def on_mode_change(self, *args):
        self.stop_solving() 
        current_mode = self.mode_var.get()
        
        if current_mode == 'Belief':
            self.normal_board_frame.grid_remove() # Hide normal frame
            self.belief_board_frame.grid() # Show belief frame

            # Update Initial Belief States display (now 2)
            for i in range(NUM_BELIEF_DISPLAYS):
                if i < len(BELIEF_STATES) and i < len(self.belief_init_frames):
                    self.draw_static_board(self.belief_init_frames[i], BELIEF_STATES[i])
            
            self.draw_static_board(self.belief_goal_frame, BELIEF_MODE_GOAL_STATE)

            # Update Current Belief States display (now 2, show initial beliefs)
            for i in range(NUM_BELIEF_DISPLAYS):
                 if i < len(BELIEF_STATES) and i < len(self.belief_current_frames):
                    self.draw_static_board(self.belief_current_frames[i], BELIEF_STATES[i]) 
            
            self.belief_step_label.config(text='Step 0 of 0')

        else: # Normal mode
            self.belief_board_frame.grid_remove() # Hide belief frame
            self.normal_board_frame.grid() # Show normal frame
            self.update_puzzle_display() 
            self.step_label.config(text='Step 0 of 0')
        
        self.steps_display.delete('1.0', tk.END)
        self.time_display.config(text='0.0000 seconds')
        self.current_step_index = 0


    def train_q_learning(self):
        if self.is_solving:
            messagebox.showinfo("Info","Solver/Trainer is already running.")
            return

        self.is_solving = True 
        self.time_display.config(text='Training Q-Learning...')
        self.root.update_idletasks()
        initial_state_for_train = self.current_initial_state 
        threading.Thread(target=lambda: self._train_q_learning_thread(initial_state_for_train), daemon=True).start()

    def _train_q_learning_thread(self, initial_state):
        try:
            q_learning_train(initial_state, NORMAL_MODE_GOAL_STATE, episodes=1000) 
            self.root.after(0, lambda: messagebox.showinfo("Q-learning", "Training completed!"))
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Q-learning Error", f"Training failed: {e}"))
        finally:
            self.is_solving = False
            self.root.after(0, lambda: self.time_display.config(text='0.0000 seconds'))


def main():
    root = tk.Tk()
    app = PuzzleApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()