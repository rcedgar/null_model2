#!/bin/bash -e

xr=0.05:0.3
yr=1e-3:1
#                          ref                 	target					xrange	yrange		prior
./predict_P_F_score.bash   reseek.scop40       	reseek.scop40x8		 	$xr		$yr			0.5
./predict_P_F_score.bash   reseek.scop40x8        reseek.scop40			 	$xr		$yr		0.5
./predict_P_F_score.bash   reseek.scop40       reseek.scop40.sf4 	$xr		$yr				0.5
./predict_P_F_score.bash   reseek.scop40.sf4  	reseek.scop40 			$xr		$yr				0.5
./predict_P_F_score.bash   reseek.scop40          reseek.scop40.n4 	$xr		$yr				0.5
./predict_P_F_score.bash   reseek.scop40.n4  reseek.scop40 			$xr		$yr				0.5

xr=_0:12
yr=1e-3:1
#                          ref                    target					xrange	yrange
./predict_P_F_score.bash   foldseek.scop40          foldseek.scop40x8		 	$xr		$yr	0.9
./predict_P_F_score.bash   foldseek.scop40x8        foldseek.scop40			 	$xr		$yr	0.9
./predict_P_F_score.bash   foldseek.scop40          foldseek.scop40.sf4	$xr		$yr	0.9
./predict_P_F_score.bash   foldseek.scop40.sf4  foldseek.scop40			$xr		$yr	0.9
./predict_P_F_score.bash   foldseek.scop40          foldseek.scop40.n4 	$xr		$yr	0.9
./predict_P_F_score.bash   foldseek.scop40.n4  foldseek.scop40 			$xr		$yr	0.9

xr=0.2:0.8
yr=1e-2:1
#                          ref                    target					xrange	yrange
./predict_P_F_score.bash   tm.scop40          tm.scop40.sf4	$xr		$yr	0.99
./predict_P_F_score.bash   tm.scop40.sf4  tm.scop40			$xr		$yr	0.99
./predict_P_F_score.bash   tm.scop40          tm.scop40.n4 	$xr		$yr	0.99
./predict_P_F_score.bash   tm.scop40.n4  tm.scop40 			$xr		$yr	0.99
