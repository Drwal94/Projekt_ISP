$(function() {

    var $angleAJAX = $['angleAJAX'];

    updateData()
    setInterval(function(){
        updateData()
    }, 3000);

    var ctx = document.getElementById("myAreaChart");
    var myLineChart = new Chart(ctx, {
      type: 'line',
      data: {
        datasets: [{
            label: 'Kąt',
            lineTension: 0.3,
            borderColor: "#0200dc",
            pointRadius: 5,
            pointHoverRadius: 5,
            pointHitRadius: 20,
            pointBorderWidth: 2,
        },{
            label: 'Wartość średnia',
            lineTension: 0.1,
            borderColor: "#292929",
            pointRadius: 0,
            pointHoverRadius: 5,
            pointHitRadius: 20,
            pointBorderWidth: 2,
        },{
            label: 'Linia trendu',
            lineTension: 0.1,
            borderColor: "#b20d01",
            pointRadius: 0,
            pointHoverRadius: 5,
            pointHitRadius: 20,
            pointBorderWidth: 2,
        }],
      },
    });

    function updateData(){
        $.ajax({
            type: 'POST',
            url: '/postDataset/',
            success: function(data){
                dataAJAX = data.data
                dateAJAX = data.date
                avgAJAX = data.avg
                trendAJAX = data.trend

                myLineChart.data.datasets[0].data = dataAJAX
                myLineChart.data.datasets[1].data = avgAJAX
                myLineChart.data.datasets[2].data = trendAJAX
                myLineChart.data.labels = dateAJAX
                myLineChart.update()

            }
        });
    }

});