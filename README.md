# Artifact Deckcode Encoder & Decoder for Classic & Foundry
Artifact Classic 和 Foundry 牌组代码的解码器和编码器。
* 核心代码照搬，增加 Foundry 支持，不考虑校验位、异常和错误。
* php中`strlen`取字节数（位长度），参考的Python项目有误。
* 客户端支持超过63位的牌组名称，所以本项目不设限。
* 虽然解码和编码支持超过5个英雄的牌组，但客户端只读取排序之后的前5个。
* Artifact 的套牌代码压缩率非常高，值得参考。
* `dcg.py`是将解码与编码合并的单文件版本。
* `enums.py`加`./deckcode/*`是性能稍佳的原始版本。
## 解码
    import dcg
    code = 'ADCJWkTZX05uwGDCRV4XQGy3QGLmqUBg4GQJgGLGgO7AaABR3JlZW4vQmxhY2sgRXhhbXBsZQ__'
    deck = dcg.Deck(code)
    print(f'名称：{deck.name}')
    print(f'版本：{deck.game!s}')
    print(f'英雄：{deck.heroes}')
    print(f'卡牌：{deck.cards}')
## 新建 & 编码
    heroes = [(4005, 2), (10014, 1), (10017, 3), (10026, 1), (10047, 1)]
    cards = [(3000, 2), (3001, 1), (10091, 3), (10102, 3), (10128, 3), (10165, 3), (10168, 3), (10169, 3), (10185, 3), (10223, 1), (10234, 3), (10260, 1), (10263, 1), (10322, 3), (10354, 3)]
    name = 'Green/Black Example'
    game = dcg.GameClass.CLASSIC
    deck = dcg.Deck(heroes, cards, name, game)
    print(f'编码：{deck.deckcode}')
## 修改 & 编码
    deck.heroes = []
    deck.name = '删除所有英雄'
    deck.encode()
    print(f'编码：{deck.deckcode}')
## 资料
* [Artifact 的 Steam 商店页面](https://store.steampowered.com/app/583950/Artifact)
* [关于 API 公告](https://store.steampowered.com/news/app/583950/view/4549154898511384075)
* [Valve 的 php 实现](https://github.com/ValveSoftware/ArtifactDeckCode)
* [某 Python 完整实现](https://github.com/djetelina/pyArtifact)
* [某 Python 弃坑实现](https://github.com/PlumPeanut/ArtifactCard-Python3)
* [Classic 组牌站点 Artifactfire](https://www.artifactfire.com)
* [Classic 组牌站点 RedMist](https://redmist.gg)
* [Classic Set0](https://gist.github.com/MisterJimson/6eb23814c6054ae036013c948085e3f0)
* [Classic Set1](https://gist.github.com/MisterJimson/1f9b6008dd2ad25fa804fec7e5be79f6)
* [Classic Mutation](https://gist.github.com/MisterJimson/ddcbc0f09cdadda8ba5ef1fe7c2b4f23)*
* [Foundry 非官方弃坑 API](https://github.com/aquelemiguel/artifact-beta-2.0-unofficial-api)
* [Foundry 组牌站点 ThinkArtifact](https://thinkartifact.com)
# About Artifact Mods
关于 Artifact 的模组。
* 《Artifact》和《炉石》都不主动校验本地文件，这点非常好。《LoR》和《MTGA》一开始也不校验，后来改成强制校验就更显得小肚鸡肠。又不是不能改。
* 说到这个就多说个笑话。《LoR》和《LoL》一样，看见你开'Cheat Engine'就自爆，早期版本甚至看见你开标题栏含`Cheat Engine`的网页也自爆（保）。
## 文字
* PAX West 2018 后的一次预览活动，官推送给我一个激活码。之后通过某个有提前体验资格的号拿到客户端，第一次制作了社区汉化。官中第一次出现之后隔了一阵子，大量牌名和术语居然复制了我的。因若干内容与《刀塔2》不一致，做了修订版。`GUSHCATI`分享了把评分放在牌名前方便新手。2.0发布后，我在较长时间里维护着社区汉化。官方弃坑也没维护汉化的意义了。
## 换画
* 换画原理沿袭自 Dota 2，最早来自英文社区。科学打包方式是我后来从 Dota 2 客户端里总结的。中文社区是 Yeti 在维护素材包。
* 在`gameinfo.gi`的`SearchPaths`顶部增加一行是加载MOD最简单的方法，启动项、全素材大包或全拆出来都很麻烦。
## 残局
* Classic 中后期的社区内容。
## 资料
* [Valve Resource Format](https://github.com/SteamDatabase/ValveResourceFormat)
* [Mod Guide 1](https://www.reddit.com/r/Artifact/comments/a88viy/guide_how_to_import_custom_card_art_into_artifact)
* [Mod Guide 2](https://www.reddit.com/r/Artifact/comments/ad5rcd/guide_how_to_make_custom_card_art_for_artifact)
* [Classic 残局模式](https://www.reddit.com/r/Artifact/comments/aljhm6/puzzle_smash_the_ancient_a_custom_artifact_puzzle)
# Artifact Legacies
Artifact 遗产
* 极高压缩率的套牌编码方式。
* 可能在电子卡牌对战游戏中服务器存续时间最长。
* 向长期自愿被众多游戏公司榨取价值的玩家群体提供了一个发泄对象。
* It's Moonday, my dudes.