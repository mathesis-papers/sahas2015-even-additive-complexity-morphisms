import heapq
import itertools
import json
from fractions import Fraction
from math import gcd


def factor_sum_sets(codebook, maximum):
    words = tuple(word for word in codebook if word)
    states = tuple((index, offset) for index, word in enumerate(words) for offset in range(len(word)))
    following = {}
    for state in states:
        index, offset = state
        following[state] = ((index, offset + 1),) if offset + 1 < len(words[index]) else tuple((next_index, 0) for next_index in range(len(words)))
    active = {state: {words[state[0]][state[1]]} for state in states}
    result = {}
    for length in range(1, maximum + 1):
        result[length] = set().union(*active.values())
        next_active = {state: set() for state in states}
        for state, sums in active.items():
            for next_state in following[state]:
                value = words[next_state[0]][next_state[1]]
                next_active[next_state].update(total + value for total in sums)
        active = next_active
    return result


def padding_threshold(lengths):
    divisor = gcd(*lengths)
    reduced = tuple(length // divisor for length in lengths)
    modulus = min(reduced)
    distances = [None] * modulus
    distances[0] = 0
    pending = [(0, 0)]
    while pending:
        distance, residue = heapq.heappop(pending)
        if distance != distances[residue]:
            continue
        for length in reduced:
            next_distance = distance + length
            next_residue = next_distance % modulus
            if distances[next_residue] is None or next_distance < distances[next_residue]:
                distances[next_residue] = next_distance
                heapq.heappush(pending, (next_distance, next_residue))
    assert all(distance is not None for distance in distances)
    return divisor, divisor * max(distances)


def brute_factor_sums(codebook, length):
    words = tuple(word for word in codebook if word)
    sums = set()
    for sequence in itertools.product(words, repeat=length + 1):
        image = tuple(itertools.chain.from_iterable(sequence))
        sums.update(sum(image[offset:offset + length]) for offset in range(len(image) - length + 1))
    return sums


def common_slope_checks(codebook, maximum):
    words = tuple(word for word in codebook if word)
    slope = Fraction(sum(words[0]), len(words[0]))
    assert all(Fraction(sum(word), len(word)) == slope for word in words)
    prefix_errors = set()
    for word in words:
        prefix = 0
        for offset, value in enumerate(word):
            prefix_errors.add(prefix - slope * offset)
            prefix += value
    differences = {right - left for left in prefix_errors for right in prefix_errors}
    divisor, threshold = padding_threshold(tuple(map(len, words)))
    radius = max(map(len, words))
    sums_by_length = factor_sum_sets(codebook, maximum)
    parity_cases = 0
    for length, sums in sums_by_length.items():
        assert {Fraction(total) - slope * length for total in sums} <= differences
        assert len(sums) <= len(differences)
        if length % divisor == 0 and length >= threshold + 2 * radius:
            center = slope * length
            assert center.denominator == 1 and center in sums
            assert {2 * center - total for total in sums} == sums
            assert len(sums) % 2 == 1
            parity_cases += 1
    return parity_cases


def run():
    maximum = 16
    alphabet = (-1, 0, 1)
    words = tuple(itertools.chain.from_iterable(itertools.product(alphabet, repeat=length) for length in range(4)))
    common_count = 0
    parity_cases = 0
    growing_count = 0
    cross_checks = 0
    for first, second in itertools.product(words, repeat=2):
        nonempty = tuple(word for word in (first, second) if word)
        if not nonempty:
            continue
        short_sets = factor_sum_sets((first, second), 4)
        for length in range(1, 5):
            assert short_sets[length] == brute_factor_sums((first, second), length)
            cross_checks += 1
        if len(nonempty) == 1 or Fraction(sum(first), len(first)) == Fraction(sum(second), len(second)):
            common_count += 1
            parity_cases += common_slope_checks((first, second), maximum)
        else:
            unit_length = len(first) * len(second)
            first_sum = len(second) * sum(first)
            second_sum = len(first) * sum(second)
            assert first_sum != second_sum
            sums_by_length = factor_sum_sets((first, second), 4 * unit_length)
            for copies in range(1, 5):
                witnessed = {count * first_sum + (copies - count) * second_sum for count in range(copies + 1)}
                assert len(witnessed) == copies + 1
                assert witnessed <= sums_by_length[copies * unit_length]
            growing_count += 1
    erasing_examples = (
        ((), (0,), (-1, 1)),
        ((), (1, -1), (-1, 0, 1)),
        ((), (0, 2), (1, 1)),
        ((), (2,), (1, 3)),
    )
    for codebook in erasing_examples:
        parity_cases += common_slope_checks(codebook, maximum)
    sharpness_cases = 0
    for parameter in range(1, 5):
        codebook = tuple((letter, 2 * parameter - letter) for letter in range(parameter + 1))
        for length, sums in factor_sum_sets(codebook, 20).items():
            assert len(sums) == 2 * parameter + 1
            sharpness_cases += 1
    exceptional = factor_sum_sets(((0, 1),), 4)
    assert len(exceptional[1]) == 2 and len(exceptional[2]) == 1
    report = {
        'status': 'PASS',
        'arithmetic': 'exact integers and rational numbers',
        'method': 'finite-state enumeration of all factors of arbitrary concatenations of the selected codewords',
        'coverage': {
            'ordered_codeword_pairs': len(words) ** 2 - 1,
            'codeword_alphabet': list(alphabet),
            'codeword_lengths': [0, 1, 2, 3],
            'common_slope_pairs': common_count,
            'finite_state_and_direct_enumeration_agreements': cross_checks,
            'common_slope_maximum_factor_length': maximum,
            'additional_erasing_three_letter_codebooks': len(erasing_examples),
            'center_reflection_and_odd_cardinality_cases': parity_cases,
            'unequal_slope_pairs': growing_count,
            'unequal_slope_repetition_counts': [1, 2, 3, 4],
            'banero_parameters': [1, 2, 3, 4],
            'banero_maximum_factor_length': 20,
            'banero_cases': sharpness_cases,
            'divisibility_example': {'codebook': [[0, 1]], 'rho_1': 2, 'rho_2': 1},
        },
        'scope': 'The finite checks illustrate the written proofs; the quantified statements are proved in note.tex.',
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == '__main__':
    run()
