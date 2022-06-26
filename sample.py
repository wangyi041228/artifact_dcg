from deckcode import decode, encode

test_codes = [
    'ADCJWkTZX05uwGDCRV4XQGy3QGLmqUBg4GQJgGLGgO7AaABR3JlZW4vQmxhY2sgRXhhbXBsZQ__',
    'RTFACTJVsSv7kCC0vBBPoeBay7AqgBZwIDFKYDKQkKbgJ3AYa4BXcBUrsBgSNEQ0dfUGxheXRlc3REZWNrMQ__',
]

print('虽然解码和编码支持超过5个英雄的牌组，但客户端只读取排序之后的前5个。')

for test_code in test_codes:
    print()
    print(f'测试代码：{test_code}')
    deck = decode.Decoder(test_code)
    print(f'名称：{deck.name}')
    print(f'版本：{deck.game!s}')
    print(f'英雄：{deck.heroes}')
    print(f'卡牌：{deck.cards}')
    recode = encode.Encoder(deck.heroes, deck.cards, deck.name, deck.game)
    print(f'重新编码：{recode.deckcode}')
    print()
    print('*'*20)
    print()
