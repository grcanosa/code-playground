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
        console.log(info)
        this._squares = []
        var price_button = info.price_button
        for(i=0; i< info.points.length; i++)
        {
            point = info.points[i]
            this._squares.push(this.rect(PIECE.side,PIECE.side)
                            .fill("white")
                            .stroke("black")
                            .x(point.x*PIECE.side)
                            .y(point.y*PIECE.side))
            if(i==0) 
            {
                //COST in BUTTONS
                this.text1 = this.text(info.cost_button).fill("black")
                            .x(point.x*PIECE.side+10)
                            .y(point.y*PIECE.side+3).attr({"text-anchor":"middle"})
                this.button().x(point.x*PIECE.side+PIECE.side/1.6)
                                .y(point.y*PIECE.side+PIECE.side/4).mark_as_cost().size(BUTTON.size/2,BUTTON.size/2)
                //COST in TIME
                this.text2 = this.text(info.cost_time).fill("black")
                            .x(point.x*PIECE.side+10)
                            .y(point.y*PIECE.side+3+PIECE.side/2).attr({"text-anchor":"middle"})    

                this.time().x(point.x*PIECE.side+PIECE.side/1.6)
                                .y(point.y*PIECE.side+PIECE.side*3/4)                            

            }
            else
            {
                if(price_button > 0)
                {
                    this.button().x(point.x*PIECE.side+PIECE.side/2)
                                .y(point.y*PIECE.side+PIECE.side/2)
                    price_button--;
                }
            }
        }
        if(price_button > 0)
        {
            console.log("Not all buttons fit!!")
        }
        this
        
        return this
    },
    mirror: function(){
        this.flip('x')
        this.text1.flip('x')
        this.text2.flip('x')
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