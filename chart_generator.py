import matplotlib.pyplot as plt
import json
import os

# 必須與 account_app.py 中的檔案名稱一致
DATA_FILE = 'account_records.json'
plt.rcParams['font.family'] = ['Microsoft JhengHei'] 
def load_records_from_file():
    """
    從 JSON 檔案中讀取所有記帳記錄。
    
    Returns:
        list: 記錄列表，如果檔案不存在或損壞則返回空列表。
    """
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            try:
                # 嘗試載入數據
                return json.load(f)
            except json.JSONDecodeError:
                print("錯誤：記錄檔案損壞或為空。")
                return []
    else:
        print(f"錯誤：找不到記錄檔案 '{DATA_FILE}'，請先執行記帳程式。")
        return []

def generate_pie_chart(records):
    """
    根據傳入的記錄列表生成並顯示圓餅圖。
    
    Args:
        records (list): 包含交易字典的列表。
    """
    if not records:
        print("\n記錄為空，無法生成圓餅圖。")
        return

    # 1. 數據聚合：計算各類別的總支出/收入
    category_totals = {}
    for record in records:
        # 使用 .get() 確保安全讀取，即使欄位缺失也不會崩潰
        cat = record.get('category', '未分類')
        total = record.get('total', 0)
        
        # 排除 total 為 0 的記錄
        if total != 0:
            category_totals[cat] = category_totals.get(cat, 0) + total
    
    if not category_totals:
        print("\n所有記錄的總額皆為零，無法生成圓餅圖。")
        return

    # 2. 準備繪圖數據
    labels = category_totals.keys()
    sizes = category_totals.values()
    
    # 3. 繪圖設定與顯示 [Image of 圓餅圖範例]
    plt.figure(figsize=(10, 6)) # 設定圖表大小
    
    # 繪製圓餅圖：
    # autopct='%1.1f%%'：在圖上顯示百分比
    # startangle=90：從上方開始繪製
    # pctdistance=0.85：調整百分比文字與圓心的距離
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, pctdistance=0.85)
    
    plt.axis('equal')  # 確保圓餅圖是圓形的
    plt.tight_layout() # 自動調整佈局
    plt.show()

# 程式的啟動點
if __name__ == "__main__":
    # 步驟 1: 載入數據
    current_records = load_records_from_file()
    
    # 步驟 2: 生成圖表
    generate_pie_chart(current_records)