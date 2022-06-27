from base64 import b64decode, b64encode
from enum import IntEnum


class GameClass(IntEnum):
    CLASSIC = 0
    FOUNDRY = 1


class Deck:
    def __init__(self, kw1=None, kw2=None, kw3=None, kw4=GameClass.CLASSIC):
        self._binary = bytearray()
        self._previous_card_base = 0
        self._point = 0
        if type(kw1) == str:
            self.deckcode = kw1
            self.heroes = []
            self.cards = []
            self.name = ''
            self.game = GameClass.CLASSIC
            self.decode()
        else:
            self.deckcode = ''
            self.heroes = kw1 if kw1 else []
            self.cards = kw2 if kw2 else []
            self.name = kw3 if kw2 else ''
            self.game = kw4
            self.encode()

    def decode(self):
        if self.deckcode.startswith('ADC'):
            self.game = GameClass.CLASSIC
            self._binary = b64decode(self.deckcode.lstrip('ADC').replace('-', '/').replace('_', '='))
        else:
            self.game = GameClass.FOUNDRY
            self._binary = b64decode(self.deckcode.lstrip('RTFACT').replace('-', '/').replace('_', '='))

        version_and_heroes = self._binary[0]
        version = version_and_heroes >> 4
        if version == 1:
            name_length = 0
            start_index = 2
            # checksum = self._binary[2]
        else:
            name_length = self._binary[2]
            start_index = 3
            # checksum = 0
        card_byte_length = len(self._binary) - name_length
        heroes_count, self._point = self._read_var_encoded(version_and_heroes, 3, start_index)

        self._previous_card_base = 0
        for _ in range(heroes_count):
            hero_turn, hero_card_id = self._read_serialized_card()
            self.heroes.append((hero_card_id, hero_turn))

        self._previous_card_base = 0
        while self._point < card_byte_length:
            card_count, card_id = self._read_serialized_card()
            self.cards.append((card_id, card_count))

        if name_length:
            self.name = self._binary[-name_length:].decode()

    def encode(self):
        if self.game == GameClass.CLASSIC:
            prefix = 'ADC'
        elif self.game == GameClass.FOUNDRY:
            prefix = 'RTFACT'
        else:
            raise ValueError
        self.heroes = sorted(self.heroes)
        self.cards = sorted(self.cards)
        self._binary = bytearray()
        self._point = 0
        version = 2 << 4 | _extract_n_bits(len(self.heroes), 3)
        self._binary.append(version)
        self._binary.append(0)
        _com_point = len(self._binary)
        self._binary.append(len(self.name.encode()))
        self._add_remaining_bits_from_number(len(self.heroes), 3)

        previous_card_id = 0
        for hero in self.heroes:
            self._add_card(hero[1], hero[0] - previous_card_id)
            previous_card_id = hero[0]

        previous_card_id = 0
        for card in self.cards:
            self._add_card(card[1], card[0] - previous_card_id)
            previous_card_id = card[0]

        name_start_index = len(self._binary)
        name_bytes = bytearray(self.name.encode())
        self._binary += name_bytes

        self._binary[1] = sum(b for b in self._binary[3:name_start_index]) & 255

        self.deckcode = (prefix + b64encode(bytes(self._binary)).decode()).replace('/', '-').replace('=', '_')

    def _read_var_encoded(self, base_value, base_bits, index):
        value = 0
        delta_shift = 0
        value, has_next = _read_bits_chunk(base_value, base_bits, delta_shift, value)
        if base_bits == 0 or has_next:
            delta_shift += base_bits
            while True:
                next_byte = self._binary[index]
                index += 1
                value, has_next = _read_bits_chunk(next_byte, 7, delta_shift, value)
                if not has_next:
                    break
                delta_shift += 7
        return value, index

    def _read_serialized_card(self):
        header = self._binary[self._point]
        self._point += 1

        card_id_delta, self._point = self._read_var_encoded(header, 5, self._point)
        card_id = self._previous_card_base + card_id_delta
        if (header >> 6) == 3:
            count, self._point = self._read_var_encoded(0, 0, self._point)
        else:
            count = (header >> 6) + 1

        self._previous_card_base = card_id
        return count, card_id

    def _add_remaining_bits_from_number(self, value: int, already_written_bits: int):
        value >>= already_written_bits
        while value > 0:
            next_byte = _extract_n_bits(value, 7)
            value >>= 7
            self._binary.append(next_byte)

    def _add_card(self, count_or_turn: int, value: int) -> None:
        first_byte_max_count = 3
        extended_count = ((count_or_turn - 1) >= first_byte_max_count)
        first_byte_count = first_byte_max_count if extended_count else (count_or_turn - 1)
        first_byte = first_byte_count << 6
        first_byte |= _extract_n_bits(value, 5)
        self._binary.append(first_byte)
        self._add_remaining_bits_from_number(value, 5)
        if extended_count:
            self._add_remaining_bits_from_number(count_or_turn, 0)


def _read_bits_chunk(chunk, numb_bits, curr_shift, out_bits):
    continue_bit = 1 << numb_bits
    new_bits = chunk & (continue_bit - 1)
    out_bits |= (new_bits << curr_shift)
    return out_bits, (chunk & continue_bit) != 0


def _extract_n_bits(value: int, num_bits: int):
    limit_bit = 1 << num_bits
    result = value & (limit_bit - 1)
    if value >= limit_bit:
        result |= limit_bit
    return result
