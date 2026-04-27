import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button
from collections import deque

# Create Graph
G = nx.Graph()
edges = [
    ('A', 'B'), ('A', 'C'),
    ('B', 'D'), ('B', 'E'),
    ('C', 'F'), ('C', 'G'),
    ('A', 'H'), ('H', 'I')
]
G.add_edges_from(edges)
pos = nx.spring_layout(G)

# Traversal steps and animation state
bfs_steps, dfs_steps = [], []
current_animation = None
traversal_type = 'BFS'
current_step = 0
is_playing = False
is_paused = False

# BFS
def bfs_traversal(start):
    visited = set()
    queue = deque([start])
    steps = []
    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.add(node)
            steps.append(list(visited))
            queue.extend(neighbor for neighbor in G.neighbors(node) if neighbor not in visited)
    return steps

# DFS
def dfs_traversal(start):
    visited = set()
    stack = [start]
    steps = []
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            steps.append(list(visited))
            stack.extend(reversed(list(G.neighbors(node))))
    return steps

# Draw function for animation
def draw_step(i):
    global current_step
    current_step = i
    draw_current_step()

# Draw current step (used by both animation and manual stepping)
def draw_current_step():
    ax.clear()
    steps = bfs_steps if traversal_type == 'BFS' else dfs_steps
    
    if current_step < len(steps):
        ax.set_title(f"{traversal_type} - Step {current_step + 1}/{len(steps)}")
        color_map = ['red' if node in steps[current_step] else 'lightgray' for node in G.nodes()]
    else:
        ax.set_title(f"{traversal_type} - Complete")
        color_map = ['red' for node in G.nodes()]
    
    nx.draw(G, pos, with_labels=True, node_color=color_map, node_size=1000, ax=ax)
    plt.draw()

# Animation control functions
def start_animation(event):
    global current_animation, is_playing, is_paused
    if is_paused:
        # Resume from pause
        current_animation.resume()
        is_playing = True
        is_paused = False
        btn_start.label.set_text('Pause')
    else:
        # Start new animation
        reset_to_beginning()
        steps = bfs_steps if traversal_type == 'BFS' else dfs_steps
        current_animation = animation.FuncAnimation(fig, draw_step, frames=len(steps), 
                                                 interval=1000, repeat=False)
        is_playing = True
        is_paused = False
        btn_start.label.set_text('Pause')
    plt.draw()

def pause_animation(event):
    global is_playing, is_paused
    if current_animation is not None and is_playing:
        current_animation.pause()
        is_playing = False
        is_paused = True
        btn_start.label.set_text('Resume')
        plt.draw()

def next_step(event):
    global current_step
    steps = bfs_steps if traversal_type == 'BFS' else dfs_steps
    if current_step < len(steps) - 1:
        current_step += 1
        draw_current_step()
        # Pause animation if running
        if is_playing:
            pause_animation(None)

def prev_step(event):
    global current_step
    if current_step > 0:
        current_step -= 1
        draw_current_step()
        # Pause animation if running
        if is_playing:
            pause_animation(None)

def reset_to_beginning():
    global current_step
    current_step = 0

def reset_graph(event):
    global current_animation, is_playing, is_paused, current_step
    
    # Stop any running animation
    if current_animation is not None and current_animation.event_source is not None:
        current_animation.event_source.stop()
        current_animation = None
    
    is_playing = False
    is_paused = False
    current_step = 0
    btn_start.label.set_text('Start')
    
    ax.clear()
    nx.draw(G, pos, with_labels=True, node_color='lightgray', node_size=1000, ax=ax)
    ax.set_title("Graph Reset - Ready for Traversal")
    plt.draw()

# Button Handlers for traversal type
def set_bfs(event):
    global traversal_type, current_step
    traversal_type = 'BFS'
    current_step = 0  # Reset step when changing algorithm
    if not is_playing:  # Only update display if not currently animating
        ax.set_title("Selected BFS - Ready to Start")
        plt.draw()

def set_dfs(event):
    global traversal_type, current_step
    traversal_type = 'DFS'
    current_step = 0  # Reset step when changing algorithm
    if not is_playing:  # Only update display if not currently animating
        ax.set_title("Selected DFS - Ready to Start")
        plt.draw()

# Handle start/pause button click
def toggle_play_pause(event):
    if is_playing:
        pause_animation(event)
    else:
        start_animation(event)

# Precompute steps
bfs_steps = bfs_traversal('A')
dfs_steps = dfs_traversal('A')

# Matplotlib setup
fig, ax = plt.subplots(figsize=(12, 8))
plt.subplots_adjust(bottom=0.25)

# Create buttons with better spacing
button_width = 0.12
button_height = 0.075
button_y = 0.05
spacing = 0.02

# Row 1: Algorithm selection and main controls
ax_bfs = plt.axes((0.05, button_y + 0.1, button_width, button_height))
ax_dfs = plt.axes((0.05 + button_width + spacing, button_y + 0.1, button_width, button_height))
ax_start = plt.axes((0.05 + 2*(button_width + spacing), button_y + 0.1, button_width, button_height))
ax_reset = plt.axes((0.05 + 3*(button_width + spacing), button_y + 0.1, button_width, button_height))

# Row 2: Step controls
ax_prev = plt.axes((0.35, button_y, button_width, button_height))
ax_next = plt.axes((0.35 + button_width + spacing, button_y, button_width, button_height))

# Create buttons
btn_bfs = Button(ax_bfs, 'BFS')
btn_dfs = Button(ax_dfs, 'DFS')
btn_start = Button(ax_start, 'Start')
btn_reset = Button(ax_reset, 'Reset')
btn_prev = Button(ax_prev, '← Prev')
btn_next = Button(ax_next, 'Next →')

# Connect button events
btn_bfs.on_clicked(set_bfs)
btn_dfs.on_clicked(set_dfs)
btn_start.on_clicked(toggle_play_pause)
btn_reset.on_clicked(reset_graph)
btn_prev.on_clicked(prev_step)
btn_next.on_clicked(next_step)

# Initialize the graph display
reset_graph(None)

# Add keyboard support (optional enhancement)
def on_key_press(event):
    if event.key == ' ':  # Spacebar for play/pause
        toggle_play_pause(None)
    elif event.key == 'left':  # Left arrow for previous
        prev_step(None)
    elif event.key == 'right':  # Right arrow for next
        next_step(None)
    elif event.key == 'r':  # R for reset
        reset_graph(None)

fig.canvas.mpl_connect('key_press_event', on_key_press)

plt.show()