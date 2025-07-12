#!/bin/bash -e

xr=0.05:0.3
yr=1e-3:1
#                          ref                    target					xrange	yrange
./predict_P_F_score.bash   reseekts.scop40          reseekts.scop40x8		 	$xr		$yr
./predict_P_F_score.bash   reseekts.scop40x8        reseekts.scop40			 	$xr		$yr
./predict_P_F_score.bash   reseekts.scop40          reseekts.scop40.sf8.seed1 	$xr		$yr
./predict_P_F_score.bash   reseekts.scop40          reseekts.scop40.sf4.seed1 	$xr		$yr
./predict_P_F_score.bash   reseekts.scop40.sf8.seed1  reseekts.scop40 			$xr		$yr
./predict_P_F_score.bash   reseekts.scop40.sf4.seed1  reseekts.scop40 			$xr		$yr
./predict_P_F_score.bash   reseekts.scop40          reseekts.scop40.n8.seed1 	$xr		$yr
./predict_P_F_score.bash   reseekts.scop40          reseekts.scop40.n4.seed1 	$xr		$yr
./predict_P_F_score.bash   reseekts.scop40.n8.seed1  reseekts.scop40 			$xr		$yr
./predict_P_F_score.bash   reseekts.scop40.n4.seed1  reseekts.scop40 			$xr		$yr
