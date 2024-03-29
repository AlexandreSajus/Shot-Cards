from taipy.gui import Gui
import numpy as np
from math import cos, sin, atan, sqrt, pi
import random

shots = [
    (8.1, 15),
    (9.5, 5),
    (9.6, 25),
    (9.4, 65),
    (9.2, 280),
    (9.8, 280),
    (9.4, 95),
    (10.4, 240),
    (10.6, 270),
    (10.8, 30),
    (10.7, 70),
    (9.7, 185),
    (9.9, 175),
    (9.6, 180),
    (9.3, 170),
    (8.8, 150),
    (8.7, 180),
    (8.6, 200),
    (7.9, 225),
    (7.1, 170),
]

# Decrease all radii by 1
shots = [(r - 1, a) for (r, a) in shots]

exercise = "Single Shots"
firearm = "Glock 19X"
caliber = "9x19mm"
shooting_distance = 15
target_radius = 0.25

radiuses = [x[0] for x in shots]
angles = [x[1] for x in shots]

average_score = sum(radiuses) / len(radiuses)
# torso is shots above 5
torso_hits = len([x for x in radiuses if x + 1 >= 5])
torso_accuracy = torso_hits / len(radiuses)
# head is shots above 8
head_hits = len([x for x in radiuses if x + 1 >= 8])
head_accuracy = head_hits / len(radiuses)

mean_hit_radius = sum([(10 - x) * 0.025 for x in radiuses]) / len(radiuses)
accuracy_radians = atan(mean_hit_radius / shooting_distance)
accuracy_moa = accuracy_radians * (180 / pi) * 60

distances_to_center = [10 - x for x in radiuses]
angles_to_center = [x * pi / 180 for x in angles]

x_coords = [r * cos(a) for (r, a) in zip(distances_to_center, angles_to_center)]
y_coords = [r * sin(a) for (r, a) in zip(distances_to_center, angles_to_center)]

mean_x = sum(x_coords) / len(x_coords)
mean_y = sum(y_coords) / len(y_coords)

mean_hit_angle = atan(mean_y / mean_x)
mean_hit_angle = mean_hit_angle * (180 / pi)
if mean_x < 0:
    mean_hit_angle += 180
if mean_x > 0 and mean_y < 0:
    mean_hit_angle += 360
mean_radius = 10 - sqrt(mean_x**2 + mean_y**2)


def scattering_distance(shots: list) -> float:
    scattering_distance = 0
    for shot_1 in shots:
        for shot_2 in shots:
            (r_1, a_1) = ((10 - shot_1[0]) * 0.025, shot_1[1])
            (r_2, a_2) = ((10 - shot_2[0]) * 0.025, shot_2[1])
            x_1 = r_1 * cos(a_1 * pi / 180)
            y_1 = r_1 * sin(a_1 * pi / 180)
            x_2 = r_2 * cos(a_2 * pi / 180)
            y_2 = r_2 * sin(a_2 * pi / 180)
            distance_between_shots = sqrt((x_2 - x_1) ** 2 + (y_2 - y_1) ** 2)
            if distance_between_shots > scattering_distance:
                scattering_distance = distance_between_shots
    return scattering_distance / 2


general_scattering_distance = scattering_distance(shots)
general_scatter_radians = atan(general_scattering_distance / shooting_distance)
general_scatter_moa = general_scatter_radians * (180 / pi) * 60

five_shot_scatters = []
for i in range(100):
    sample = random.sample(shots, 5)
    five_shot_scatter = scattering_distance(sample)
    five_shot_scatters.append(five_shot_scatter)

# Take the median
five_shot_scatters.sort()
five_shot_scattering_distance = five_shot_scatters[49]
five_shot_scatter_radians = atan(five_shot_scattering_distance / shooting_distance)
five_shot_scatter_moa = five_shot_scatter_radians * (180 / pi) * 60


data = {"Score": radiuses, "Hits": angles}

data_average = {"Score": [mean_radius], "Hits Average": [mean_hit_angle]}

layout = {
    "polar": {
        "angularaxis": {
            "rotation": 90,
            "direction": "clockwise",
            # One tick every 30 degrees
            "tickvals": list(np.arange(0.0, 360.0, 30)),
            # Text value for every tick
            "showgrid": False,
            # Don't show tick labels
            "showticklabels": False,
        },
        "radialaxis": {
            "angle": 0,
            "tickmode": "array",
            "tickvals": [9.5, 9, 8, 7, 6, 5, 4, 3, 2, 1],
            "ticktext": [
                "",
                "   9",
                "   8",
                "   7",
                "   6",
                "   5",
                "   4",
                "   3",
                "   2",
                "   1",
            ],
            "range": [10, 0],
            "showline": False,
            "tickfont": {"size": 15},
        },
    },
    "showlegend": False,
    "hovermode": False,
    "dragmode": "select",
    "legend": {"font": {"size": 20}},
}

layout_average = {
    "polar": {
        "angularaxis": {
            "rotation": 90,
            "direction": "clockwise",
            # One tick every 30 degrees
            "tickvals": list(np.arange(0.0, 360.0, 30)),
            # Text value for every tick
            "showgrid": False,
            # Don't show tick labels
            "showticklabels": False,
        },
        "radialaxis": {
            "angle": 0,
            "tickmode": "array",
            "tickvals": [9.5, 9, 8, 7, 6, 5, 4, 3, 2, 1],
            "ticktext": [
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
            ],
            "range": [10, 0],
            "showline": False,
            "tickfont": {"size": 8},
        },
    },
    "showlegend": False,
    "hovermode": False,
    "dragmode": "select",
    "legend": {"font": {"size": 20}},
    "margin": {"l": 0, "r": 0, "t": 0, "b": 0},
}

marker = {"color": "red", "size": 10}

marker_average = {"color": "green", "size": 10}

page = """
<|layout|columns=1 1|
<|part|
# <center>Shot **Card**{: .color-primary}</center>
<|part|
<|layout|columns=1 1|
<|part|class_name=card mt1|
## Session
- **10 m**{: .color-primary} **Distance** ( 10.9 yds )
- **Glock 19**
- **9x19mm**
- 20 Shots ( No Time Constraint )
- 25 cm Target Radius ( 9.8 in )
|>

<|part|class_name=card mt1|
## Average Score: <|{round(average_score,1)}|text|raw|>
Grouping center:
<|{data_average}|chart|type=scatterpolar|layout={layout_average}|mode=markers|marker={marker_average}|height=25vh|>
|>
|>
<|layout|columns=1 1|
<|part|class_name=card mt1|
## Accuracy
- **Average Accuracy:** **<|{round(accuracy_moa,1)}|text|raw|> MOA**{: .color-primary}
    - <|{round(mean_hit_radius*100,1)}|text|raw|> cm from center ( <|{round(mean_hit_radius*100*0.394,1)}|text|raw|> in )
- Torso Hits: <|{torso_hits}|text|raw|> ( <|{round(torso_accuracy*100,1)}|text|raw|>% )
- Head Hits: <|{head_hits}|text|raw|> ( <|{round(head_accuracy*100,1)}|text|raw|>% )
|>

<|part|class_name=card mt1|
## Grouping
- **Estimated 5 Shot Scatter:** **<|{round(five_shot_scatter_moa,1)}|text|raw|> MOA**{: .color-primary}
    - <|{round(five_shot_scattering_distance*100,1)}|text|raw|> cm radius ( <|{round(five_shot_scattering_distance*100*0.394,1)}|text|raw|> in )
- Full 8 Shot Scatter: <|{round(general_scatter_moa,1)}|text|raw|> MOA 
    - <|{round(general_scattering_distance*100,1)}|text|raw|> cm radius ( <|{round(general_scattering_distance*100*0.394,1)}|text|raw|> in )

|>
|>
|>
|>

<|{data}|chart|type=scatterpolar|layout={layout}|mode=markers|height=100vh|marker={marker}|>
|>
"""

Gui(page).run(debug=True, use_reloader=True, dark_mode=True, watermark="")
