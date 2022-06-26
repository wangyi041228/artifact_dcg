## Artifact Classic & Foundary Deckcode Encoder & Decoder
Artifact 牌组代码的解码器和编码器，支持 Classic 和 Foundary。  
核心代码照搬，不面向对象，增加 Foundary 支持。  
虽然解码和编码支持超过5个英雄的牌组，但客户端只读取排序之后的前5个。  
虽然 Artifact 早已停止更新，但说不定会比《炉石传说》和《万智牌竞技场》更晚停服。  
Artifact 的套牌代码压缩率非常高，值得参考。此处鄙视《漫威SNAP》。  
有时间再尝试改写，看看能否提高性能。
## 用法
### 解码
    test_code = 'ADCJWkTZX05uwGDCRV4XQGy3QGLmqUBg4GQJgGLGgO7AaABR3JlZW4vQmxhY2sgRXhhbXBsZQ__'
    deck = decode.Decoder(test_code)
    print(f'名称：{deck.name}')
    print(f'版本：{deck.game!s}')
    print(f'英雄：{deck.heroes}')
    print(f'卡牌：{deck.cards}')
### 编码
    recode = encode.Encoder(deck1.heroes, deck1.cards, deck1.name, deck1.game)
    print(f'重新编码：{recode.deckcode}')
## 资料
[Artifact 的 Steam 商店页面](https://store.steampowered.com/app/583950/Artifact)  
[关于 API 公告](https://store.steampowered.com/news/app/583950/view/4549154898511384075)  
[Valve 的 php 实现](https://github.com/ValveSoftware/ArtifactDeckCode)  
[某 Python 完整实现](https://github.com/djetelina/pyArtifact)  
[某 Python 弃坑实现](https://github.com/PlumPeanut/ArtifactCard-Python3)  
[组牌站点 Artifactfire](https://www.artifactfire.com)  
[组牌站点 RedMist](https://redmist.gg)  
