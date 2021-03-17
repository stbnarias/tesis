DETAIL_NONE = 'none'
DETAIL_LOW = 'low'
DETAIL_FULL = 'full'

import os
from biocyc import biocyc

biocyc.set_organism('BSUB')
biocyc.set_detail(DETAIL_LOW)
o = biocyc.get_from_api("compounds-of-pathway","GLYCOLYSIS")
print o