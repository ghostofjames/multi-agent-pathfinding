import tkinter as tk
from tkinter import ttk
from threading import Thread

from simulation import Simulation
from world import Position


class Application(tk.Frame):
    UPDATE_FREQUENCY: int = 1

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
        self.simulation = Simulation(speed=0.25)

        self.canvas = Grid(self.main, self.simulation)
        self.canvas.grid(column=0, row=0, sticky='nsew')

        self.side.task_list.update(self.simulation.agents)

        self.thread = Thread(target=self.simulation.run, daemon=True)
        self.thread.start()

    def reset(self):
        print('Reset')
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
        self.side.time_variable.set(f'Time: {self.simulation.time}')

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

        ttk.Separator(self, orient='horizontal').grid(column=0, row=5, pady=5, sticky='nsew')

        self.time_variable = tk.StringVar()
        self.time_variable.set(f'Time: 0')
        self.labelTime = ttk.Label(self, textvariable=self.time_variable)
        self.labelTime.grid(column=0, row=6, sticky='ew')

        ttk.Separator(self, orient='horizontal').grid(column=0, row=7, pady=5, sticky='nsew')

        self.task_list = TaskList(self, columns=('start', 'end'), selectmode='none')
        self.task_list.grid(column=0, row=10, sticky='s')
        self.rowconfigure(10, weight=1)


class TaskList(ttk.Treeview):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent

        self.column('#0', width=50, stretch=False)
        self.heading('#0', text='agent')
        self.column('start', width=50, stretch=False)
        self.heading('start', text='start')
        self.column('end', width=50, stretch=False)
        self.heading('end', text='end')
        self.bind('<Button-1>', lambda e: 'break')
        self.bind('<Motion>', lambda e: 'break')

    def update(self, agents):
        self.delete(*self.get_children())
        for agent in agents:
            self.insert('', 'end', text=str(agent.id), values=(
                str(getattr(getattr(agent, 'task', None), 'start', None)),
                str(getattr(getattr(agent, 'task', None), 'end', None))))


class Grid(tk.Canvas):
    COLORS = ['red', 'green', 'blue', 'cyan', 'yellow', 'magenta',
              'red', 'green', 'blue', 'cyan', 'yellow', 'magenta']
    CELL_SIZE: int = 50
    MARGIN: int = 2
    AGENT_SIZE: int = 40
    simulation: Simulation

    def __init__(self, parent, simulation: Simulation):
        self.simulation = simulation

        super().__init__(parent,
                         width=(self.simulation.world.size[0] + 1) * self.CELL_SIZE + self.MARGIN,
                         height=(self.simulation.world.size[1] + 1) * self.CELL_SIZE + self.MARGIN)

        self.bind('<Button-1>', self.clicked)

        self.draw_grid()

        self.draw_agents()

    def draw_grid(self):
        for i in range(self.simulation.world.size[0] + 1):
            for j in range(self.simulation.world.size[1] + 1):
                self.create_rectangle(self.scale(i), self.scale(j),
                                      self.scale(i) + self.CELL_SIZE,
                                      self.scale(j) + self.CELL_SIZE,
                                      fill='' if self.simulation.world.passable(Position(i, j)) else 'black')
                self.create_text((self.scale(i)+1, self.scale(j)),
                                 text=f'({i}, {j})', anchor='nw',
                                 font=('TkDefaultFont', 8),
                                 fill='black' if self.simulation.world.passable(Position(i, j)) else 'white')

    def draw_agents(self):
        for agent in self.simulation.agents:
            x, y = agent.position[0], agent.position[1]

            self.create_line(0, 0, 0, 0,
                             tags=f'line-{agent.id}',
                             fill=self.COLORS[agent.id], width=5)
            self.create_oval(self.scale(x) + (self.CELL_SIZE - self.AGENT_SIZE),
                             self.scale(y) + (self.CELL_SIZE - self.AGENT_SIZE),
                             self.scale(x) + self.AGENT_SIZE,
                             self.scale(y) + self.AGENT_SIZE,
                             tags=['agent', f'agent-{agent.id}'],
                             fill=self.COLORS[agent.id])
            self.create_text(self.scale(x) + (self.CELL_SIZE / 2),
                             self.scale(y) + (self.CELL_SIZE / 2),
                             tags=['agent', f'agent-text-{agent.id}'],
                             text=f'{agent.id}')

        self.tag_raise('agent')

    def update(self):
        for agent in self.simulation.agents:
            x = agent.position[0]
            y = agent.position[1]

            self.coords(f'agent-{agent.id}',
                        self.scale(x) + (self.CELL_SIZE - self.AGENT_SIZE),
                        self.scale(y) + (self.CELL_SIZE - self.AGENT_SIZE),
                        self.scale(x) + self.AGENT_SIZE,
                        self.scale(y) + self.AGENT_SIZE)
            self.coords(f'agent-text-{agent.id}',
                        self.scale(x) + (self.CELL_SIZE / 2),
                        self.scale(y) + (self.CELL_SIZE / 2))

            if agent.path:
                self.itemconfigure(f'line-{agent.id}', state='normal')
                self.coords(f'line-{agent.id}',
                            *[self.scale(item) + (self.CELL_SIZE / 2)
                              for sublist in [agent.position] + [p[1] for p in agent.path]
                              for item in sublist])
            else:
                self.itemconfigure(f'line-{agent.id}', state='hidden')

    def scale(self, n):
        return (n * self.CELL_SIZE) + self.MARGIN

    def descale(self, n):
        return (n - self.MARGIN) // self.CELL_SIZE

    def clicked(self, event):
        x = self.descale(event.x)
        y = self.descale(event.y)
        print(f'clicked ({x},{y})')


if __name__ == "__main__":
    root = tk.Tk()
    Application(root)
    root.mainloop()
