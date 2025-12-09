import json
import os
from datetime import datetime

# --- 配置 ---
DATA_FILE = 'account_records.json'  # 儲存記錄的檔案名稱

# --- 數據操作 ---
def load_records():
    """載入現有的記錄或建立一個空的列表。"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            try:
                # 嘗試從檔案載入 JSON 數據
                records = json.load(f)
                print(f"已載入 {len(records)} 條記錄。")
                return records
            except json.JSONDecodeError:
                # 如果檔案損壞或為空，則返回空列表
                print("警告：記錄檔案損壞，將從零開始建立新記錄。")
                return []
    return []

def save_records(records):
    """將當前記錄儲存到 JSON 檔案中。"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        # 使用 json.dump 格式化儲存，ensure_ascii=False 確保中文正常顯示
        json.dump(records, f, ensure_ascii=False, indent=4)
    print("\n--- 記錄已儲存 ---")

# --- 核心功能：記錄交易 ---
def record_transaction(records):
    """接收使用者的輸入並將交易記錄加入列表。"""
    print("\n--- 記錄新的交易 ---")

    # 1. 輸入種類 (確保有輸入)
    category = input("請輸入種類 (例如：餐飲, 交通, 收入)：").strip() or "未分類"

    # 2. 輸入金額 (確保是有效數字)
    while True:
        try:
            amount_str = input("請輸入金額：").strip()
            amount = float(amount_str)
            if amount <= 0:
                print("金額必須大於零。")
                continue
            break
        except ValueError:
            print("金額輸入無效，請輸入數字。")

    # 3. 輸入數量 (確保是有效整數，預設為 1)
    while True:
        try:
            quantity_str = input("請輸入數量 (預設為 1)：").strip() or '1'
            quantity = int(quantity_str)
            if quantity < 1:
                print("數量必須大於等於 1。")
                continue
            break
        except ValueError:
            print("數量輸入無效，請輸入整數。")

    # 4. 輸入日期 (預設為今天)
    date_str = input("請輸入日期 (格式 YYYY-MM-DD，留空則為今天)：").strip()
    if not date_str:
        date_str = datetime.now().strftime('%Y-%m-%d')

    new_record = {
        'category': category,
        'amount': amount,
        'quantity': quantity,
        'total': amount * quantity,
        'date': date_str
    }

    records.append(new_record)
    print(f"\n成功記錄：[{date_str}] {category} | 總額: {amount * quantity}。")

# --- 顯示功能 ---
def display_records(records):
    """將所有記錄顯示在終端機上。"""
    if not records:
        print("\n--- 目前沒有任何記錄 ---")
        return

    print("\n--- 所有交易記錄 ---")
    for i, r in enumerate(records):
        print(f"{i+1:2}. [{r['date']}] {r['category']:10} | 單價: {r['amount']:7.2f} x 數量: {r['quantity']} | 總額: {r['total']:7.2f}")
    print("-" * 40)

# --- 主選單與程式運行 ---
def main():
    """程式的主運行函數。"""
    records = load_records()  # 載入所有現有記錄

    while True:
        print("\n=== 簡易記帳本 ===")
        print("1. 記錄一筆交易")
        print("2. 顯示所有記錄")
        print("3. 退出並儲存")
        print("=" * 20)

        choice = input("請選擇功能 (1-3)：").strip()

        if choice == '1':
            record_transaction(records)
        elif choice == '2':
            display_records(records)
        elif choice == '3':
            save_records(records)
            break
        else:
            print("輸入無效，請輸入 1 到 3 之間的數字。")

if __name__ == "__main__":
    main()