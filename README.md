# 📂 業務自動化(RPA)ポートフォリオ（デモ版）

<p align="left">
  <img src="https://img.shields.io/badge/Python-3.12-blue.svg?style=for-the-badge&logo=python" alt="Python 3.12">
  <img src="https://img.shields.io/badge/PyPDF2-PDF_Manipulation-purple.svg?style=for-the-badge" alt="PyPDF2">
  <img src="https://img.shields.io/badge/reportlab-PDF_Generation-orange.svg?style=for-the-badge" alt="reportlab">
  <img src="https://img.shields.io/badge/CSV-Instruction_File-green.svg?style=for-the-badge" alt="CSV">
</p>

## 1. プロジェクト概要
大手教育機関（アルバイト先）で、**リーダーとして業務のDXを主導**したプロジェクトである。煩雑なPDFの仕分け・分割作業を自動化するRPAシステムを設計・導入し、月20時間の工数削減とヒューマンエラーの撲滅を実現した。

## 2. P：課題・背景 (Problem)
当時、私が所属してい組織では、非効率な手作業が常態化し、組織の生産性を阻害する根本的な問題となっていた。

1.  **業務上の課題:**
    「スプレッドシートの情報に基づき、社内システムから検索・保存したPDFを、手作業でページ分割・仕分けする」という非効率な業務が常態化していた。
2.  **経営上の課題:**
    この作業は**月20時間以上**の工数を要し、組織の予算（年間1000万円） を逼迫させていた。
3.  **品質上の課題:**
    手作業であるが故に、誤った仕分けによる**ヒューマンエラーが多発**し、業務品質の低下を招いていた。

## 3. A：システム構成・設計 (Action)
私はこの課題を解決するため、リーダーとして自動化システムの導入を決定。プログラミング言語の知識はゼロであったが、AI（Copilot）を「実装のパートナー」として活用し、私自身が**要件定義（設計）**を行った。

### システム構成図
![RPA_ポートフォリオ_構造図](https://github.com/user-attachments/assets/4dae4eea-f918-4d16-aaa4-74c4ef803efc)


### A-1. 要件定義（設計思想）
「人間の手作業」を「機械が読み取れる指示書」に置き換えることを設計の核とした。
1.  **指示書の自動読込:**
    人間の「勘」や「記憶」に頼るのではなく、`list_demo.csv` という**指示書CSV**を読み込み、処理すべきタスクを自動で認識させる。
2.  **PDFの自動分割:**
    指示書に記載されたページ数(NOP)に基づき、`PyPDF2`ライブラリを用いてPDFを正確に分割する。
3.  **PDFの自動仕分け:**
    分割後のPDF（AfterQ）と元のPDF（AfterE）を、指示書通りのファイル名に変更し、所定のフォルダ（`output_Q`, `output_E`）に自動で格納する。

### A-2. デモ版の設計（セキュリティ戦略）
アルバイト先の機密情報（実際のPDFや指示書）を一切含まない形で、「**課題解決のロジック**」だけを安全に証明するため、以下のデモ機能を設計・実装した（`portfolio_rpa_demo.py`）。
* **ダミーPDFの自動生成:**
    `reportlab` を使い、本来システムからダウンロードするPDFの「ダミー」を自動生成する。
* **安全な指示書:**
    実際の業務で使った指示書CSVを、機密情報を削除した `list_demo.csv` に置き換える。

## 4. R：成果 (Result)
このRPAシステムの導入により、**月20時間かかっていた作業工数をほぼ0**にし、ヒューマンエラーも撲滅することができた。

私は単にコードを書いたのではなく、「現場の課題」を特定し、「解決策を設計（要件定義）」し、「AIを活用して実装」し、「組織に導入」するという、**DX推進の全プロセスをリーダーとして完遂**した。この経験は、ITコンサルタントとしてクライアントの業務改革を推進する上で、私の核となるスキルである。

## 5. 実行手順（技術デモ）
このリポジトリのコードは、実際の業務フローを「安全なデモ版」として再現したものである。

1.  このリポジトリをダウンロードする。
2.  `portfolio_rpa_demo.py` が必要とするライブラリをインストールする。
    ```bash
    pip install PyPDF2 reportlab
    ```
3.  `portfolio_rpa_demo.py` を実行する。
    ```bash
    python portfolio_rpa_demo.py
    ```
4.  実行後、ターミナルに処理ログが表示され、`input` フォルダにダミーPDFが、`output_Q` と `output_E` フォルダに指示書通りに仕分け・分割されたPDFが自動生成されることを確認できる。

## 6. 使用技術
* **Python**
* **PyPDF2:** PDFの分割・加工
* **reportlab:** （デモ用）ダミーPDFの自動生成
* **csv:** （Python標準）指示書の読み書き
