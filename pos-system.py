import pandas as pd
import datetime
import os

# 定数、変数
now = datetime.datetime.now()
ymdhms = f"{now:%Y%m%d%H%M%S}"
CSV_PATH = "item_master.csv"
RECEIPT_DIR = "./receipt"
receipt_path = RECEIPT_DIR + f"/{ymdhms}.log"

### 商品クラス
class Item:
    def __init__(self,item_code,item_name,price):
        self.item_code=item_code
        self.item_name=item_name
        self.price=price
        
    def get_price(self):
        return self.price

### オーダークラス
class Order:
    def __init__(self,item_master):
        # 商品マスタ
        self.item_master=item_master
        self.item_master_code_list = []
        # オーダー
        self.item_order_list=[]
        self.item_order_quantity_list = []
        self.total_price = 0
        self.total_quantity = 0
    def add_item_order(self,item_code):
        '''オーダーした商品をリストに追加（商品番号のみ）'''
        self.item_order_list.append(item_code)
        
    def add_item_quantity(self, quantity):
        '''オーダー数量を記録'''
        self.item_order_quantity_list.append(quantity)
        
    def view_item_list(self):
        for item in self.item_order_list:
            print("商品コード:{}".format(item))
    
    def view_name_price(self, item_code):
        '''オーダー済み商品の名前、価格を表示する'''
        for m in self.item_master:
            if m.item_code == item_code:
                return m.item_name, m.price
            
    def view_order_list(self):
        '''オーダーした商品の一覧と合計を表示 + レシート出力'''
        # レシートの見出しを出力
        make_receipt("----------\nご注文明細")
        # 注文済み商品の商品番号と数量をループで回す
        for code, quantity in zip(self.item_order_list, self.item_order_quantity_list):
            # 商品番号より商品名と価格を呼び出す
            name, price = self.view_name_price(code)
            # コンソールに情報を表示
            print(f"[{name} ¥{price}] {quantity}個")
            # レシートに追記
            make_receipt(f"[{name} ¥{price}] {quantity}個")
            # 合計金額に加算
            self.total_price += (int(price) * int(quantity))
            # 合計数量に加算
            self.total_quantity += int(quantity)
            
        # コンソール画面に表示
        print(f"[合計金額:{self.total_price}, 合計数量:{self.total_quantity}]")
        # レシートに追記
        make_receipt(f"[合計金額:{self.total_price}, 合計数量:{self.total_quantity}]")
        
    def pay(self):
        '''受け取り金額の入力とお釣りの計算 + レシート追記'''
        receive = input(f"お支払い金額は¥{self.total_price}です。受け取り金額を入力してください。 >>")
        oturi = int(receive) - int(self.total_price)
        # コンソール画面に表示
        print(f"お釣りは{oturi}です。ありがとうございました。")
        # レシートに追記
        make_receipt(f"[お受け取り金額:{receive},お釣り:{oturi}]\n----------")
                
    def order_from_console(self):
        '''コンソール画面からオーダー登録をする'''
        # マスタリスト（商品コードのみ）を作成する
        for item_obj in self.item_master:
            self.item_master_code_list.append(item_obj.item_code)
        print("--- オーダー ---")
        while True:
            input_num = input("商品コードを入力してください。（'n'キーでオーダーストップ）>>")
            if input_num == "n":
                print("--- オーダーを終了します。 ---")
                break
            ### オーダー登録する
            if input_num in self.item_master_code_list:
                # 数量を入力
                input_qt = input("続いて注文数量を入力してください。 >>")
                if str(input_qt).isdecimal():
                    self.add_item_quantity(input_qt)
                    # 商品番号を登録
                    self.add_item_order(input_num)
                    print("商品の登録が完了しました。")
                else:
                    print("個数が正しく入力されていません。最初からやり直してください。")
                    continue
            else:
                print("商品コードが不正です。番号を再確認の上、登録してください。")
                
def item_master_from_csv():
    '''CSVファイルからマスタ登録する'''
    item_master = []
    df = pd.read_csv(CSV_PATH)
    print("--- 商品マスタ登録 ---")
    for code, name, price in zip(list(df["item_code"]), list(df["item_name"]), list(df["price"])):
        item_master.append(Item(str(code).zfill(3), name, price))
        print(str(code).zfill(3), name, price)
    print("--- 商品マスタ登録完了 ---")
    return item_master

def make_receipt(txt):
    with open(receipt_path, mode="a", encoding="utf-8_sig")as f:
        f.write(txt + "\n")
            
### メイン処理
def main():
    # ディレクトリ作成
    os.makedirs(RECEIPT_DIR, exist_ok=True)
    # [課題3]CSVファイルよりマスタ登録する
    item_master = item_master_from_csv()
    # オーダー登録
    order=Order(item_master)
    # [課題2]コンソール画面よりオーダーを受け付ける
    order.order_from_console()
    
    # # [課題1]オーダーした商品の商品名と価格を表示する
    # for item_num in order.item_order_list:
    #     print(order.view_name_price(item_num))
    
    # [課題5] オーダー登録した商品の商品名、価格を表示し、かつ合計金額、個数を表示できるようにしてください
    print("--- ご注文明細 ---")
    order.view_order_list()
    # お釣りの計算等
    order.pay()
    
if __name__ == "__main__":
    main()