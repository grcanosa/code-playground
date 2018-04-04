svg_container = SVG('svgcontainer').size(1000,1000).style("overflow","visible")


var pieces = PIECES.split("#")
var pieces_objs = []
for(i=0;i<pieces.length;i++)
{
    piece_spli = pieces[i].split(";")
    if(piece_spli.length == 4)
    {
        var piece_info = {}
        piece_info.cost_button = piece_spli[0]
        piece_info.cost_time = piece_spli[1]
        piece_info.price_button = Number(piece_spli[2])
        piece_info.points = []
        points = piece_spli[3].split(",")
        for(j=0;j<points.length;j++)
        {
            piece_info.points.push({"x":Number(points[j][0]),"y":Number(points[j][1])})
        }
        pieces_objs.push(piece_info)
    }
    else
    {
        console.log("Problem with piece: \""+pieces[i]+"\"")
    }
}

console.log(pieces_objs)
svg_container.size(1000,10000)
var y_offset = 0
var x_offset = 0
var max_y = 0
for(k =0; k < pieces_objs.length;k++)
{
    piece = svg_container.piece(pieces_objs[k])    
    piece.y(y_offset).x(x_offset)
    if(k%3 == 0 && k != 0)
    {
        y_offset = y_offset + max_y + PIECE.side /2
        x_offset = 0
        max_y = 0
    }
    else
    {
        x_offset = piece.bbox().width + x_offset + PIECE.side /2
        if(max_y < piece.bbox().height)
            max_y = piece.bbox().height
    }
}
y_offset = y_offset +max_y+ PIECE.side/3
max_y = 0
x_offset = 0
for(k2 =0; k2 < pieces_objs.length;k2++)
{
    console.log(k2)
    piece = svg_container.piece(pieces_objs[k2]) 
    piece.flip('x')
    piece.y(y_offset).x(x_offset)
    if(k2%3 == 0 && k2 != 0)
    {
        y_offset = y_offset + max_y + PIECE.side /2
        x_offset = 0
        max_y = 0
    }
    else
    {
        x_offset = piece.bbox().width + x_offset + PIECE.side /2
        if(max_y < piece.bbox().height)
            max_y = piece.bbox().height
    }
}

