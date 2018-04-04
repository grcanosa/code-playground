SVG.Piece = SVG.invent({
    // Initialize node
    create: function() {
        this.constructor.call(this, SVG.create('svg'))

        this.style('overflow', 'visible')
        //this.circle(5).fill("red").cx(0).cy(0)
        this.size(1000,1000)

    }

//Inherit from
, inherit: SVG.Container

, extend: {
    _build: function(info) {

        
        for(i=0; i< info.points.length; i++)
        {
            point = info.points[i]
            this.circle(50).fill("red").cx(point.x*50).cy(point.y*50)
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