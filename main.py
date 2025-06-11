from util import extract_kanji_block, read_all_srt_files, extract_words_from_srt
import pandas as pd
from tqdm import tqdm

if __name__ == "__main__":
    seen_kanji_set_tobira = "一二三四五六七八九十月私子人学生先年曜日火水木金土百千万円大小上下中外右左山川寺何時間毎明今田町花食飲言話語本持行来見週体口目耳足手回会聞読立住知入売買物音楽海国門矢貝牛男女好作出書分午前後有名父母兄弟姉妹思休悪新古高校雨雪晴度天気元病英家心帰使暗早広安親切番社長道昔友達文化末勉強着自場所茶料理肉鳥魚絵例方次最王糸集配動働走当荷由計画映仕事初東京同半士拾返守変止電車神様注意味色々世界記昨若開閉消汚乗遅困運転痛医者薬服店部屋教室続助調忘図館質問宿題試験受練習飯族夕馬取泣笑起始終決歌洗台旅駅朝昼晩夜漢字竹北南西合送活近歩急授卒業写真研究顔幸正院通考答残留重便利不弱用地球野空港両他覚貸借待落違死多少工主員去風経春夏秋冬結婚果予約定全伝感暑寒犬赤青白黒銀紙葉横職島平和温差美選建形的特市説別都州府県泳酒観光階専関身然雑誌実相難性比代表忙短必要皆敬複課面僕連絡願簡単論誰議過無発首声供解念法直苦呼技術際緒型毛周欲格遊寝将案内頼君辞現組勝成負絶対礼向育能彼与係速寄種類健康互尊含精折打投驚席迷般談輩具億在米以失敗功数増信得客流費量袋湯値段暮戦列歳商品競争境慣統混座皿紹介置式石査熱民紀倍参加個反賛宗仏祈福交換祝存歴史怒恋識殺岩戻構許割済虫丸命未深号悲静払影響欧版第亡頃鼻躍放芸愛情超降鳴傾挙機適状況血液効科減完登公逆低点常確村恥証患講義均踊劇普途偉派毒甘謝破喜追逃探突抜怖制満進協位原因求可容算等洋務率徒希望指厳庭環就給認判断述限基堂似否訪景冷区危険役省報独遠並販街及凍犯罪盗壊著氏製械宣徴批策缶導規替各税支季節非共政良泊輸候産律築装展至貿易興積極江戸郵禁録燃演植軽仲角線側頭治枚薄隠乾柔丈夫優改欠沿羽曲息吹込級爆飾態印象細夢氷詩想像接示池妻担任姿察章張飛俳句浮則素詞溶誕憶孫娘条件暖祖標束票責権期評価総臣除貧域補看板応党引退離討剣雰囲偏疑太付悩豊届再森林緑捨測栄養恐従恵齢寿延老収財労貯衛賞資源善農防募裏"
    seen_kanji_set = set(list(seen_kanji_set_tobira))
    print(f"Number of kanji already seen: {len(seen_kanji_set)}")

    directory = "/Users/mike/Downloads/[Netflix] Slam Dunk JP Subs (SRT) (Netflix Multi-Season Naming)"
    file_names, all_srt_contents = read_all_srt_files(directory)

    arr = []
    for i, file_name in tqdm(enumerate(file_names)):
        file_path = directory + "/" + file_name
        
        unique_words = extract_words_from_srt(file_path)
        
        for word, sentence, timestamp in unique_words:
            if word == None: continue

            for kanji in ''.join(extract_kanji_block(word)):
                if kanji not in seen_kanji_set:
                    seen_kanji_set.add(kanji)
                    arr.append([kanji, word, sentence, timestamp, i + 1])

    df = pd.DataFrame(arr)
    df.columns = ["kanji", "jp", "sentence", "timestamp", "episode"]

    print(len(df["kanji"].unique()))

    df.to_csv("results2.csv", index=False)