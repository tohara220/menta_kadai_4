import pandas as pd  # CSVファイルの読み込みに使用
import sys           # プログラムの終了に使用
import datetime      # レシートファイル名に使用
import os            # ディレクトリ作成に使用

# 定数、変数
CSV_PATH = "item_master.csv"
master = '"001",りんご,100\n' + \
         '"002", なし, 120\n' + \
         '"003", みかん, 150'
RECEIPT_FOLDER = "./receipt"
os.makedirs(RECEIPT_FOLDER, exist_ok=True)

### 商品クラス
class Item:
    def __init__(self, item_code, item_name, price):
        self.item_code = item_code
        self.item_name = item_name
        self.price = price
    
    def get_price(self):
        return self.price
        
### オーダークラス
class Order:
    def __init__(self, item_master):
        self.item_order_list = []
        self.item_count_list = []
        self.item_master = item_master
        self.set_datetime()
    
    def add_item_order(self, item_code, item_count):
        self.item_order_list.append(item_code)
        self.item_count_list.append(item_count)
            
    def get_item_data(self, item_code):
        for m in self.item_master:
            if item_code == m.item_code:
                return m.item_name, m.price
    
    def input_order(self):
        # [課題2]コンソールから商品登録をさせる
        print("いらっしゃいませ!")
        while True:
            buy_item_code = input("購入したい商品を入力してください。登録を終了する場合は0を入力してください。>>>")
            if int(buy_item_code) != 0:
                # マスタに存在するかチェック
                check = self.get_item_data(str(buy_item_code).zfill(3))
                print(check)
                # get_item_dataの戻り値がNoneでなければ（登録されていれば）OK
                if check != None:
                    # リストの0番目、すなわち「商品名」が登録された旨を表示。
                    print(f"{check[0]}が登録されました。")
                    buy_item_count = input("個数を入力してください。 >>")
                    # 商品登録をする
                    self.add_item_order(str(buy_item_code).zfill(3), buy_item_count)
                # Noneならマスタにないので元に戻る
                else:
                    print(f"「{buy_item_code.zfill(3)}」は商品マスタに存在しません。")
            else:
                print("商品登録を終了します。")
                break
            
    def set_datetime(self):
        self.datetime = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
            
    def view_order(self):
        number = 1
        self.sum_price = 0
        self.sum_count = 0
        self.receipt_name = f"receipt_{self.datetime}.log"
        self.write_receipt("------------------------")
        self.write_receipt("オーダー登録された商品一覧\n")
        for item_order, item_count in zip(self.item_order_list, self.item_count_list):
            result = self.get_item_data(item_order)
            self.sum_price += result[1] * int(item_count)
            self.sum_count += int(item_count)
            receipt_data="{0}.{2}({1}) : ￥{3:,}　{4}個 = ￥{5:,}".format(number,item_order,result[0],result[1],item_count,int(result[1])*int(item_count))
            self.write_receipt(receipt_data)
            number += 1
            
        # 合計金額、個数の表示
        self.write_receipt("------------------------")
        self.write_receipt("合計金額:￥{:,} {}個".format(self.sum_price,self.sum_count))
        
    def write_receipt(self, text):
        '''
        レシートファイルとして書き込み
        '''
        print(text)
        with open(f"{RECEIPT_FOLDER}/{self.receipt_name}", mode="a", encoding="utf-8_sig") as f:
            f.write(text+"\n")
            
    def input_and_change_money(self):
        if len(self.item_order_list)>=1:
            while True:
                self.money = int(input("お預かり金額を入力してください。 >>"))
                self.change_money = self.money - self.sum_price # お釣り
                if self.change_money >= 0:
                    self.write_receipt("お預かり金:¥{:,}".format(self.money))
                    self.write_receipt("お釣り:¥{:,}".format(self.change_money))
                    break
                else:
                    print("¥{:,}不足しています。再度入力してください。".format(self.change_money))
                    
            print("お買い上げありがとうございました。")
        
    
def regist_item_csv(path):
    '''
    CSVファイルの存在確認・読み込み
    '''
    print("------- マスタ登録開始 ---------")
    item_master=[]
    try:
        item_master_df=pd.read_csv(CSV_PATH,dtype={"item_code":object}) # CSVでは先頭の0が削除されるためこれを保持するための設定
        for item_code,item_name,price in zip(list(item_master_df["item_code"]),list(item_master_df["item_name"]),list(item_master_df["price"])):
            item_master.append(Item(item_code,item_name,price))
            print(f"{item_name}({item_code})")
        print("------- マスタ登録完了 ---------")
        return item_master
    except:
        print("マスタ登録が失敗しました")
        print("------- マスタ登録完了 ---------")
        sys.exit()
            
### メイン処理
def main():
    # CSVファイルの存在確認・データ読み込み
    item_master=regist_item_csv(CSV_PATH) # CSVからマスタへ登録
    order=Order(item_master) #マスタをオーダーに登録
    
    # [課題4-2]ターミナルから商品登録
    order = Order(item_master)
    order.input_order()
    # オーダー番号から商品情報を取得する
    order.view_order()
    order.input_and_change_money()
    
    # # [課題4-1]オーダー番号から商品情報を取得する
    # print("**[課題1] オーダー番号から商品情報を取得する**")
    # for item_code in order.item_order_list:
    #     print(order.get_item_data(item_code))
    #     print(order.get_item_data(item_code))
        
if __name__ == "__main__":
    main()