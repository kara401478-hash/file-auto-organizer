import os
import shutil
from pathlib import Path
from datetime import datetime

# ファイル種別の定義
FILE_CATEGORIES = {
    '画像': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'],
    '文書': ['.pdf', '.docx', '.doc', '.xlsx', '.xls', '.pptx', '.txt'],
    '動画': ['.mp4', '.avi', '.mov', '.mkv', '.wmv'],
    '音楽': ['.mp3', '.wav', '.flac', '.aac'],
    'プログラム': ['.py', '.js', '.html', '.css', '.java', '.cpp'],
    'その他': []
}

def get_category(extension):
    """拡張子からカテゴリを取得する"""
    for category, extensions in FILE_CATEGORIES.items():
        if extension.lower() in extensions:
            return category
    return 'その他'

def organize_files(source_dir, output_dir):
    """ファイルを仕分けする"""
    os.makedirs(output_dir, exist_ok=True)
    log = []
    count = 0

    for filename in os.listdir(source_dir):
        filepath = os.path.join(source_dir, filename)
        if os.path.isfile(filepath):
            ext = Path(filename).suffix
            category = get_category(ext)
            dest_dir = os.path.join(output_dir, category)
            os.makedirs(dest_dir, exist_ok=True)
            dest_path = os.path.join(dest_dir, filename)

            # 同名ファイルが存在する場合はリネーム
            if os.path.exists(dest_path):
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                name, ext = os.path.splitext(filename)
                filename = f"{name}_{timestamp}{ext}"
                dest_path = os.path.join(dest_dir, filename)

            shutil.copy2(filepath, dest_path)
            log_msg = f"✅ {filename} → {category}/"
            print(log_msg)
            log.append(log_msg)
            count += 1

    return log, count

def rename_files(directory, prefix):
    """ファイルを一括リネームする"""
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    for i, filename in enumerate(sorted(files), 1):
        ext = Path(filename).suffix
        new_name = f"{prefix}_{i:03d}{ext}"
        old_path = os.path.join(directory, filename)
        new_path = os.path.join(directory, new_name)
        os.rename(old_path, new_path)
        print(f"✅ {filename} → {new_name}")

def save_log(log, filepath):
    """ログを保存する"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"処理日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 40 + "\n")
        for line in log:
            f.write(line + "\n")
    print(f"✅ ログを保存しました: {filepath}")

def create_sample_files():
    """サンプルファイルを生成する"""
    os.makedirs('data', exist_ok=True)
    sample_files = [
        'data/photo1.jpg', 'data/photo2.png',
        'data/document1.pdf', 'data/document2.docx',
        'data/video1.mp4', 'data/script1.py',
        'data/music1.mp3', 'data/other1.zip'
    ]
    for f in sample_files:
        Path(f).touch()
    print(f"✅ サンプルファイルを生成しました: {len(sample_files)}件")

def main():
    print("📁 ファイル自動仕分けツール起動")
    print("=" * 40)

    # サンプルファイル生成
    create_sample_files()

    # ファイル仕分け
    print("\n🔄 仕分け開始...")
    log, count = organize_files('data', 'output')

    # ログ保存
    save_log(log, 'output/log.txt')

    print(f"\n🎉 完了！{count}件のファイルを仕分けしました。")
    print("outputフォルダを確認してください。")

if __name__ == "__main__":
    main()
