import os

CSV_PATH = "item_master.csv"

def read_csv(path):
    # CSVファイルが存在しなければ新規作成
    if not os.path.exists(path):
        with open(path, mode="w", encoding="utf-8_sig") as f:
            f.write('"001",りんご,100\n'
                    '"002",なし,120\n'
                    '"003",みかん,150\n')
    # 改行をキーにリストに格納する
    with open(path, mode="r", encoding="utf-8_sig") as f:
        csv_list = f.read().splitlines()
        print(csv_list)
        return csv_list

### 商品クラス
class Item:
    def __init__(self,item_code,item_name,price):
        self.item_code=item_code
        self.item_name=item_name
        self.price=price
    def get_num(self):
        return self.item_code
    
    def get_price(self):
        return self.price
    
    def get_name(self):
        return self.item_name

### オーダークラス
class Order:
    def __init__(self,item_master):
        self.item_order_list=[]
        self.item_master=item_master
    
    def add_item_order(self,item_code, item_cnt):
        self.item_order_list.append(item_code)
        
        
        
    def view_item_list(self):
        '''
        オーダーされた商品コードを出力
        '''
        order_list = []
        for item in self.item_order_list:
            order_list.append(item)
        return order_list
    
### メイン処理
def main():
    # マスタ登録
    item_master=[]
    # item_master.append(Item("001","りんご",100))
    # item_master.append(Item("002","なし",120))
    # item_master.append(Item("003","みかん",150))
    
    # [課題4-3] CSVから商品マスタ登録
    item_list = read_csv(CSV_PATH)
    for item in item_list:
        item =  item.split(",")
        item_master.append(Item(item[0], item[1], item[2]))
    
    
    # print(item_master[0].item_code)
    
    # # オーダー登録
    # order=Order(item_master)
    # order.add_item_order("001")
    # order.add_item_order("002")
    # order.add_item_order("003")
    
    # [課題4-2, 4-4] コンソールからオーダー登録
    order = Order(item_master)
    while True:
        order_num = input("商品番号を入力（入力を終了する場合は'n'を入力）>>")
        if order_num == "n":
            break
        elif not order_num.isdecimal():
            print("商品番号を数字で入力してください。")
            continue
        order_count = input("個数を入力してください。（商品番号を訂正する場合は'n'を入力）>>")
        if order_count == "n":
            order_num = ""
            continue
        elif not order_num.isdecimal():
            print("商品番号を数字で入力してください。")
            continue
        else:
            order.add_item_order(str(order_num).zfill(3))
            continue
    
    # [課題4-1]オーダー登録した商品の一覧（商品名・価格）を表示する
    print("---オーダー登録された商品一覧---")
    order_list = order.view_item_list()
    for i in range(len(item_master)):
        if item_master[i].item_code in order_list:
            print(f"商品コード: {item_master[i].item_code}",
                  f"商品名: {item_master[i].item_name}",
                  f"価格: {item_master[i].price}")
    
if __name__ == "__main__":
    main()