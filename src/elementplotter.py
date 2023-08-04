import pandas as pd
import plotly.express as px


class ElementPlotter:
    def __init__(self, base_stations, user_equipments):
        self._base_stations = base_stations
        self._user_equipments = user_equipments

    def _max_x(self):
        bs_x = max(bs.x for bs in self._base_stations)
        ue_x = max(ue.x for ue in self._user_equipments)
        return max(bs_x, ue_x)

    def _max_y(self):
        bs_y = max(bs.y for bs in self._base_stations)
        ue_y = max(ue.y for ue in self._user_equipments)
        return max(bs_y, ue_y)

    def plot_elements(self):
        bs_coordinates = [bs.coordinates for bs in self._base_stations]
        ue_coordinates = [ue.coordinates for ue in self._user_equipments]
        coordinates_dict_list = []

        for (x, y) in bs_coordinates:
            bs_dict = {"Type": "bs", "x": x, "y": y}
            coordinates_dict_list.append(bs_dict)

        for (x, y) in ue_coordinates:
            ue_dict = {"Type": "ue", "x": x, "y": y}
            coordinates_dict_list.append(ue_dict)

        df = pd.DataFrame(coordinates_dict_list)
        df = df.reset_index(drop = True)

        df["size"] = [30 if marker_type == 'bs' else (5 if marker_type == 'ue' else 0) for marker_type in df['Type']]

        fig = px.scatter(df,
                         x="x",
                         y="y",
                         color="Type",
                         symbol="Type",
                         symbol_sequence=["triangle-up", "circle"],
                         range_x=(-10, (self._max_x()) + 10),
                         range_y=(-10, (self._max_y()+ 10)),
                         size="size",
                         size_max=30)

        fig.update_layout(xaxis_title="X-coordinate", yaxis_title="Y-coordinate",
                          title="Location of Base Stations and User Equipments")
        fig.show()
