sum  = function(list, end) {
    // This only works with an ordered list of lists
    for(var s=0,i=end+1;i;s+=list[--i][1]);
    return s;
}

function Graph(el, data, options){
    var context = this;
    this.data = data;
    this.el = el;
    this.options = options || {};
    this.flotobject = '';
    this.plot = function(){
        this.flotobject = $.plot(this.el, this.data, this.options)
    };

    this.zoomgraph = function(event, ranges){
        context.zoomflotobject = $.plot(context.options['zoomtarget'], context.data, $.extend(true, {}, context.options, { xaxis:{min: ranges.xaxis.from,max:ranges.xaxis.to}}));
        context.flotobject.setSelection(ranges, true);
        context.flotobject.clearSelection();


    };

    $(this.el).bind("plotselected", this.zoomgraph);
};

// Example Usage:
//    var options = { xaxis: { mode: "time", tickLength: 5 }, legend: {position: 'nw',}, grid: { hoverable: true}, tooltip: true, tooltipOpts: { content: "%y %s on %x", xDateFormat: "%b %e", }, series: { lines: { show: true },  }, selection: { mode: "x" }, zoomtarget:"#detailGraph" };
//    window.graphs = {
//        userPlot: new Graph("#userGraph",
//           [{data: user_by_day, label:"New Users"}, {data: rolling_user, label:"New Users (weekly rolling average)"}],
//           options),
//    }
//
//    for (var index in window.graphs) {
//        window.graphs[index].plot()
//    };
