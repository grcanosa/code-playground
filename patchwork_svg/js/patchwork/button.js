SVG.Button = SVG.invent({
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
        
        this._main_circle = this.circle(BUTTON.size).fill(BUTTON.color1).stroke("black").cx(0).cy(0)
        this._circle1 = this.circle(BUTTON.size/4).fill(BUTTON.color2).stroke("black").cx(BUTTON.size/4).cy(0)
        this._circle2 = this.circle(BUTTON.size/4).fill(BUTTON.color2).stroke("black").cx(-BUTTON.size/4).cy(0)

        return this
    },
    mark_as_cost: function() {
        this._main_circle.attr({"fill-opacity":0}).size(BUTTON.size/2)
        this._circle1.size(BUTTON.size/8).cx(BUTTON.size/8).cy(0)
        this._circle2.size(BUTTON.size/8).cx(-BUTTON.size/8).cy(0)
        return this
    }
    
}


//Add parent method
, construct: {
    // Create nested svg document
    button: function() {
        return this.put(new SVG.Button)._build()
    }
}
})