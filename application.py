import tkinter as tk
from threading import Thread
from tkinter import ttk

from simulation import Simulation
from simulation.world import Position

DEFAULT_SPEED = 5
DEFAULT_ALGORITHM = 'CA*'


class Application(tk.Frame):
    UPDATE_FREQUENCY: int = 60
    simulation: Simulation

    def __init__(self, root, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)
        self.root = root
        self.root.title("Application")
        self.root.resizable(False, False)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.grid(column=0, row=0, padx=5, pady=5, sticky='nsew')
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)

        self.main = ttk.Frame(self)
        self.main.grid(column=0, row=0, sticky='nsew')

        self.side = Side(self, text='Controls:', padding=5)
        self.side.grid(column=1, row=0, padx=5, pady=5, sticky='nsew')

        self.initalise_simulation()

        self.mainloop()

    def initalise_simulation(self):
        self.simulation = Simulation(speed=self.side.speedval.get(),
                                     algorithm=self.side.selectedAlgorithm.get())

        self.canvas = Grid(self.main, self.simulation)
        self.canvas.grid(column=0, row=0, sticky='nsew')

        self.side.task_list.update()

        self.thread = Thread(target=self.simulation.run, daemon=True)
        self.thread.start()

    def reset(self):
        print('Reset')
        self.simulation.paused = True
        self.initalise_simulation()
        self.side.buttonStart.configure(state='enabled')
        self.side.buttonStep.configure(state='enabled')

    def start(self):
        print('Start')
        self.simulation.paused = False
        self.side.buttonStart.configure(state='disabled')
        self.side.buttonStep.configure(state='disabled')

    def step(self):
        print('Step')
        self.simulation.step()

    def stop(self):
        print('Stop')
        self.simulation.paused = True
        self.side.buttonStart.configure(state='enabled')
        self.side.buttonStep.configure(state='enabled')

    def mainloop(self):
        self.canvas.update()
        self.side.update()
        self.side.task_list.update()

        self.after(self.UPDATE_FREQUENCY, self.mainloop)


class Side(ttk.Labelframe):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent

        self.buttonReset = ttk.Button(self, text='Reset', command=self.parent.reset)
        self.buttonReset.grid(column=0, row=0)

        ttk.Separator(self, orient='horizontal').grid(column=0, row=1, pady=5, sticky='nsew')

        self.buttonStart = ttk.Button(self, text='Start', command=self.parent.start)
        self.buttonStart.grid(column=0, row=2)

        self.buttonStep = ttk.Button(self, text='Step', command=self.parent.step)
        self.buttonStep.grid(column=0, row=3)

        self.buttonStop = ttk.Button(self, text='Stop', command=self.parent.stop)
        self.buttonStop.grid(column=0, row=4)

        self.speedPicker = ttk.Frame(self)
        self.speedPicker.grid(column=0, row=5, pady=5)

        ttk.Label(self.speedPicker, text='Speed').grid(column=0, row=0)

        def updatespeed(*_):
            self.parent.simulation.speed = self.speedval.get()

        self.speedval = tk.IntVar(value=DEFAULT_SPEED)
        self.speedval.trace('w', updatespeed)

        self.spinboxSpeed = ttk.Spinbox(self.speedPicker, from_=1,
                                        to=5, textvariable=self.speedval, width=2)
        self.spinboxSpeed.grid(column=1, row=0)

        ttk.Separator(self, orient='horizontal').grid(column=0, row=15, pady=5, sticky='nsew')

        ttk.Label(self, text='Path Finding Algorithm \n (requires reset)').grid(column=0, row=16)

        self.selectedAlgorithm = tk.StringVar(value=DEFAULT_ALGORITHM)
        r1 = ttk.Radiobutton(self, text='Algorithm CA*', value='CA*',
                             variable=self.selectedAlgorithm)
        r1.grid(column=0, row=17, sticky='w')
        r2 = ttk.Radiobutton(self, text='Algorithm HCA*', value='HCA*',
                             variable=self.selectedAlgorithm)
        r2.grid(column=0, row=18, sticky='w')
        r3 = ttk.Radiobutton(self, text='Algorithm WHCA*', value='WHCA*',
                             variable=self.selectedAlgorithm)
        r3.grid(column=0, row=19, sticky='w')
        r4 = ttk.Radiobutton(self, text='Algorithm WCA*', value='WCA*',
                             variable=self.selectedAlgorithm)
        r4.grid(column=0, row=20, sticky='w')

        ttk.Separator(self, orient='horizontal').grid(column=0, row=30, pady=5, sticky='nsew')

        self.time_variable = tk.StringVar()
        self.time_variable.set(f'Time: 0')
        self.labelTime = ttk.Label(self, textvariable=self.time_variable)
        self.labelTime.grid(column=0, row=32, sticky='ew')

        self.var_makespan = tk.StringVar()
        self.var_makespan.set(f'Makespan = 0')
        self.label_makespan = ttk.Label(self, textvariable=self.var_makespan)
        self.label_makespan.grid(column=0, row=33, sticky='ew')

        self.var_sumcosts = tk.StringVar()
        self.var_sumcosts.set(f'Sum of Costs = 0')
        self.label_sumcosts = ttk.Label(self, textvariable=self.var_sumcosts)
        self.label_sumcosts.grid(column=0, row=34, sticky='ew')

        ttk.Separator(self, orient='horizontal').grid(column=0, row=40, pady=5, sticky='nsew')

        self.var_tasks = tk.StringVar()
        self.var_tasks.set(f'Tasks remaining 0/0')
        self.label_tasks = ttk.Label(self, textvariable=self.var_tasks)
        self.label_tasks.grid(column=0, row=41, sticky='ew')

        self.task_list = TaskList(self)
        self.task_list.grid(column=0, row=42, sticky='s')
        self.rowconfigure(42, weight=1)

    def update(self) -> None:
        self.time_variable.set(f'Time: {self.parent.simulation.time}')
        self.var_makespan.set(f'Makespan = {max(self.parent.simulation.costs.values())}')
        self.var_sumcosts.set(f'Sum of Costs = {sum(self.parent.simulation.costs.values())}')
        self.var_tasks.set(
            f'Tasks remaining {len(list(self.parent.simulation.taskmanager.incomplete))}/{len(self.parent.simulation.taskmanager.tasks)}')


class TaskList(ttk.Treeview):
    def __init__(self, parent):
        super().__init__(parent, columns=('task', 'goal'), selectmode='none')
        self.parent = parent

        self.column('#0', width=40, stretch=False, anchor='center')
        self.heading('#0', text='Agent')
        self.column('task', width=40, stretch=False, anchor='center')
        self.heading('task', text='Task')
        self.column('goal', width=50, stretch=False, anchor='center')
        self.heading('goal', text='Goal')
        self.bind('<Button-1>', lambda e: 'break')
        self.bind('<Motion>', lambda e: 'break')

    def update(self):
        self.delete(*self.get_children())
        for agent in self.parent.parent.simulation.agents:
            self.insert('', 'end', text=str(agent.id), values=(
                str(getattr(getattr(agent, 'task', None), 'id', None)),
                str(getattr(agent, 'goal', None))))


class Grid(tk.Canvas):
    COLORS: list = ['red', 'green', 'blue', 'cyan', 'yellow', 'magenta']
    CELL_SIZE: int = 50
    MARGIN: int = 2
    AGENT_SIZE: int = 40
    TEXT_SIZE: int = 8
    simulation: Simulation

    def __init__(self, parent, simulation: Simulation):
        self.simulation = simulation

        # Calculate size of canvas based on world size
        (size_x, size_y) = self.simulation.world.size

        if size_x > 30 or size_y > 30:
            self.CELL_SIZE = 25
            self.AGENT_SIZE = 20
            self.TEXT_SIZE = 4

        grid_width = self.scale(size_x + 1)
        grid_height = self.scale(size_y + 1)

        super().__init__(parent, width=grid_width, height=grid_height)

        # Draw grid
        for i in range(size_x + 1):
            for j in range(size_y + 1):
                self.create_rectangle(self.scale(i), self.scale(j),
                                      self.scale(i) + self.CELL_SIZE,
                                      self.scale(j) + self.CELL_SIZE,
                                      fill='' if self.simulation.world.passable(Position(i, j)) else 'black')
                self.create_text((self.scale(i)+1, self.scale(j)),
                                 text=f'({i}, {j})', anchor='nw', font=('TkDefaultFont', self.TEXT_SIZE),
                                 fill='black' if self.simulation.world.passable(Position(i, j)) else 'white')

        # Draw agents, paths and goals
        for agent in self.simulation.agents:
            color = self.COLORS[agent.id % len(self.COLORS)]
            # Agent goal
            self.create_oval(0, 0, 0, 0, tags=['goal', f'goal-{agent.id}'])
            self.create_text(0, 0, tags=['goal', f'goal-text-{agent.id}'], text=f'{agent.id}')
            # Agent path
            self.create_line(0, 0, 0, 0,
                             tags=f'line-{agent.id}', fill=color, width=5)
            # Agent position
            (x, y) = agent.position
            self.create_oval(self.scale(x) + (self.CELL_SIZE - self.AGENT_SIZE),
                             self.scale(y) + (self.CELL_SIZE - self.AGENT_SIZE),
                             self.scale(x) + self.AGENT_SIZE,
                             self.scale(y) + self.AGENT_SIZE,
                             tags=['agent', f'agent-{agent.id}'], fill=color)
            self.create_text(self.scale(x) + (self.CELL_SIZE / 2),
                             self.scale(y) + (self.CELL_SIZE / 2),
                             tags=['agent', f'agent-text-{agent.id}'], text=f'{agent.id}')

    def update(self):
        # Update position of agents, paths and goals
        for agent in self.simulation.agents:
            # Update agent position
            (x, y) = agent.position
            self.coords(f'agent-{agent.id}',
                        self.scale(x) + (self.CELL_SIZE - self.AGENT_SIZE),
                        self.scale(y) + (self.CELL_SIZE - self.AGENT_SIZE),
                        self.scale(x) + self.AGENT_SIZE,
                        self.scale(y) + self.AGENT_SIZE)
            self.coords(f'agent-text-{agent.id}',
                        self.scale(x) + (self.CELL_SIZE / 2),
                        self.scale(y) + (self.CELL_SIZE / 2))

            # Update path line
            if agent.path:
                self.itemconfigure(f'line-{agent.id}', state='normal')
                self.coords(f'line-{agent.id}',
                            *[self.scale(item) + (self.CELL_SIZE / 2)
                              for sublist in [agent.position] + [p[1] for p in agent.path]
                              for item in sublist])
            else:
                # Hide if no current path
                self.itemconfigure(f'line-{agent.id}', state='hidden')

            # Update goal position
            if agent.goal:
                self.itemconfigure(f'goal-{agent.id}', state='normal')
                self.itemconfigure(f'goal-text-{agent.id}', state='normal')
                (x, y) = agent.goal
                self.coords(f'goal-{agent.id}',
                            self.scale(x) + (self.CELL_SIZE - self.AGENT_SIZE),
                            self.scale(y) + (self.CELL_SIZE - self.AGENT_SIZE),
                            self.scale(x) + self.AGENT_SIZE,
                            self.scale(y) + self.AGENT_SIZE)
                self.coords(f'goal-text-{agent.id}',
                            self.scale(x) + (self.CELL_SIZE / 2),
                            self.scale(y) + (self.CELL_SIZE / 2))
            else:
                # Hide if no current goal
                self.itemconfigure(f'goal-{agent.id}', state='hidden')
                self.itemconfigure(f'goal-text-{agent.id}', state='normal')

        self.tag_raise('goal')
        self.tag_raise('agent')

    def scale(self, n: int):
        # Scale grid coordinates to canvas coordinates
        return (n * self.CELL_SIZE) + self.MARGIN


if __name__ == "__main__":
    root = tk.Tk()
    Application(root)
    root.mainloop()
