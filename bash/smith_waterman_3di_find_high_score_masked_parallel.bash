#!/bin/bash -e

seq 101 120 | parallel -j20 ./smith_waterman_3di_find_high_score_masked.bash
