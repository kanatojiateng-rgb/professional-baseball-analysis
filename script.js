// 関数定義（これ単体で実行できるようにする）
function updatePlayers() {
    const year = document.getElementById('yearSelector').value;
    const teamId = document.getElementById('teamSelector').value;
    const playerSelect = document.getElementById('player-select');

    playerSelect.innerHTML = '<option>読み込み中...</option>';

    if (!teamId) {
        playerSelect.innerHTML = '<option value="">先にチームを選択してください</option>';
        return;
    }

    
    // URLに年度も含めて送信する
    fetch(`/get_players?team_id=${teamId}&year=${year}`)
        .then(response =>  response.json())
        .then(players => {
            playerSelect.innerHTML = '<option value="">選手を選択</option>';
            players.forEach(player => {
                let option = document.createElement('option');
                option.value = player;
                option.textContent = player;
                playerSelect.appendChild(option);
            });
        })
        .catch(error => {
            console.error('Error:', error);
            playerSelect.innerHTML = '<option value="">読み込み失敗</option>';
        });
}
    // 両方の変更を監視する
document.getElementById('yearSelector').addEventListener('change', updatePlayers);
document.getElementById('teamSelector').addEventListener('change', updatePlayers);

;
