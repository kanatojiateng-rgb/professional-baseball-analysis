from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)



TEAM_MAP = { 
    "hanshin": ["阪神タイガース"],
    "giants": ["読売ジャイアンツ"],
    "yakult": ["東京ヤクルトスワローズ"],
    "carp": ["広島東洋カープ"],
    "dena": ["横浜DeNAベイスターズ","横浜ベイスターズ"],
    "chunichi": ["中日ドラゴンズ"],
    "hawks": ["福岡ソフトバンクホークス"],
    "fighters": ["北海道日本ハムファイターズ"],
    "marines": ["千葉ロッテマリーンズ"],
    "lions": ["埼玉西武ライオンズ"],
    "eagles": ["東北楽天ゴールデンイーグルス"],
    "buffaloes": ["オリックスバファローズ"]
}
@app.route('/')
def index():
    #1. CSVファイルを読み込む
    df = pd.read_csv('data.csv', encoding='UTF-8')

    #2. 分析に使う項目をリスト化する
    exclude_columns = ['年度', 'チーム', '選手', '選手名'] 
    
    analysis_items = [col for col in df.columns.tolist() if col not in exclude_columns]
    
    year_list = sorted(df['年度'].dropna().unique().tolist())
  #3. HTML(index.html)に項目リストを渡して表示させる
    return render_template('index.html', items=analysis_items, years=year_list)


@app.route('/get_players', methods=['GET'])
def get_players():
    team_id = request.args.get('team_id')
    selected_year = request.args.get('year')
    team_name_list = TEAM_MAP.get(team_id, [])


    if not team_name_list:    
        return jsonify([])
    
    try:
        # CSVを読み込む
        df = pd.read_csv('data.csv', encoding='UTF-8')
        team_col = [col for col in df.columns if 'チーム' in col][0]
        

        # チーム名でフィルタリング
        filtered_df = df[
            (df[team_col].astype(str).isin(team_name_list)) &
            (df['年度'].astype(str) == str(selected_year))
    ]
        
        # 選手名の取得
        raw_players = filtered_df['選手'].dropna().astype(str).str.strip().unique().tolist()
        
        # 不要なデータの除外
        filtered_players = [p for p in raw_players if p not in ['', '*', '+', '選手', '選手名', 'nan', '年度']]
        
        print(f"DEBUG: 検索対象のチーム名: {team_name_list}, 抽出された選手数: {len(filtered_players)}")
        return jsonify(filtered_players)  
    
    except Exception as e:
       print(f"エラー発生: {e}")
       return jsonify([])


    # フォームが送信されたときの処理を追加
@app.route('/analyze', methods=['POST'])
def analyze():
    print(f"受信した全データ: {request.form.to_dict()}")
    # HTMLの各サジェストや入力欄から値を取得（name属性をキーにする）
    selected_year = request.form.get('year')
    selected_team = request.form.get('team')
    selected_player = request.form.get('player')
    selected_item = request.form.get('item')

    # デバッグ用にコンソールに印刷（必要に応じてデータ処理やグラフ描画を行う）
    print("f 【受信データ】年度: {selected_year}, チーム: {selected_team}, 選手: {selected_player}, 項目: {selected_item}")

    # TODO: ここでCSVから条件に合うデータを抽出・分析する
    # 例: df[(df['年度']==int(selected_year)) & (df['選手名']==selected_player)]

    # ひとまず簡易的なテキストで結果を返す（実際は結果画面のHTMLをリターンするのが一般的です）
    return f"<h3>分析リクエストを受け付けました</h3>"\
           f"年度: {selected_year}<br>" \
           f"チーム（Value）: {selected_team}<br>" \
           f"選手名: {selected_player}<br>" \
           f"分析項目: {selected_item}"

if __name__ == '__main__':
    app.run(debug=True)
