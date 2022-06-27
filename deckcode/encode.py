from base64 import b64encode
from enums import GameClass


class Encoder:
    def __init__(self, heroes, cards, name='', game=GameClass.CLASSIC):
        if game == GameClass.CLASSIC:
            prefix = 'ADC'
        elif game == GameClass.FOUNDRY:
            prefix = 'RTFACT'
        else:
            raise ValueError
        self.heroes = sorted(heroes)
        self.cards = sorted(cards)
        self.name = name
        self.array = bytearray()
        version = 2 << 4 | _extract_n_bits(len(heroes), 3)
        self.array.append(version)
        self.array.append(0)
        _com_point = len(self.array)
        self.array.append(len(self.name.encode()))
        self._add_remaining_bits_from_number(len(self.heroes), 3)

        previous_card_id = 0
        for hero in self.heroes:
            self._add_card(hero[1], hero[0] - previous_card_id)
            previous_card_id = hero[0]

        previous_card_id = 0
        for card in self.cards:
            self._add_card(card[1], card[0] - previous_card_id)
            previous_card_id = card[0]

        name_start_index = len(self.array)
        name_bytes = bytearray(self.name.encode())
        self.array += name_bytes

        self.array[1] = sum(b for b in self.array[3:name_start_index]) & 255

        self.deckcode = (prefix + b64encode(bytes(self.array)).decode()).replace('/', '-').replace('=', '_')

    def _add_remaining_bits_from_number(self, value: int, already_written_bits: int):
        value >>= already_written_bits
        while value > 0:
            next_byte = _extract_n_bits(value, 7)
            value >>= 7
            self.array.append(next_byte)

    def _add_card(self, count_or_turn: int, value: int) -> None:
        first_byte_max_count = 3
        extended_count = ((count_or_turn - 1) >= first_byte_max_count)
        first_byte_count = first_byte_max_count if extended_count else (count_or_turn - 1)
        first_byte = first_byte_count << 6
        first_byte |= _extract_n_bits(value, 5)
        self.array.append(first_byte)
        self._add_remaining_bits_from_number(value, 5)
        if extended_count:
            self._add_remaining_bits_from_number(count_or_turn, 0)


def _extract_n_bits(value: int, num_bits: int):
    limit_bit = 1 << num_bits
    result = value & (limit_bit - 1)
    if value >= limit_bit:
        result |= limit_bit
    return result


if __name__ == '__main__':
    _a = [(4005, 2), (10014, 1), (10017, 3), (10026, 1), (10047, 1)]
    _a1 = [(10014, 1), (10017, 3), (10026, 1), (4005, 2), (10047, 1), (10014, 1), (10017, 3), (10026, 1), (4005, 2),
           (10047, 1), (10014, 1), (10017, 3), (10026, 1), (4005, 2), (10047, 1)]
    _b = [(3000, 2), (3001, 1), (10091, 3), (10102, 3), (10128, 3), (10165, 3),
          (10168, 3), (10169, 3), (10185, 3), (10223, 1), (10234, 3), (10260, 1),
          (10263, 1), (10322, 3), (10354, 3)]
    _c = 'Green/Black Example'
    Encoder(_a, _b, _c, GameClass.CLASSIC)
    Encoder(_a1, _b, _c, GameClass.CLASSIC)
