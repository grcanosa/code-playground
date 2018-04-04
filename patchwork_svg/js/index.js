svg_container = SVG('svgcontainer').size(1000,1000).style("overflow","visible")


pieceinfo = {
    "buttons": 1,
    "cost": {
        "buttons": 3,
        "time" : 2
    },
    "points" : [ {"x": 0, "y": 0}, {"x":1, "y": 0}]

}


svg_container.piece(pieceinfo)