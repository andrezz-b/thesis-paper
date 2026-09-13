# latexmk configuration for the DTU thesis template.
#
# The template relies on `fontspec` (\setmainfont{Arial}) and `biblatex`
# with `backend=biber`, so we compile with XeLaTeX and drive biber
# automatically instead of bibtex.

$pdf_mode = 5;          # 5 = xelatex -> pdf
$postscript_mode = 0;
$dvi_mode = 0;

$biber = 'biber %O %S';
$bibtex_use = 2;        # only run biber/bibtex when needed

$out_dir = 'build';
$aux_dir = 'build';

# Keep going on nonfatal errors so a single missing reference etc. doesn't
# stop the whole pipeline; combined with -halt-on-error at the CLI level
# for tasks that should fail fast (e.g. CI / agent runs).
$max_repeat = 5;

# Clean up extra byproducts on `latexmk -c` / `-C` in addition to defaults.
$clean_ext = 'bbl bcf run.xml synctex.gz';
