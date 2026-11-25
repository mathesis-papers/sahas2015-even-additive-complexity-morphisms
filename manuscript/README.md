# Sahasrabudhe's even additive-complexity construction question

The note proves that a finite morphism of a universal source word cannot have a positive even additive complexity constant at every positive length. Erasing codewords are allowed when their concatenation is infinite. More generally, bounded additive complexity implies odd cardinality of the factor-sum set at every sufficiently large length divisible by the gcd of the codeword lengths. A uniformly recurrent output of a universal-input finite morphism is periodic.

## Scope

The complementary-window argument also applies to vector sums in an integer
lattice, including Parikh vectors and hence abelian complexity (Corollary 5).
Corollary 4 gives the common-slope criterion, credits Banero's earlier
non-erasing anchor theorem, and proves the universal-input special case of
his splicing Problem 32. The general splicing conjecture and Sahasrabudhe's
second question on other uniformly recurrent fixed-complexity words are not
answered in general.

## Files

- `note.tex`: self-contained proofs and bibliography.
- `note.pdf`: readable typeset note, supplied separately from the source archive.
- `metadata.json`: title, creators, license, problem coverage and mathematical evidence links.
- `verify.py`: Python 3 exact-arithmetic finite checks, using the standard library.
- `checks.json`: expected checker output.

## Build

Use Tectonic 0.17.0:

```sh
tectonic --untrusted note.tex
```

Alternatively, use a standard LaTeX installation with `amsmath`, `amssymb`, `amsthm`, `geometry`, `booktabs`, `array`, `fontenc`, `lmodern`, `microtype` and `hyperref`:

```sh
pdflatex -halt-on-error -no-shell-escape note.tex
pdflatex -halt-on-error -no-shell-escape note.tex
```

The bibliography is included in `note.tex`; BibTeX and network access are unnecessary once the LaTeX packages are installed.

## Exact finite checks

```sh
python3 verify.py > checks-new.json
python3 -c 'import json; assert json.load(open("checks-new.json")) == json.load(open("checks.json")); print("PASS")'
```

The checker represents a factor by a path through states `(codeword, offset)`. The next state advances inside a codeword, or selects any nonempty codeword at its end. Universality makes precisely these finite paths available in the output language; deleting empty codewords leaves that language unchanged. Dynamic programming records every attainable integer sum. Direct enumeration of finite concatenations independently checks the shorter paths. These are complete factor-sum computations for the specified finite codebooks and lengths, rather than samples of starting positions in an infinite word.

The quantified proofs are in the note. The pinned Lean declaration `D5.S1.Words.Complexity.SahasrabudheEvenAdditiveComplexityMorphism.result` covers the constant positive even obstruction, including erasing codewords with unbounded cumulative boundaries. The bounded-complexity parity extension, eventual-constant consequence, common-slope and anchored-word consequences, lattice-valued extension and uniform-recurrence result have written proofs. The finite checks illustrate the scalar statements and Banero's odd construction; their exact ranges appear in `checks.json`.

Lean source: https://github.com/the-omega-institute/trureturing/blob/ea30c256f9857dcf2582db122a9570836d8a5f18/D5/S1/Words/Complexity/SahasrabudheEvenAdditiveComplexityMorphism.lean

Primary posing source: Julian Sahasrabudhe, *Sturmian Words and Constant Additive Complexity*, Integers 15 (2015), A30, Section 5, p. 7: https://math.colgate.edu/~integers/p30/p30.pdf

## Authors and license

Haobo Ma — ChronoAI Pte Ltd, Singapore.

Wenlin Zhang — National University of Singapore; ChronoAI Pte Ltd, Singapore.

Copyright 2026 Haobo Ma and Wenlin Zhang. Licensed under Creative Commons Attribution 4.0 International, https://creativecommons.org/licenses/by/4.0/ (`cc-by-4.0`).
