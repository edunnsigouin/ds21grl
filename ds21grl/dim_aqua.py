# list of useful hardcoded constants and coordinate grids for aqua planet model simulations

import numpy as np


years      = np.arange(11,51,1)
months     = np.arange(1,13,1)
wavenumber = np.arange(0,41,1)
chunk      = 73
nday       = 365

timestamp  = str(years[0]) + '-' + str(years[-1])


lat = np.array([
    -90, -89.0575916230366, -88.1151832460733, -87.1727748691099, 
    -86.2303664921466, -85.2879581151832, -84.3455497382199, 
    -83.4031413612565, -82.4607329842932, -81.5183246073298, 
    -80.5759162303665, -79.6335078534031, -78.6910994764398, 
    -77.7486910994764, -76.8062827225131, -75.8638743455497, 
    -74.9214659685864, -73.979057591623, -73.0366492146597, 
    -72.0942408376963, -71.151832460733, -70.2094240837696, 
    -69.2670157068063, -68.3246073298429, -67.3821989528796, 
    -66.4397905759162, -65.4973821989529, -64.5549738219895, 
    -63.6125654450262, -62.6701570680628, -61.7277486910995, 
    -60.7853403141361, -59.8429319371728, -58.9005235602094, 
    -57.9581151832461, -57.0157068062827, -56.0732984293194, 
    -55.130890052356, -54.1884816753927, -53.2460732984293, -52.303664921466, 
    -51.3612565445026, -50.4188481675393, -49.4764397905759, 
    -48.5340314136126, -47.5916230366492, -46.6492146596859, 
    -45.7068062827225, -44.7643979057592, -43.8219895287958, 
    -42.8795811518325, -41.9371727748691, -40.9947643979058, 
    -40.0523560209424, -39.1099476439791, -38.1675392670157, 
    -37.2251308900524, -36.282722513089, -35.3403141361257, 
    -34.3979057591623, -33.455497382199, -32.5130890052356, 
    -31.5706806282723, -30.6282722513089, -29.6858638743456, 
    -28.7434554973822, -27.8010471204188, -26.8586387434555, 
    -25.9162303664921, -24.9738219895288, -24.0314136125654, 
    -23.0890052356021, -22.1465968586387, -21.2041884816754, 
    -20.261780104712, -19.3193717277487, -18.3769633507853, -17.434554973822, 
    -16.4921465968586, -15.5497382198953, -14.6073298429319, 
    -13.6649214659686, -12.7225130890052, -11.7801047120419, 
    -10.8376963350785, -9.89528795811518, -8.95287958115183, 
    -8.01047120418848, -7.06806282722513, -6.12565445026178, 
    -5.18324607329843, -4.24083769633508, -3.29842931937173, 
    -2.35602094240838, -1.41361256544503, -0.471204188481676, 
    0.471204188481675, 1.41361256544503, 2.35602094240838, 3.29842931937173, 
    4.24083769633508, 5.18324607329843, 6.12565445026178, 7.06806282722513, 
    8.01047120418848, 8.95287958115183, 9.89528795811518, 10.8376963350785, 
    11.7801047120419, 12.7225130890052, 13.6649214659686, 14.6073298429319, 
    15.5497382198953, 16.4921465968586, 17.434554973822, 18.3769633507853, 
    19.3193717277487, 20.261780104712, 21.2041884816754, 22.1465968586387, 
    23.0890052356021, 24.0314136125654, 24.9738219895288, 25.9162303664921, 
    26.8586387434555, 27.8010471204188, 28.7434554973822, 29.6858638743456, 
    30.6282722513089, 31.5706806282722, 32.5130890052356, 33.4554973821989, 
    34.3979057591623, 35.3403141361257, 36.282722513089, 37.2251308900524, 
    38.1675392670157, 39.1099476439791, 40.0523560209424, 40.9947643979058, 
    41.9371727748691, 42.8795811518325, 43.8219895287958, 44.7643979057592, 
    45.7068062827225, 46.6492146596859, 47.5916230366492, 48.5340314136126, 
    49.4764397905759, 50.4188481675393, 51.3612565445026, 52.303664921466, 
    53.2460732984293, 54.1884816753927, 55.130890052356, 56.0732984293194, 
    57.0157068062827, 57.9581151832461, 58.9005235602094, 59.8429319371728, 
    60.7853403141361, 61.7277486910995, 62.6701570680628, 63.6125654450262, 
    64.5549738219895, 65.4973821989529, 66.4397905759162, 67.3821989528796, 
    68.3246073298429, 69.2670157068063, 70.2094240837696, 71.151832460733, 
    72.0942408376963, 73.0366492146597, 73.979057591623, 74.9214659685864, 
    75.8638743455497, 76.8062827225131, 77.7486910994764, 78.6910994764398, 
    79.6335078534031, 80.5759162303665, 81.5183246073298, 82.4607329842932, 
    83.4031413612565, 84.3455497382199, 85.2879581151832, 86.2303664921466, 
    87.1727748691099, 88.1151832460733, 89.0575916230366, 90 ])

lon = np.array([
    0, 1.25, 2.5, 3.75, 5, 6.25, 7.5, 8.75, 10, 11.25, 12.5, 13.75, 15, 
    16.25, 17.5, 18.75, 20, 21.25, 22.5, 23.75, 25, 26.25, 27.5, 28.75, 30, 
    31.25, 32.5, 33.75, 35, 36.25, 37.5, 38.75, 40, 41.25, 42.5, 43.75, 45, 
    46.25, 47.5, 48.75, 50, 51.25, 52.5, 53.75, 55, 56.25, 57.5, 58.75, 60, 
    61.25, 62.5, 63.75, 65, 66.25, 67.5, 68.75, 70, 71.25, 72.5, 73.75, 75, 
    76.25, 77.5, 78.75, 80, 81.25, 82.5, 83.75, 85, 86.25, 87.5, 88.75, 90, 
    91.25, 92.5, 93.75, 95, 96.25, 97.5, 98.75, 100, 101.25, 102.5, 103.75, 
    105, 106.25, 107.5, 108.75, 110, 111.25, 112.5, 113.75, 115, 116.25, 
    117.5, 118.75, 120, 121.25, 122.5, 123.75, 125, 126.25, 127.5, 128.75, 
    130, 131.25, 132.5, 133.75, 135, 136.25, 137.5, 138.75, 140, 141.25, 
    142.5, 143.75, 145, 146.25, 147.5, 148.75, 150, 151.25, 152.5, 153.75, 
    155, 156.25, 157.5, 158.75, 160, 161.25, 162.5, 163.75, 165, 166.25, 
    167.5, 168.75, 170, 171.25, 172.5, 173.75, 175, 176.25, 177.5, 178.75, 
    180, 181.25, 182.5, 183.75, 185, 186.25, 187.5, 188.75, 190, 191.25, 
    192.5, 193.75, 195, 196.25, 197.5, 198.75, 200, 201.25, 202.5, 203.75, 
    205, 206.25, 207.5, 208.75, 210, 211.25, 212.5, 213.75, 215, 216.25, 
    217.5, 218.75, 220, 221.25, 222.5, 223.75, 225, 226.25, 227.5, 228.75, 
    230, 231.25, 232.5, 233.75, 235, 236.25, 237.5, 238.75, 240, 241.25, 
    242.5, 243.75, 245, 246.25, 247.5, 248.75, 250, 251.25, 252.5, 253.75, 
    255, 256.25, 257.5, 258.75, 260, 261.25, 262.5, 263.75, 265, 266.25, 
    267.5, 268.75, 270, 271.25, 272.5, 273.75, 275, 276.25, 277.5, 278.75, 
    280, 281.25, 282.5, 283.75, 285, 286.25, 287.5, 288.75, 290, 291.25, 
    292.5, 293.75, 295, 296.25, 297.5, 298.75, 300, 301.25, 302.5, 303.75, 
    305, 306.25, 307.5, 308.75, 310, 311.25, 312.5, 313.75, 315, 316.25, 
    317.5, 318.75, 320, 321.25, 322.5, 323.75, 325, 326.25, 327.5, 328.75, 
    330, 331.25, 332.5, 333.75, 335, 336.25, 337.5, 338.75, 340, 341.25, 
    342.5, 343.75, 345, 346.25, 347.5, 348.75, 350, 351.25, 352.5, 353.75, 
    355, 356.25, 357.5, 358.75 ])

lev = np.array([
    3.64346569404006, 7.59481964632869, 14.3566322512925, 
    24.6122200042009, 38.2682997733355, 54.5954797416925, 72.0124505460262, 
    87.8212302923203, 103.317126631737, 121.547240763903, 142.994038760662, 
    168.225079774857, 197.908086702228, 232.828618958592, 273.910816758871, 
    322.241902351379, 379.100903868675, 445.992574095726, 524.687174707651, 
    609.778694808483, 691.389430314302, 763.404481112957, 820.858368650079, 
    859.53476652503, 887.020248919725, 912.644546944648, 936.198398470879, 
    957.485479535535, 976.325407391414, 992.556095123291 ])

P0 = 100000.0

hyai = np.array([0.00225523952394724, 0.00503169186413288, 0.0101579474285245, 
    0.0185553170740604, 0.0306691229343414, 0.0458674766123295, 
    0.0633234828710556, 0.0807014182209969, 0.0949410423636436, 
    0.11169321089983, 0.131401270627975, 0.154586806893349, 
    0.181863352656364, 0.17459799349308, 0.166050657629967, 
    0.155995160341263, 0.14416541159153, 0.130248308181763, 
    0.113875567913055, 0.0946138575673103, 0.0753444507718086, 
    0.0576589405536652, 0.0427346378564835, 0.0316426791250706, 
    0.0252212174236774, 0.0191967375576496, 0.0136180268600583, 
    0.00853108894079924, 0.00397881818935275, 0, 0 ])

hybi = np.array([ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.0393548272550106, 
    0.0856537595391273, 0.140122056007385, 0.204201176762581, 
    0.279586911201477, 0.368274360895157, 0.47261056303978, 
    0.576988518238068, 0.672786951065063, 0.753628432750702, 
    0.813710987567902, 0.848494648933411, 0.881127893924713, 
    0.911346435546875, 0.938901245594025, 0.963559806346893, 
    0.985112190246582, 1])

ilev = np.array([ 2.25523952394724, 5.03169186413288, 10.1579474285245, 
    18.5553170740604, 30.6691229343414, 45.8674766123295, 63.3234828710556, 
    80.7014182209969, 94.9410423636436, 111.69321089983, 131.401270627975, 
    154.586806893349, 181.863352656364, 213.952820748091, 251.704417169094, 
    296.117216348648, 348.366588354111, 409.83521938324, 482.149928808212, 
    567.22442060709, 652.332969009876, 730.445891618729, 796.363070607185, 
    845.353666692972, 873.715866357088, 900.324631482363, 924.964462406933, 
    947.432334534824, 967.538624536246, 985.112190246582, 1000 ])
