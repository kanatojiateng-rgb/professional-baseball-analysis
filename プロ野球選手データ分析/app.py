from flask import Flask, render_template, request, jsonify
import pandas as pd
import json

app = Flask(__name__)

TEAM_MAP = { 
    "hanshin": ["阪神タイガース", "阪神タイガース*"],
    "giants": ["読売ジャイアンツ", "読売ジャイ*", ],
    "yakult": ["東京ヤクルトスワローズ",  "東京ヤクルト*"],
    "carp": ["広島東洋カープ", "広島東洋カープ*" ],
    "dena": ["横浜DeNAベイスターズ", "横浜ベイスターズ",  "横浜ベイスターズ*"],
    "chunichi": ["中日ドラゴンズ",  "中日ドラゴンズ*"],
    "hawks": ["福岡ソフトバンクホークス","福岡ソフトバンク*"],
    "fighters": ["北海道日本ハムファイターズ"],
    "marines": ["千葉ロッテマリーンズ",  "千葉ロッテ*"],
    "lions": ["埼玉西武ライオンズ",  "埼玉西武*"],
    "eagles": ["東北楽天ゴールデンイーグルス",  "東北楽天*"],
    "buffaloes": ["オリックスバファローズ", "オリックス*"]
}

# タイプによって読み込むCSVを判定するヘルパー関数
def get_csv_by_type(player_type):
    if player_type == 'pitcher':
        return 'pitcher_data.csv'
    return 'batter_data.csv' # デフォルトは打者

@app.route('/')
def index():
    csv_file = get_csv_by_type('batter')
    df = pd.read_csv(csv_file, encoding='UTF-8')

    exclude_columns = ['年度', 'チーム', '選手', '選手名', '投　手', 'Unnamed: 2' 'Unnamed: 16'] 
    analysis_items = [col for col in df.columns.tolist() if col not in exclude_columns]
    year_list = sorted(df['年度'].dropna().unique().tolist())
    return render_template('index.html', items=analysis_items, years=year_list)

@app.route('/get_players', methods=['GET'])
def get_players():
    team_ids = request.args.getlist('team_ids')
    start_year = int(request.args.get('start_year', 2005))
    end_year = int(request.args.get('end_year', 2026))
    player_type = request.args.get('player_type', 'batter')
    
    if not team_ids:    
        return jsonify([])
          
    try:
        csv_file = get_csv_by_type(player_type)
        df = pd.read_csv(csv_file, encoding='UTF-8')


        for col in df.columns:
            if 'チーム' in col:
                df[col] = df[col].astype(str).str.strip().str.replace('*', '', regex=False)
        
        # '年度' 列を数値型に統一
        df['年度'] = pd.to_numeric(df['年度'], errors='coerce')

        team_col_list = [col for col in df.columns if 'チーム' in col]
        if not team_col_list:
            print("エラー: CSVに 'チーム' を含む列が見つかりません")
            return jsonify([])
        team_col = team_col_list[0]
        
        #CSVの列名に '投手' があれば '投手' を、なければ '選手' を使う（どちらもなければ1番目の列）
        if '投　手' in df.columns:
            player_col = '投　手'
        elif '選手' in df.columns:
            player_col = '選手'
        elif '選手名' in df.columns:
            player_col = '選手名'   
        else:
            # 1枚目のExcel画像をベースに、C列（インデックス2）を強制指定する安全策
            player_col = df.columns[2]
        
        players_with_teams = []

        #  チームごとにループを回し、チーム名と選手リストのペアを辞書形式で作る
        for team_id in team_ids:
            team_names = TEAM_MAP.get(team_id, [])
            if not team_names:
                continue
            
            # そのチームの該当年度のデータのみを抽出
            team_df = df[
                (df[team_col].astype(str).isin(team_names)) &
                (df['年度'] >= start_year) &
                (df['年度'] <= end_year)
            ]
            
            
            raw_players = team_df[player_col].dropna().astype(str).str.strip().unique().tolist()
            filtered_players = [p for p in raw_players if p not in ['', '*', '+', '選手', '選手名', 'nan', '年度','投手']]
            
            # 選手が存在する場合のみ、チームごとにまとめてリストに追加
            if filtered_players:
                players_with_teams.append({
                    'team_name': team_names[0],
                    'player_list': filtered_players
                })
        print(f"DEBUG: 抽出されたチーム数: {len(players_with_teams)}")
        return jsonify(players_with_teams)  # グループ化されたデータを返す
    
    except Exception as e:
        print(f"エラー発生: {e}")
        return jsonify([])

@app.route('/analyze', methods=['POST'])
def analyze():
    selected_players = request.form.getlist('players')
    selected_items = request.form.getlist('items')
    player_type = request.form.get('player_type', 'batter')


    if len(selected_items) > 2:
        return "分析項目は２つまで選択してください"
    
    start_year = int(request.form.get('start_year', 2005))
    end_year = int(request.form.get('end_year', 2026))

    if start_year > end_year:
        return "開始年度は終了年度以下にしてください"
    
    csv_file = get_csv_by_type(player_type)
    df = pd.read_csv(csv_file, encoding='UTF-8')
    df['年度'] = pd.to_numeric(df['年度'], errors='coerce')
    
    if player_type == 'pitcher' and '投球回' in df.columns and 'Unnamed: 2' in df.columns:
        df['Unnamed: 2'] = pd.to_numeric(df['Unnamed: 2'], errors='coerce').fillna(0)
        df['投球回'] = pd.to_numeric(df['投球回'], errors='coerce').fillna(0)
        df['投球回'] = df['投球回'] + df['Unnamed: 2'] * (10 / 3)
    player_col = '投　手' if player_type == 'pitcher' else '選手'

    filtered_df = df[
       (df[player_col].isin(selected_players)) &
       (df['年度'] >= start_year) &
       (df['年度'] <= end_year)  
    ].sort_values('年度')

    datasets = []
    all_years = []

    for player in selected_players:
        player_df = filtered_df[filtered_df[player_col] == player]

        if not player_df.empty:
            if not all_years:
                all_years = player_df['年度'].astype(str).tolist()

        for index, item in enumerate(selected_items):
            chart_type = 'line' if index == 1 else 'bar'
            datasets.append({
                'label': f"{player} ({item})",
                'data': player_df[item].fillna(0).tolist(),
                'item': item,
                'type': chart_type,
                'fill': False,
                'tension': 0.1
            })
        
    return render_template('analysis.html',
                           item=selected_items,
                           items_json=json.dumps(selected_items, ensure_ascii=False),
                           labels=json.dumps(all_years),
                           datasets=json.dumps(datasets))

@app.route('/get_items', methods=['GET'])
def get_items():
    player_type = request.args.get('player_type', 'batter')
    try:
        # 選択されたタイプのCSVを読み込む
        csv_file = get_csv_by_type(player_type)
        df = pd.read_csv(csv_file, encoding='UTF-8')
        
        if player_type == 'pitcher' and '投球回' in df.columns and 'Unnamed: 2' in df.columns:
            df['Unnamed: 2'] = pd.to_numeric(df['Unnamed: 2'], errors='coerce').fillna(0)
            df['投球回'] = pd.to_numeric(df['投球回'], errors='coerce').fillna(0)
            df['投球回'] = df['投球回'] + df['Unnamed: 2'] * (10 / 3)

        # 除外する列
        exclude_columns = ['年度', 'チーム', '選手', '選手名', '投　手', 'Unnamed: 2','Unnamed: 16'] 
        analysis_items = [col for col in df.columns.tolist() if col not in exclude_columns]
        
        return jsonify(analysis_items)
    except Exception as e:
        print(f"項目取得エラー: {e}")
        return jsonify([])

if __name__ == '__main__':
    app.run(debug=True)