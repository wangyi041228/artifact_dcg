import dcg
import timeit


def main():
    test_codes = [
        'ADCJWkTZX05uwGDCRV4XQGy3QGLmqUBg4GQJgGLGgO7AaABR3JlZW4vQmxhY2sgRXhhbXBsZQ__',
        'RTFACTJVsSv7kCC0vBBPoeBay7AqgBZwIDFKYDKQkKbgJ3AYa4BXcBUrsBgSNEQ0dfUGxheXRlc3REZWNrMQ__',
    ]
    for test_code in test_codes:
        print()
        print(f'代码：{test_code}')
        deck1 = dcg.Deck(test_code)
        print(f'名称：{deck1.name}')
        print(f'版本：{deck1.game!s}')
        print(f'英雄：{deck1.heroes}')
        print(f'卡牌：{deck1.cards}')
        deck2 = dcg.Deck(deck1.heroes, deck1.cards, deck1.name, deck1.game)
        print(f'编码：{deck2.deckcode}')
        print()

    test_decks = [
        [[(4005, 2), (10014, 1), (10017, 3), (10047, 1), (10047, 1)],
         [(3000, 2), (3001, 1), (10091, 3), (10102, 3), (10128, 3), (10165, 3), (10168, 3), (10169, 3), (10185, 3),
          (10223, 1), (10234, 3), (10260, 1), (10263, 1), (10322, 3), (10354, 3)],
         'Green/Black Example',
         dcg.GameClass.CLASSIC],

        [[(10047, 3), (10058, 1), (10069, 2), (10070, 4), (11056, 5)],
         [(10092, 3), (10132, 3), (10203, 2), (10206, 1), (10226, 1), (10328, 3), (10625, 1), (10635, 1), (10713, 2),
          (10768, 2), (10774, 3), (10958, 3), (11013, 2), (11031, 2), (11090, 3), (11091, 3)],
         '#DCG_PlaytestDeck1',
         dcg.GameClass.FOUNDRY],

        [[(4005, 1)],
         [],
         '基础黑英雄',
         dcg.GameClass.CLASSIC],
    ]
    for test_deck in test_decks:
        print()
        deck1 = dcg.Deck(*test_deck)
        print(f'名称：{deck1.name}')
        print(f'版本：{deck1.game!s}')
        print(f'英雄：{deck1.heroes}')
        print(f'卡牌：{deck1.cards}')
        print(f'代码：{deck1.deckcode}')

    test_codes = [
        'ADCJWkTZX05uwGDCRV4XQGy3QGLmqUBg4GQJgGLGgO7AaABR3JlZW4vQmxhY2sgRXhhbXBsZQ__',
    ]
    for test_code in test_codes:
        print()
        print(f'代码：{test_code}')
        deck1 = dcg.Deck(test_code)
        print(f'名称：{deck1.name}')
        print(f'版本：{deck1.game!s}')
        print(f'英雄：{deck1.heroes}')
        print(f'卡牌：{deck1.cards}')
        deck1.heroes = []
        deck1.name = '**** 删除所有英雄 ****'
        deck1.encode()
        print('删除所有英雄')
        print(f'编码：{deck1.deckcode}')
        print(f'名称：{deck1.name}')
        print(f'版本：{deck1.game!s}')
        print(f'英雄：{deck1.heroes}')
        print(f'卡牌：{deck1.cards}')
        print()


def timeit_test():
    a = 0
    times_n = 100
    for _ in range(times_n):
        x = timeit.timeit(
            "decode.Decoder('ADCJWkTZX05uwGDCRV4XQGy3QGLmqUBg4GQJgGLGgO7AaABR3JlZW4vQmxhY2sgRXhhbXBsZQ__')",
            setup='from deckcode import decode', number=10_00)
        y = timeit.timeit(
            "dcg.Deck('ADCJWkTZX05uwGDCRV4XQGy3QGLmqUBg4GQJgGLGgO7AaABR3JlZW4vQmxhY2sgRXhhbXBsZQ__')",
            setup='import dcg', number=10_00)
        if x < y:
            a += 1
    print(a / 100)


if __name__ == '__main__':
    main()
    # timeit_test()
