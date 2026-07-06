// analysis_chart.js
// 別のJSファイルだが、グローバルスコープの変数としてchartLabelsなどが参照可能
const ctx = document.getElementById('myChart').getContext('2d');

console.log(chartLabels);
console.log(chartDatasets);console.log(chartLabels);

const itemLeft = selectedItems[0] || "項目１";
const itemRight = selectedItems[1] || "項目２";

// シンプルで洗練されたカラーパレット（最大3選手分を想定）
// 折れ線用（濃いめ・はっきり）
const lineColors = [
  '#004488', // 濃いブルー
  '#D4A373', // 落ち着いたゴールド
  '#2A9D8F'  // 深みのあるミント
];
// 棒グラフ用（薄め・スタイリッシュなグレー〜ネイビー系）
const barColors = [
  'rgba(142, 154, 175, 0.5)', // ニュアンスグレー
  'rgba(163, 177, 138, 0.5)', // セージグリーン
  'rgba(202, 210, 197, 0.5)'  // ライトグレー
];

new Chart(ctx, {
    type: 'bar',
    data: {
      labels: chartLabels,
      // datasetsのmap処理で、軸の振り分けととデザインを行う
      datasets: chartDatasets.map((ds, index) => {

        const isRightAxis = (selectedItems.length > 1 && ds.item === itemRight);
        const colorIndex = Math.floor(index / selectedItems.length) % 3; // 選手ごとに色を分ける計算
        
        return {
          label: ds.label,
          data: ds.data,
        
        type: isRightAxis ? 'line' : 'bar',
        yAxisID: isRightAxis ? 'y1' : 'y',

        // 色をシンプルかつ視認性高く設定
        borderColor: isRightAxis ? lineColors[colorIndex]: 'transparent',
        backgroundColor: isRightAxis ? lineColors[colorIndex]: barColors[colorIndex],

        // ★ 折れ線グラフをより見やすくするための調整
          tension: 0.15,         // 線をほんの少し滑らかに
          borderWidth: isRightAxis ? 4 : 0, // 折れ線の線を太く（4px）して強調
          pointRadius: isRightAxis ? 6 : 0, // 棒グラフのときはポインター点を消す
          pointHoverRadius: 8,
          pointBackgroundColor: isRightAxis ? lineColors[colorIndex] : 'transparent',
          pointBorderColor: '#ffffff', // 線のポインターに白いフチをつけて見やすく
          pointBorderWidth: 2,

          order: isRightAxis ? 1:2 // 折れ線（１）を棒グラフ（２）より手前に描画
      };
    })
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
              grid: {display: false },
              ticks: {
                align: 'center',
                color: '#666666' },
              offset: true,
            },
            // 左Y軸の設定
            y: {
                type: 'linear',
                position: 'left',
                grace: '10%',
                border: { display: false },
                grid: { display: true, color: 'rgba(0,0,0, 0.05)' },
                title: {
                  display: true,
                  text: itemLeft, 
                  color: '#333333',
                  font: { weight: 'bold' }
                }
            },
            // 右Y軸の設定（2つ目の項目がある場合のみ表示）
            y1: {
                type: 'linear',
                position: 'right',
                grace: '10%',
                display: selectedItems.length > 1, // 2項目以上選ばれた時だけ右軸を出す
                border: { display: false },
                grid: { display: false },
                title: {
                  display: true,
                  text: itemRight,
                  color: '#333333',
                  font: {weight: 'bold'}
                }
            }
        },
        plugins: {
            legend: {
                position: 'top',
                labels: {
                  boxWidth: 15,
                  font: { size: 12 }
                }
            }
        }
    } 
});