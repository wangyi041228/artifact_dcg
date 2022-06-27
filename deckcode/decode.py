from base64 import b64decode
from enums import GameClass


def _read_bits_chunk(chunk, numb_bits, curr_shift, out_bits):
    continue_bit = 1 << numb_bits
    new_bits = chunk & (continue_bit - 1)
    out_bits |= (new_bits << curr_shift)
    return out_bits, (chunk & continue_bit) != 0


class Decoder:
    def __init__(self, deckcode):
        self.deckcode = deckcode
        self.decoded = None
        self._previous_card_base = 0
        self.game = None
        self.heroes = []
        self.cards = []
        self.name = ''
        self.point = 0
        self.decode(deckcode)

    def decode(self, deckcode):
        if deckcode.startswith('ADC'):
            self.game = GameClass.CLASSIC
            self.decoded = b64decode(deckcode.lstrip('ADC').replace('-', '/').replace('_', '='))
        else:
            self.game = GameClass.FOUNDRY
            self.decoded = b64decode(deckcode.lstrip('RTFACT').replace('-', '/').replace('_', '='))

        version_and_heroes = self.decoded[0]
        version = version_and_heroes >> 4
        if version == 1:
            name_length = 0
            start_index = 2
            # checksum = self.decoded[2]
        else:
            name_length = self.decoded[2]
            start_index = 3
            # checksum = 0
        card_byte_length = len(self.decoded) - name_length
        heroes_count, self.point = self._read_var_encoded(version_and_heroes, 3, start_index)

        for _ in range(heroes_count):
            hero_turn, hero_card_id = self._read_serialized_card()
            self.heroes.append((hero_card_id, hero_turn))

        self._previous_card_base = 0
        while self.point < card_byte_length:
            card_count, card_id = self._read_serialized_card()
            self.cards.append((card_id, card_count))

        if name_length:
            self.name = self.decoded[-name_length:].decode()

    def _read_var_encoded(self, base_value, base_bits, index):
        value = 0
        delta_shift = 0
        value, has_next = _read_bits_chunk(base_value, base_bits, delta_shift, value)
        if base_bits == 0 or has_next:
            delta_shift += base_bits
            while True:
                next_byte = self.decoded[index]
                index += 1
                value, has_next = _read_bits_chunk(next_byte, 7, delta_shift, value)
                if not has_next:
                    break
                delta_shift += 7
        return value, index

    def _read_serialized_card(self):
        header = self.decoded[self.point]
        self.point += 1

        card_id_delta, self.point = self._read_var_encoded(header, 5, self.point)
        card_id = self._previous_card_base + card_id_delta
        if (header >> 6) == 3:
            count, self.point = self._read_var_encoded(0, 0, self.point)
        else:
            count = (header >> 6) + 1

        self._previous_card_base = card_id
        return count, card_id
