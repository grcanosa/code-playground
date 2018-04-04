SVG.Piece = SVG.invent({
    // Initialize node
    create: function() {
        this.constructor.call(this, SVG.create('svg'))

        this.style('overflow', 'visible')
        //this.circle(5).fill("red").cx(0).cy(0)
        this.size(10,10)
    }

//Inherit from
, inherit: SVG.Container

, extend: {
    _build: function(info) {
        this._pieces = []
        
        for(i=0; i< info.points.length; i++)
        {
            point = info.points[i]
            this._pieces.push(this.rect(PIECE_SIZE,PIECE_SIZE).fill("white").stroke("black").x(point.x*PIECE_SIZE).y(point.y*PIECE_SIZE))
        }

        return this
    }
    
}


//Add parent method
, construct: {
    // Create nested svg document
    piece: function(info) {
        return this.put(new SVG.Piece)._build(info)
    }
}
})