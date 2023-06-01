from base.shapes import DisplayableObstacle, DisplayableCircle, DisplayablePolygon

color = (151, 151, 151)

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

symmetric_rooms = [
    # horisontal walls
    (
        DisplayableObstacle, {"points": [1, 10, 15, 1], "color": color, "textured": False}
    ),
    (
        DisplayableObstacle, {"points": [1, 20, 15, 1], "color": color, "textured": False}
    ),
    (
        DisplayableObstacle, {"points": [20, 10, 11, 1], "color": color, "textured": False}
    ),
    (
        DisplayableObstacle, {"points": [20, 20, 11, 1], "color": color, "textured": False}
    ),
    (
        DisplayableObstacle, {"points": [35, 10, 15, 1], "color": color, "textured": False}
    ),
    (
        DisplayableObstacle, {"points": [35, 20, 15, 1], "color": color, "textured": False}
    ),

    # vertical walls
    (
        DisplayableObstacle, {"points": [25, 1, 1, 10], "color": color, "textured": False}
    ),
    (
        DisplayableObstacle, {"points": [25, 20, 1, 10], "color": color, "textured": False}
    ),
    # polygons
    (
        DisplayablePolygon, {
            "points": [[3, 4],
                       [5, 5],
                       [3, 7],
                       [2, 5],
                       [3, 4]],
            "color": (255, 51, 51)
        }
    ),
    (
        DisplayablePolygon, {
            "points": [[3, 24],
                       [5, 25],
                       [4, 28],
                       [3, 27],
                       [2, 25],
                       [3, 24]],
            "color": (255, 255, 0)
        }
    ),
    (
        DisplayablePolygon, {
            "points": [[47, 4],
                       [49, 5],
                       [47, 8],
                       [47, 7],
                       [46, 5],
                       [47, 4]],
            "color": (128, 255, 0)
        }
    ),
    (
        DisplayablePolygon, {
            "points": [[47, 24],
                       [49, 25],
                       [48, 28],
                       [47, 27],
                       [46, 25],
                       [47, 24]],
            "color": (0, 128, 255)
        }
    ),
]
