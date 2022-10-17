import requests, traceback, sys, os, json, rpc, time
from bs4 import BeautifulSoup

class DQXCharacterInfo():
    def __init__(self, characterId, server, area):
        self.characterId = characterId
        self.server = server
        self.area = area
    def printInfo(self):
        print("ID: " + self.characterId)
        print("サーバー: " + self.server)
        print("エリア: " + self.area)

class DQXClient():
    BASE_DOMAIN = "https://hiroba.dqx.jp"
    def __init__(self, token):
        self.token = token
        self.content = None
        #フレンドリストへのpathを取得
        self.httpGet("/sc/home/")
        soup = BeautifulSoup(self.content, "html.parser")
        subNaviFriendlist = soup.find(id="sub-navi-friendlist")
        if subNaviFriendlist is None:
            return
        self.friendListPath = subNaviFriendlist.find("a")["href"]
        #print(self.friendListPath)
    #GETリクエスト送信
    def httpGet(self, path):
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
            'Cookie': 'sm_open_5=' + self.token,
            'Referer': 'https://hiroba.dqx.jp/sc/'}
            with requests.get(self.BASE_DOMAIN + path, stream=True, headers=headers) as r:
                #print("レスポンスヘッダー: ")
                #for (k, v) in r.headers.items():
                #    print(f'  {k}: {v}')
                self.content = r.content.decode('utf-8')
                #f = open(os.path.dirname(__file__) + "/dqx_test.html", 'w', encoding='UTF-8')
                #f.write(self.content)
                #f.close()
            soup = BeautifulSoup(self.content, "html.parser")
            #キャラのアイコンがなければログインできてない
            icon = soup.find(id="myCharacterImg")
            if icon is None:
                print("ログイン状態が維持できていません。tokenが無効になった可能性があります")
        except:
            traceback.print_exc()
            self.content = None
    #POSTリクエスト送信
    def httpPost(self, path, payload):
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
            'Cookie': 'sm_open_5=' + self.token,
            'Referer': 'https://hiroba.dqx.jp/sc/'}
            with requests.post(self.BASE_DOMAIN + path, stream=True, params=payload, headers=headers) as r:
                #print("レスポンスヘッダー: ")
                #for (k, v) in r.headers.items():
                #    print(f'  {k}: {v}')
                self.content = r.content.decode('utf-8')
                #f = open(os.path.dirname(__file__) + "/dqx_test.html", 'w', encoding='UTF-8')
                #f.write(self.content)
                #f.close()
        except:
            traceback.print_exc()
    def getFriendsState(self):
        #https://hiroba.dqx.jp/sc/character/<cid>/friendlist/
        #からフレンドの情報を取得し、DQXCharacterInfoのリストとして返す
        result = list()
        self.httpGet(self.friendListPath)
        if self.content is None:
            #GETがうまくいかなかったら空リストを返す
            return []
        #返ってきたHTMLをパース
        soup = BeautifulSoup(self.content, "html.parser")
        myFriendList = soup.find(class_="bdBox1 myFriendList")
        friendDivs = list()
        try:
            friendDivs = myFriendList.find_all(class_="article_b")
            #該当する要素が1つだけの場合、find_all()だと例外が発生する
        except:
            friendDivs = [myFriendList.find(class_="article_b")]
        for i in friendDivs:
            boxCharaInfoTile = i.find(class_="box_charaInfo tile")
            dds = boxCharaInfoTile.find_all("dd")
            characterId = dds[1].text.replace("： ", "")
            boxServerTile = i.find(class_="box_server tile")
            dds = boxServerTile.find_all("dd")
            server = dds[0].text.replace("： ", "")
            area = dds[1].text.replace("： ", "")
            result.append(DQXCharacterInfo(characterId, server, area))
        return result
    def getFriend(self, characterId):
        #characterIdから該当するDQXCharacterInfoを返す
        #見つからなければNone
        friends = self.getFriendsState()
        for i in friends:
            if i.characterId == characterId:
                return i
        return None


f = open(os.path.dirname(__file__) + "/config.json", "r")
config = json.load(f)
f.close()
dqxc = DQXClient(config["friend_token"])
rpc_obj = rpc.DiscordIpcClient.for_platform("1031486521867517993")
#15秒おきにループを実行
while True:
    targetState = dqxc.getFriend(config["target_character_id"])
    if targetState is None:
        rpc_obj.set_activity({
            "state": "ログイン状況不明",
            "assets" : {
                "large_image" : "dqx_icon",
                "large_text": "DQX オンライン"}
        })
    else:
        targetState.printInfo()
        if targetState.area == "--" and targetState.server == "--":
            rpc_obj.set_activity({
                "state": "ログアウト中",
                "assets" : {
                    "large_image" : "dqx_icon",
                    "large_text": "DQX オンライン"}
            })
        else:
            rpc_obj.set_activity({
            "state": targetState.server + "　" + targetState.area,
            "assets" : {
                "large_image" : "dqx_icon",
                "large_text": "DQX オンライン"}
        })
    time.sleep(15)
