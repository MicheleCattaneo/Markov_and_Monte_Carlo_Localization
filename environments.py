from base.shapes import DisplayableRectangle, DisplayableObstacle, DisplayableCircle, DisplayablePolygon


color = (255, 20, 147)

custom = [
    (
        DisplayableObstacle, {"points": [5, 5, 2, 10], "color": color}
    ), (
        DisplayableObstacle, {"points": [10, 5, 2, 10], "color": color}
    ), (
        DisplayableObstacle, {"points": [5, 25, 2, 10], "color": color}
    ), (
        DisplayableObstacle, {"points": [10, 25, 2, 10], "color": color}
    ), (
        DisplayablePolygon, {
            "points": [[20, 20],
                       [25, 25],
                       [20, 25],
                       [18, 23],
                       [20, 20]],
            "color": color
        }
    ), (
        DisplayableCircle, {"points": [20, 2], "radius": 69, "color": color}
    )
]

base_with_obstacle = [
    (
        DisplayableObstacle, {"points": [8, 8, 4, 4], "color": color}
    )
]
