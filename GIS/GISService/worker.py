import json
from typing import Dict, Any


class Worker:
    def __init__(self, config: Dict[Any, Any]):
        self.config = config

    def test(self, data):
        points = data['points']
        p = 0.0
        print(points)
        if len(points) > 2:
            for i in range(len(points) - 1):
                lat1 = points[i][0]
                lon1 = points[i][1]
                lat2 = points[i + 1][0]
                lon2 = points[i + 1][1]
                p += ((lat2 - lat1)**2 + (lon2 - lon1)**2)**0.5
            lat1 = points[0][0]
            lon1 = points[0][1]
            lat2 = points[-1][0]
            lon2 = points[-1][1]
            p += ((lat2 - lat1)**2 + (lon2 - lon1)**2)**0.5
        return str(p)
