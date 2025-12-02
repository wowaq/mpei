import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class Grid:
    def __init__(self, n_h, n_v, cx=0, cy=0, dx=1, dy=1):
        self.n_h = n_h
        self.n_v = n_v
        self.cx = cx
        self.cy = cy
        self.dx = dx
        self.dy = dy

        self.vertecies = self.get_vertecies_table(n_h, n_v, cx, cy, dx, dy)
        self.edges = self.get_edges_table(self.vertecies, n_h, n_v)
        # self.polygons = self.get_polygons_table(self.edges)

    @staticmethod
    def get_vertecies_table(n_h, n_v, cx=0, cy=0, dx=1, dy=1):
        x = np.linspace(cx - dx, cx + dx, n_h + 2)
        y = np.linspace(cy - dy, cy + dy, n_v + 2)
        xx, yy = np.meshgrid(x, y)
        print(xx.size)
        return pd.DataFrame(
            {"x": xx.ravel(), "y": yy.ravel(), "c": np.random.rand(xx.size)}
        ).dropna()

    @staticmethod
    def get_edges_table(vt: pd.DataFrame, n_h, n_v):
        grid_values = vt.sort_values(by=["x", "y"]).to_numpy()
        5
        return pd.DataFrame({})


df = Grid(5, 20).edges.dropna()
for e in df.itertuples(name="Edge"):
    print(e)
    plt.plot([e.x1, e.x2], [e.y1, e.y2])  # pyright: ignore[reportAttributeAccessIssue]
