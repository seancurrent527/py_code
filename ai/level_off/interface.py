from level_off import parse_args
import game, problems
import tkinter as tk

def draw_grid(position, grid, size = 50):
    rows, cols = len(grid), len(grid[0])
    grid_elements = {}
    for r in range(rows):
        for c in range(cols):
            kind = 'P' if ((r, c) == position) else grid[r][c]
            color = 'black' if kind is None else 'white'
            canvas = tk.Canvas(root, width=size, height=size, bg=color)
            text = canvas.create_text(size//2, size//2, font=('Helvetica', size//2),
            text = ' ' if not kind else str(kind))
            grid_elements[(r, c)] = [canvas, text]
    return grid_elements

def update_grid(grid_elements, position, grid):
    for (r, c), (canvas, text) in grid_elements.items():
        kind = 'P' if ((r, c) == position) else grid[r][c]
        canvas.itemconfigure(text, text = ' ' if not kind else str(kind))
    root.update()

def position_grid(grid_elements, looper):
    max_r = 0
    for (r, c), (canvas, text) in grid_elements.items():
        canvas.grid(row=r, column=c)
        if r > max_r:
            max_r = r
    up = tk.Button(root, text="^", command=lambda: looper('w'))
    up.grid(row=max_r + 2, column=1)
    left = tk.Button(root, text="<", command=lambda: looper('a'))
    left.grid(row=max_r + 3, column=0)
    right = tk.Button(root, text=">", command=lambda: looper('d'))
    right.grid(row=max_r + 3, column=2)
    down = tk.Button(root, text="v", command=lambda: looper('s'))
    down.grid(row=max_r + 4, column=1)
    pull = tk.Button(root, text="Pull", command=lambda: looper('p'))
    pull.grid(row=max_r + 3, column=3, columnspan=2)
    quitter = tk.Button(root, text="Quit", command=root.destroy)
    quitter.grid(row=max_r + 5, column=7)

def messenger(max_r):
    text = tk.StringVar()
    # set initial value of text
    text.set("  ")
    result = tk.Label(root, textvariable=text, font = ('Helvetica', 12), fg='black')
    result.grid(row=max_r + 2, column=4, columnspan=3)
    
    def message(s):
        text.set(s)
    
    return message

def action_loop(game, grid_elements, message):

    def looper(action):
        global PULL
        if action == 'p':
            message('Pull on')
            PULL = True
            return
        if PULL:
            action = 'p' + action
            PULL = False
        mp = {'w':'NORTH', 'a':'WEST', 's':'SOUTH', 'd':'EAST'}
        prefix = 'PULL_' if action.startswith('p') else 'PUSH_'
        action = prefix + mp[action[-1]]
        result = game.gameState.move(action)
        if not result:
            message('Not valid')
        else:
            message(' ')
            update_grid(grid_elements, game.gameState.getPlayerPosition(), game.gameState.getState())
        if not game.gameState.isPlayable():
            message('Leveled off!')

    return looper

def run(game):
    grid_elements = draw_grid(game.gameState.getPlayerPosition(), game.gameState.getState(), size = 50)
    message = messenger(game.gameState.size[0])
    looper = action_loop(game, grid_elements, message)
    position_grid(grid_elements, looper)

if __name__ == '__main__':
    args = parse_args()
    root = tk.Tk()
    PULL = False
    gameState = game.GameState.fromFile(args.file)
    playing = game.Game(gameState, None)
    run(playing)
    root.mainloop()