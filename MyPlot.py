#MyPlot.py

class Figure:    
    def __init__(self, figsize=(50, 15)):
        self.width = figsize[0]
        self.height = figsize[1]
        self.plots = []
        self.title = None
        self.xlabel = None
        self.ylabel = None                                              
      
    def add_plot(self, xs, ys, marker='*', linestyle='-', label=None):
        if len(xs) != len(ys):
            raise ValueError("xs y ys deben tener la misma longitud")
        self.plots.append({
            'xs': list(xs),
            'ys': list(ys),
            'marker': marker,
            'linestyle': linestyle,
            'label': label
        })


class ASCIIPlot:
    def __init__(self):                                           
        self.current_figure = None
        self.figures = []
        
    def figure(self, figsize=(50, 15)):
        self.current_figure = Figure(figsize)
        self.figures.append(self.current_figure)
        return self.current_figure
    
    def plot(self, *args, marker='*', linestyle='-', label=None):
        if self.current_figure is None:
            self.figure()
        
        if len(args) == 1:
            ys = args[0]
            xs = list(range(len(ys)))
        elif len(args) == 2:
            xs, ys = args
        else:
            raise ValueError("plot() acepta 1 o 2 argumentos posicionales")
        
        self.current_figure.add_plot(xs, ys, marker, linestyle, label)
    
    # Grafico de dispersion    
    def scatter(self, xs, ys, marker='o', label=None):
        if self.current_figure is None:
            self.figure()
        self.plot(xs, ys, marker=marker, linestyle='', label=label)
    
    def title(self, text):
        if self.current_figure is None:
            self.figure()
        self.current_figure.title = str(text)
    
    def xlabel(self, text):
        if self.current_figure is None:
            self.figure()
        self.current_figure.xlabel = str(text)
    
    def ylabel(self, text):
        if self.current_figure is None:
            self.figure()
        self.current_figure.ylabel = str(text)
    
    def show(self):
        if not self.current_figure:
            print("(grafico vacío)")
            return
        self._render_figure(self.current_figure)
    
    # Limpia la figura actual
    def clf(self):
        if self.current_figure:
            self.current_figure.plots = []
            self.current_figure.title = None
            self.current_figure.xlabel = None
            self.current_figure.ylabel = None
    
    def close(self):
        self.current_figure = None
        self.figures = []
        
    def _render_figure(self, fig):
        if not fig.plots:
            print("(grafico vacío)")
            return
                              
                           
        # Recopilar todos los datos
        all_xs = []
        all_ys = []
        for plot_data in fig.plots:
            all_xs.extend(plot_data['xs'])
            all_ys.extend(plot_data['ys'])
        
        if not all_xs:
            print("(grafico vacío)")
            return
        
        # Calcular rangos
        min_x = min(all_xs)
        max_x = max(all_xs)
        min_y = min(all_ys)
        max_y = max(all_ys)
        
        # Evitar división por cero
        if min_x == max_x:
            min_x -= 1                                              
            max_x += 1
        if min_y == max_y:
            min_y -= 1
            max_y += 1
        
        rows = fig.height
        cols = fig.width
        
        # Crear grid vacía
        grid = [[" " for _ in range(cols)] for _ in range(rows)]
        
        # Funciones de mapeo
        def x_to_col(x):
            return int((x - min_x) / (max_x - min_x) * (cols - 1))
        
        def y_to_row(y):
            pos = (y - min_y) / (max_y - min_y) * (rows - 1)
            return rows - 1 - int(pos)
        
        # Dibujar ejes
        if min_y <= 0 <= max_y:
            x_axis_row = y_to_row(0)
        else:
            x_axis_row = rows - 1
        
        for c in range(cols):
            grid[x_axis_row][c] = "-"
        
        if min_x <= 0 <= max_x:
            y_axis_col = x_to_col(0)
        else:
            y_axis_col = 0
        
        for r in range(rows):
            grid[r][y_axis_col] = "|"
        
        # Origen
        if 0 <= x_axis_row < rows and 0 <= y_axis_col < cols:
            grid[x_axis_row][y_axis_col] = "+"
        
        # Marcadores para multiples series
        markers_cycle = ['*', 'o', '#', '@', 'x', '+']
        
        # Dibujar cada plot
        for idx, plot_data in enumerate(fig.plots):
            xs = plot_data['xs']
            ys = plot_data['ys']
            marker = plot_data['marker']
            linestyle = plot_data['linestyle']
            
            # Asignar marcador unico si hay multiples plots
            if len(fig.plots) > 1 and marker == '*':
                marker = markers_cycle[idx % len(markers_cycle)]
            
            # Convertir puntos a coordenadas
            puntos = []
            for x, y in zip(xs, ys):
                c = x_to_col(x)
                r = y_to_row(y)
                if 0 <= r < rows and 0 <= c < cols:
                    puntos.append((c, r))
            
            # Dibujar lineas conectando puntos consecutivos
            if linestyle and linestyle != '' and len(puntos) > 1:
                for i in range(len(puntos) - 1):
                    c1, r1 = puntos[i]
                    c2, r2 = puntos[i + 1]
                    
                    # Algoritmo de Bresenham - dibuja linea delgada
                    dc = abs(c2 - c1)
                    dr = abs(r2 - r1)
                    sc = 1 if c2 > c1 else -1
                    sr = 1 if r2 > r1 else -1
                    err = dc - dr
                    
                    c, r = c1, r1
                    
                    while True:
                        # Solo dibujar si NO es un punto de datos
                        if 0 <= r < rows and 0 <= c < cols:
                            # Verificar que no sea uno de los puntos de datos originales
                            is_data_point = (c, r) in puntos
                            if not is_data_point and grid[r][c] == " ":
                                grid[r][c] = marker
                        
                        if c == c2 and r == r2:
                            break
                        
                        e2 = 2 * err
                        if e2 > -dr:
                            err -= dr
                            c += sc
                        if e2 < dc:
                            err += dc
                            r += sr
            
            # Marcar los puntos de datos con el marcador
            for c, r in puntos:
                if 0 <= r < rows and 0 <= c < cols:
                    grid[r][c] = marker
        
        # Imprimir título
        if fig.title:
            print()
            title_str = str(fig.title)
            title_padding = (cols - len(title_str)) // 2
            print(" " * (6 + title_padding) + title_str)
        
        print()
        
        # Etiquetas de Y y grid
        y_labels = []
        label_positions = [0, rows // 2, rows - 1]
        label_values = [max_y, (max_y + min_y) / 2, min_y]
        
        for r in range(rows):
            if r in label_positions:
                idx = label_positions.index(r)
                label = f"{label_values[idx]:5.2f}"
            else:
                label = " " * 5
            
            print(label + " " + "".join(grid[r]))
        
        # Etiquetas de X
        x_labels = [" " for _ in range(cols)]
        
        positions = [
            (0, f"{min_x:.2f}"),
            (cols // 2, f"{(min_x + max_x) / 2:.2f}"),
            (cols - 1, f"{max_x:.2f}")
        ]
        
        for pos, text in positions:
            if pos == 0:
                start = 0
            elif pos == cols - 1:
                start = max(0, cols - len(text))
            else:
                start = max(0, min(cols - len(text), pos - len(text) // 2))
            
            for i, ch in enumerate(text):
                if start + i < cols:
                    x_labels[start + i] = ch
        
        print(" " * 6 + "".join(x_labels))
        
        # Imprimir xlabel
        if fig.xlabel:
            xlabel_str = str(fig.xlabel)
            xlabel_padding = (cols - len(xlabel_str)) // 2
            print(" " * (6 + xlabel_padding) + xlabel_str)
        
        # Leyenda
        if any(p['label'] for p in fig.plots):
            print()
            print("Leyenda:")
            for idx, plot_data in enumerate(fig.plots):
                if plot_data['label']:
                    m = plot_data['marker']
                    if len(fig.plots) > 1 and m == '*':
                        m = markers_cycle[idx % len(markers_cycle)]
                    print(f"  {m} - {plot_data['label']}")
        
        print()



_plt = ASCIIPlot()

# Crea una nueva figura
def figure(figsize=(50, 15)):
    return _plt.figure(figsize)

# Grafica datos
def plot(*args, marker='*', linestyle='-', label=None):
    _plt.plot(*args, marker=marker, linestyle=linestyle, label=label)

# Grafico de dispersion
def scatter(xs, ys, marker='o', label=None):
    _plt.scatter(xs, ys, marker=marker, label=label)

def title(text):
    _plt.title(text)

def xlabel(text):
    _plt.xlabel(text)

def ylabel(text):
    _plt.ylabel(text)

def show():
    _plt.show()

def clf():
    _plt.clf()

def close():
    _plt.close()
