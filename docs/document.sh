#!/bin/bash
rm -Rf _build/
# Right now this is not picking up all of the code - so leave it undocumented:
# rm -Rf _modules/
# sphinx-apidoc -o ./_modules/ ../jawaf/
sphinx-build -b html ./ ./_build/
