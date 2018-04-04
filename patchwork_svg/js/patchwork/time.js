SVG.Time = SVG.invent({
    // Initialize node
    create: function() {
        this.constructor.call(this, SVG.create('svg'))

        this.style('overflow', 'visible')
        //this.circle(5).fill("red").cx(0).cy(0)
        this.size(BUTTON.size,BUTTON.size)
    }

//Inherit from
, inherit: SVG.Container

, extend: {
    _build: function() {
        var s = BUTTON.size/5
        var sy = BUTTON.size /5
        this.polyline([[0,0],[s,sy],[-s,sy],[0,0],[s,-sy],[-s,-sy],[0,0]])
                .stroke("black").fill("none")
        return this
    },
    mark_as_cost: function() {
        this._main_circle.attr({"fill-opacity":0})
    }
    
}


//Add parent method
, construct: {
    // Create nested svg document
    time: function() {
        return this.put(new SVG.Time)._build()
    }
}
})