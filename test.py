import ROOT

from TIMBER.Tools.Common import CompileCpp, OpenJSON
CompileCpp("cpp_modules/TaggerDiscretizer.cc")
ROOT.gInterpreter.Declare(f'TaggerDiscretizer AK4_Discretizer = TaggerDiscretizer("Jet",  "2023_Summer23", "UParTAK4_wp_values");')
