set term png font arial 40 size 6000,4000
set output "power.png"
set lmargin at screen 0.05
set rmargin at screen 0.90
set bmargin at screen 0.05
set tmargin at screen 0.99
set xlabel "Frequency (MHz)"
set cblabel "Level (dB) at Frequency (MHz)"
set pm3d map
set palette rgbformulae 22,13,-31
set xrange [1415:1425]
set yrange [19:19.97]
set cbrange [-15:15]
splot 'power.bin' binary record=(8193,-1) format='%int32%int32' u ($2/1000):3 with pm3d t ''
