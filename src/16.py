#!/usr/bin/env python3

# pylint: disable=unused-import
import collections
import functools
import io
import itertools
import operator as op
import re
import timeit
from typing import NamedTuple

import numpy as np
import aocd

YEAR = 2021
DAY = 16


LiteralPacket = collections.namedtuple(
    'LiteralPacket', ['version', 'type_id', 'value'])


OpPacket = collections.namedtuple(
    'OpPacket', ['version', 'type_id', 'len_type_id', 'length', 'subpackets'])


def parse_literal(strio, pos):
    nibbles = []
    while True:
        do_continue = int(strio.read(1))
        nibbles.append(strio.read(4))
        pos += 5
        if not do_continue:
            break
    value = int(''.join(nibbles), base=2)
    return value, pos


def parse_operator(strio, pos):
    len_type = int(strio.read(1))
    pos += 1
    version_sum = 0
    if len_type == 0:
        num_bits = int(strio.read(15), base=2)
        pos += 15
        old_pos = pos
        subpackets = []
        while pos - old_pos < num_bits-1:
            packet, pos, add_version = parse_packet(strio, pos)
            version_sum += add_version
            subpackets.append(packet)
        return len_type, num_bits, subpackets, pos, version_sum
    if len_type == 1:
        num_packs = int(strio.read(11), base=2)
        pos += 11
        subpackets = []
        for _ in range(num_packs):
            packet, pos, add_version = parse_packet(strio, pos)
            version_sum += add_version
            subpackets.append(packet)
        return len_type, num_packs, subpackets, pos, version_sum
    raise ValueError('Unknown operator packet length type')


def parse_packet(strio, pos):
    version_str = strio.read(3)
    if len(version_str) == 0:
        return None, pos, 0
    version = int(version_str, base=2)
    pos += 3
    type_id = int(strio.read(3), base=2)
    pos += 3
    match type_id:
        case 4:
            value, pos = parse_literal(strio, pos)
            return LiteralPacket(version=version, type_id=4, value=value), pos, version
        case _:
            len_type, length, subpackets, pos, add_version = parse_operator(strio, pos)
            return OpPacket(
                version=version, type_id=type_id, len_type_id=len_type,
                length=length, subpackets=subpackets), pos, version + add_version


def hex2bin(c):
    return format(int(c, base=16), '04b')


def parse(s):
    bit_str = ''.join(map(hex2bin, s))
    with io.StringIO(bit_str) as strio:
        pos = 0
        return parse_packet(strio, pos)


def calc(packet):
    match packet.type_id:
        case 4:
            return packet.value
        case 0:
            return sum(map(calc, packet.subpackets))
        case 1:
            return functools.reduce(op.mul, map(calc, packet.subpackets), 1)
        case 2:
            return min(map(calc, packet.subpackets))
        case 3:
            return max(map(calc, packet.subpackets))
        case 5:
            return calc(packet.subpackets[0]) > calc(packet.subpackets[1])
        case 6:
            return calc(packet.subpackets[0]) < calc(packet.subpackets[1])
        case 7:
            return calc(packet.subpackets[0]) == calc(packet.subpackets[1])
        case _:
            raise ValueError('Unknown packet type_id')


def main():
    test_packets = [
        'D2FE28',
        '38006F45291200',
        'EE00D40C823060',
        '8A004A801A8002F478',
        '620080001611562C8802118E34',
        'C0015000016115A2E0802F182340',
        'A0016C880162017C3686B18A3D4780',
    ]
    for p in test_packets:
        print(p)
        print(parse(p), '\n')

    test_packets_2 = [
        'C200B40A82',
        '04005AC33890',
        '880086C3E88112',
        'CE00C43D881120',
        'D8005AC2A8F0',
        'F600BC2D8F',
        '9C005AC2F8F0',
        '9C0141080250320F1802104A08',
    ]
    for p in test_packets_2:
        print(p)
        pp, _, _ = parse(p)
        print(pp)
        print(calc(pp))
        print()

    data = aocd.get_data(day=DAY, year=YEAR)

    parsed_packet, _, version_sum = parse(data)
    print(parsed_packet)
    answer = version_sum
    print(answer)
    aocd.submit(answer, part='a', day=DAY, year=YEAR)

    answer = calc(parsed_packet)
    print(answer)
    aocd.submit(answer, part='b', day=DAY, year=YEAR)


if __name__ == '__main__':
    main()
