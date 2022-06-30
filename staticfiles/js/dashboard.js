var options = {
// Internal padding for the canvas
    paddingBottom: 10,
    paddingLeft: 20,
    paddingRight: 10,
    paddingTop: 10,

    // Canvas background
    background: "#FFFFFF",

    // Show circle on the last data
    showCircle: true,
    circle: "#55AA77",
    circleSize: 7,

    // Show the line at zero
    // showZeroLine: true,#}
    zeroLineColor: "#EEE",

    // Color and whidth of the line chart
    lineColor: "#8888EE",
    lineWidth: 5,

    // Show the bounds
    showBounds: false,
    bounds: "#8888EE",
    boundsHeight: 20,
    boundsFont: "Arial",

    // Show the legend
    showLegend: true,
    legend: "#8888EE",
    legendHeight: 14,
    legendFont: "Arial"
};

function update_graphs(row){
    var stat_id = $(row).attr("data-stat-id");
    var canvas_hourly = $(row).find(".stat-graph-hourly > canvas")[0];
    var canvas_daily = $(row).find(".stat-graph-daily > canvas")[0];
    var val_holder = $(row).find(".stat-value").children().eq(1);

    $.ajax({
        url: HOST_URL + "/stat/history?id=" + stat_id,
        success: function (Data) {
            console.log(Data);
            val_holder.html(Data.last_value);
            new Graph(Data.histories_hourly, canvas_hourly, options);
            new Graph(Data.histories_daily, canvas_daily, options);
        },
        error: function (a, b, c) {
            console.log(a, b, c);
        }
    });
}

$(document).ready(function () {
    $(".stat-row").each(function () {
        update_graphs(this);
    })
});

$(".refresh_button").click(function () {
    var stat_id = $(this).attr("data-stat-id");
    var link_holder = $(this);
    var row = $(this).parent().parent();
    link_holder.html('<i class="fa fa-clock-o"></i>');
    var time_holder = row.find(".stat-time");

    $.ajax({
        url: HOST_URL + "/stat/update?id=" + stat_id,
        success: function (Data) {
            link_holder.html('<i class="fa fa-refresh"></i>');
            time_holder.html("0 minutes ago");
            update_graphs(row);
        },
        error: function (a, b, c) {
            alert(a,b,c);
            link_holder.html('<i class="fa fa-refresh"></i>');
        }
    });
});