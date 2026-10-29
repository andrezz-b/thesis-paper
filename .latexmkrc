# Shared latexmk configuration for all documents in this repository
# (thesis/ and plan/). Documents are built with `latexmk -cd <doc>/main.tex`,
# so output lands in <doc>/build/.
#
# Both documents use `fontspec` and the thesis uses `biblatex` with
# `backend=biber`, so we compile with XeLaTeX and drive biber automatically.

$pdf_mode = 5;          # 5 = xelatex -> pdf
$postscript_mode = 0;
$dvi_mode = 0;

$biber = 'biber %O %S';
$bibtex_use = 2;        # only run biber/bibtex when needed

$out_dir = 'build';
$aux_dir = 'build';

$max_repeat = 5;

# Clean up extra byproducts on `latexmk -c` / `-C` in addition to defaults.
$clean_ext = 'bbl bcf run.xml synctex.gz';
