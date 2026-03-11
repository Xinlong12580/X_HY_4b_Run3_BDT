#include <correction.h>
#include <ROOT/RVec.hxx>

using ROOT::VecOps::RVec;
void test(){
    std::string f_name = "/cvmfs/cms.cern.ch/rsync/cms-nanoAOD/jsonpog-integration/POG/BTV/2023_Summer23/btagging.json.gz"; 
    std::unique_ptr<correction::CorrectionSet> _cset = correction::CorrectionSet::from_file(f_name.c_str());
    //correction::Correction::Ref         ref = _cset->at(taggerType.c_str());
    correction::Correction::Ref         ref = _cset->at("robustParticleTransformer_wp_values");
    std::vector<float> WPs = {0.};
    std::vector<std::string> s_wps = {"L", "M", "T", "XT", "XXT"};
        
    for (auto s_wp : s_wps){
        std::map<std::string, correction::Variable::Type> map {{ "working_point" , s_wp.c_str()}};
        std::vector<correction::Variable::Type> inputs;
        for (const correction::Variable& input: ref->inputs()) {
            std::cout<<input.name()<<std::endl;
            inputs.push_back(map.at(input.name()));
        }
        int wp = ref->evaluate(inputs);
        std::cout<<s_wp<<": "<<wp<<std::endl;
        WPs.push_back(wp);
    }
    WPs.push_back(1.);
    } 
}    
