#!/bin/bash -e

./download_dali_and_tm_hits.bash

./setup_cath40.bash
./setup_scop40.bash
./setup_scop95.bash
./setup_scop40x8.bash

./reseek_search.bash cath40
./reseek_search.bash scop40
./reseek_search.bash scop95
./reseek_search_x8.bash

./foldseek_search.bash cath40
./foldseek_search.bash scop40
./foldseek_search.bash scop95
./foldseek_search_scop40x8.bash

./edfs.bash

./c_false_plots.bash
