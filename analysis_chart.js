// analysis_chart.js
// 別のJSファイルだが、グローバルスコープの変数としてchartLabelsなどが参照可能
const ctx = document.getElementById('myChart').getContext('2d');

new Chart(ctx, {
    type: 'line',
    data: {
      labels: chartLabels.length === 1 ? ['', chartLabels[0], ''] : chartLabels,
      datasets: [{
        label: itemName,
        // データも配列で定義します。元のデータは chartLabels[0] の位置です
        data: chartLabels.length === 1 ?  [null, chartData[0], null] : chartData,
        borderColor: 'rgb(75, 192, 192)',
        backgroundColor: 'rgba(54, 162, 235, 0.2)',
        fill: true,
        tension: 0.1,
        pointRadius: 6,
        pointBackgroundColor: 'rgb(54, 162, 235)',
        pointBorderWidth: 2
      }]
    },
    options: {
      layout: {
        padding: {
         bottom: 20
        }
      },
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            x: {
              grid: {
                display: false
              },
              ticks: {
                align: 'center'
              },
              offset: true,
            },
            y: {
                // ここでY軸の範囲を自動調整にします(beginAtZeroを削除)
                grace: '10%', // データの最大値・最小値の外側に少し余白を作る
                
                border: {
                  display: true,
                  color: 'black'
                },

                grid: {
                  display: true,
                  color: 'rgba(0,0,0, 0.1)'
                },

                title: {
                  display: true,
                  text: itemName + 'の値' // Y軸にラベルを追加
                }
            }
        },
        plugins: {
            legend: {
                position: 'top',
            }
        }
    }
});
