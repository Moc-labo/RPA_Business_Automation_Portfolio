# =============================================================================
# ポートフォリオ：RPAデモ（CSV指示書に基づくPDFの自動生成・分割・仕分け）
# =============================================================================
#
# 【このコードが行うこと】
# 1. `list_demo.csv` という指示書を読み込みます。
# 2. 「ダウンロード」のシミュレーションとして、ダミーのPDFを `input` フォルダに自動生成します。
# 3. `PyPDF2` を使い、指示書の「NOP（ページ数）」に従ってPDFを分割します。
# 4. 完成したファイルを `output_Q` と `output_E` フォルダに仕分けします。
#
# =============================================================================

import os
import csv
import shutil
from pathlib import Path
from tqdm import tqdm

# ▼▼▼ ポートフォリオでアピールする技術 ▼▼▼
# 1. PyPDF2（PDFを加工するライブラリ）
#    （※もしインストールしていなければ、VSコードのターミナルで `pip install PyPDF2` を実行してください）
import PyPDF2 
#
# 2. reportlab（ダミーのPDFを「生成」するためのライブラリ）
#    （※もしインストールしていなければ、`pip install reportlab` を実行してください）
from reportlab.pdfgen import canvas

# -----------------------------------------------------------------------------
# 1. 設定（フォルダ名やファイル名）
# -----------------------------------------------------------------------------
# 設計思想（フォルダ構成）をそのまま使います
INPUT_DIR = "input"
OUTPUT_Q_DIR = "output_Q"
OUTPUT_E_DIR = "output_E"
CSV_FILE = "list_demo.csv" # ポートフォリオ用のダミー指示書

# -----------------------------------------------------------------------------
# 2. CSV指示書（list_demo.csv）の自動生成
# -----------------------------------------------------------------------------
def create_demo_csv_if_not_exists():
    """ポートフォリオ用の「ダミー指示書」を自動生成する関数"""
    if os.path.exists(CSV_FILE):
        return # 既にファイルがあれば何もしない
    
    print(f"✅ ポートフォリオ用のダミー指示書『{CSV_FILE}』を作成します...")
    # CSVのカラム名（設計）を、安全な名前に変更します
    demo_data = [
        {'No': 1, 'File_ID': 'A-001', 'Document_Name': '仕様書_Alpha', 'Pages_to_Split': 3, 'Output_Q_Name': 'REQ-A001', 'Output_E_Name': 'SPEC-A001'},
        {'No': 2, 'File_ID': 'B-002', 'Document_Name': '契約書_Beta', 'Pages_to_Split': 5, 'Output_Q_Name': 'REQ-B002', 'Output_E_Name': 'SPEC-B002'},
        {'No': 3, 'File_ID': 'C-003', 'Document_Name': 'マニュアル_Gamma', 'Pages_to_Split': 1, 'Output_Q_Name': 'REQ-C003', 'Output_E_Name': 'SPEC-C003'},
    ]
    
    try:
        with open(CSV_FILE, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=demo_data[0].keys())
            writer.writeheader()
            writer.writerows(demo_data)
        print(f"   > 『{CSV_FILE}』が作成されました。")
    except Exception as e:
        print(f"❌ ダミー指示書の作成に失敗しました: {e}")

# -----------------------------------------------------------------------------
# 3. ダミーPDFの自動生成（＝ダウンロードの「シミュレーション」）
# -----------------------------------------------------------------------------
def simulate_download(filename, total_pages=10):
    """
    「Seleniumでのダウンロード」の代わりに、ダミーのPDFを生成する関数。
    これが  `download.py` の役割を代替します。
    """
    pdf_path = Path(INPUT_DIR) / f"{filename}.pdf"
    try:
        c = canvas.Canvas(str(pdf_path))
        for i in range(1, total_pages + 1):
            c.drawString(100, 750, f"これはダミーのPDFファイルです。")
            c.drawString(100, 730, f"ファイル名: {filename}.pdf")
            c.drawString(500, 50, f"ページ {i} / {total_pages}")
            c.showPage() # これで1ページが確定し、次のページに移る
        c.save()
        return pdf_path
    except Exception as e:
        print(f"❌ ダミーPDFの生成に失敗 ({filename}.pdf): {e}")
        return None

# -----------------------------------------------------------------------------
# 4. 設計した「PDF分割」ロジック（pdf_processor.py の核）
# -----------------------------------------------------------------------------
def split_pdf(input_pdf_path, pages_to_split, output_q_folder, output_q_name):
    """
     `split_pdf` のロジック。
    指示されたページ数(NOP)でPDFを分割する、「スゴさ」の部分です。
    """
    try:
        with open(input_pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            total_pages = len(pdf_reader.pages)
            
            # 実装していた、ページ数を超えた場合の安全装置
            if pages_to_split > total_pages:
                print(f"   > 警告: 指示ページ数({pages_to_split})が総ページ数({total_pages})を超過。全ページ({total_pages}P)を対象にします。")
                pages_to_split = total_pages
            
            pdf_writer = PyPDF2.PdfWriter()
            # ロジック：先頭から指示されたページ分だけループ
            for page_num in range(pages_to_split):
                pdf_writer.add_page(pdf_reader.pages[page_num])
            
            # ロジック：指示された名前で `output_Q` フォルダに保存
            afterq_path = Path(output_q_folder) / f"{output_q_name}.pdf"
            with open(afterq_path, 'wb') as output_file:
                pdf_writer.write(output_file)
            
            return afterq_path
            
    except Exception as e:
        print(f"❌ PDF分割中にエラー ({input_pdf_path.name}): {e}")
        return None

# -----------------------------------------------------------------------------
# 5. 設計した「PDFコピー」ロジック（pdf_processor.py の核）
# -----------------------------------------------------------------------------
def copy_original_pdf(input_pdf_path, output_e_folder, output_e_name):
    """
     `rename_original_pdf` のロジック。
    元のPDFを `output_E` フォルダにコピー（仕分け）します。
    """
    try:
        aftere_path = Path(output_e_folder) / f"{output_e_name}.pdf"
        shutil.copy2(input_pdf_path, aftere_path)
        return aftere_path
    except Exception as e:
        print(f"❌ PDFコピー中にエラー ({input_pdf_path.name}): {e}")
        return None

# -----------------------------------------------------------------------------
# 6. メイン処理（全体の司令塔）
# -----------------------------------------------------------------------------
def main():
    """メイン処理"""
    print("🚀 ポートフォリオ用RPAデモを開始します...")
    
    # 設計：まず指示書（CSV）を準備
    create_demo_csv_if_not_exists()
    
    # 設計：必要なフォルダを準備
    Path(INPUT_DIR).mkdir(exist_ok=True)
    Path(OUTPUT_Q_DIR).mkdir(exist_ok=True)
    Path(OUTPUT_E_DIR).mkdir(exist_ok=True)
    
    # 設計（load_config_from_csv）：指示書を読み込む
    try:
        with open(CSV_FILE, 'r', encoding='utf-8-sig') as f:
            # 使っていた `csv.DictReader` を使います
            reader = csv.DictReader(f)
            configs = list(reader)
        if not configs:
            print(f"❌ 指示書『{CSV_FILE}』が空です。処理を中止します。")
            return
    except Exception as e:
        print(f"❌ 指示書『{CSV_FILE}』の読み込みに失敗: {e}")
        return

    print(f"✅ 指示書から {len(configs)} 件のタスクを読み込みました。処理を開始します。")
    
    # 設計（for config in ...）：指示書を1件ずつループ処理
    for config in tqdm(configs, desc="RPA処理中", unit="件"):
        try:
            # --- 1. ダウンロードのシミュレーション ---
            # （面接官に「実際はここをSeleniumで自動化しました」と説明する部分）
            print(f"\n[タスク: {config['File_ID']}]")
            print(f"   > 1. 「ダウンロード」をシミュレート中...")
            
            # 設計（命名規則）：`年度_大学名...` の代わりに `File_ID` を使います
            base_filename = f"{config['File_ID']}_{config['Document_Name']}" 
            dummy_pdf_path = simulate_download(base_filename, total_pages=10)
            
            if not dummy_pdf_path:
                print(f"   > スキップ: ダミーPDFの生成に失敗しました。")
                continue
            
            print(f"   > 1. 完了: 『{dummy_pdf_path.name}』をinputフォルダに準備しました。")

            # --- 2. PDFの自動分割（ `pdf_processor.py` のロジック） ---
            print(f"   > 2. 「PDF自動分割」を開始...")
            
            # 設計：指示書から分割ページ数（NOP）と出力ファイル名（AfterQ）を取得
            pages_to_split = int(config['Pages_to_Split'])
            output_q_name = config['Output_Q_Name']
            
            split_path = split_pdf(dummy_pdf_path, pages_to_split, OUTPUT_Q_DIR, output_q_name)
            
            if not split_path:
                print(f"   > スキップ: PDFの分割に失敗しました。")
                continue
                
            print(f"   > 2. 完了: 『{split_path.name}』をoutput_Qフォルダに保存しました。({pages_to_split}ページ)")

            # --- 3. 元PDFの仕分け（ `pdf_processor.py` のロジック） ---
            print(f"   > 3. 「元PDFの仕分け」を開始...")
            
            # 設計：指示書から出力ファイル名（AfterE）を取得
            output_e_name = config['Output_E_Name']
            
            copy_path = copy_original_pdf(dummy_pdf_path, OUTPUT_E_DIR, output_e_name)
            
            if not copy_path:
                print(f"   > スキップ: 元PDFのコピーに失敗しました。")
                continue
            
            print(f"   > 3. 完了: 『{copy_path.name}』をoutput_Eフォルダに保存しました。")
            
            # 安全のため、元のダミーPDFを削除
            os.remove(dummy_pdf_path)

        except Exception as e:
            print(f"❌ タスク {config['File_ID']} の処理中に予期せぬエラー: {e}")

    print("\n🎉 全てのデモ処理が完了しました！")
    print(f"   > 結果は '{OUTPUT_Q_DIR}' と '{OUTPUT_E_DIR}' フォルダを確認してください。")

# -----------------------------------------------------------------------------
# 7. このスクリプト自体を実行可能にする
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    main()