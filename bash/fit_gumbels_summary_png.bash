
mkdir -p ../summary_pngs

cd ../fit_gumbel
montage -geometry 1000x1000 *.png \
	../summary_pngs/fit_gumbels.png
