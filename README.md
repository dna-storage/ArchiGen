[![DOI](https://zenodo.org/badge/721365800.svg)](https://zenodo.org/doi/10.5281/zenodo.10162601)

Repository with simulator code used in paper "Reducing Read Amplification and Re-synthesis in DNA-based Archival Storage".

# Reproducing results from the paper

Simulator is written in Python and has minimal dependencies on plotting modules.

1. Install requirements by running `pip3 install -r requirements.txt`
2. Generate trace by running `python3 gen.py 1_80_hint.txt 1/80` which will produce file named `1_80_hint.txt`
3. Reproduce Figure 3a-b by running and checking PDFs afterward
```
python3 sim.py 1_80_hint.txt fig3 1_80_hint.txt fig3
python3 plot3.py
```
4. Reproduce Figure 4a-b by running and checking PDFs afterward
```
python3 sim.py 1_80_hint.txt fig4 1_80_hint.txt fig4
python3 plot4.py
```
6. Reproduce Figure 6 by running and checking PDF afterward
```
python3 sim.py 1_80_hint.txt fig6 1_80_hint.txt fig6
python3 plot6.py
```

Each simulation runs 100 times and completes in around 10 minutes.
