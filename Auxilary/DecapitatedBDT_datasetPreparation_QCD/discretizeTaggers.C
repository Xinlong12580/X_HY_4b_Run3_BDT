float discretizeTaggers(float score, std::string jetType, std::string year){
    std::vector<float> WPs;
    //particleNet Tagger
    if (jetType == "AK4"){
        if (year == "2022")
            WPs = {0, 0.047, 0.245, 0.6734, 0.7862, 0.961, 1};
        if (year == "2022EE")
            WPs = {0, 0.0499, 0.2605, 0.6915, 0.8033, 0.9664, 1};
        if (year == "2023")
            WPs = {0, 0.0358, 0.1917, 0.6172, 0.7515, 0.9659, 1};
        if (year == "2023BPix")
            WPs = {0, 0.0359, 0.1919, 0.6133, 0.7544, 0.9688, 1};
        if (year == "2024")//No WP, using 2023BPix for the moment
            WPs = {0, 0.0359, 0.1919, 0.6133, 0.7544, 0.9688, 1};
    }
    else if (jetType == "AK8"){
        WPs = {0, 0.9172, 0.9734, 0.9880, 1};
        //WPs = {0, 0.2, 0.4, 0.6, 0.8, 0.9172, 0.9734, 0.9880, 1};
    }
    float score_discrete = -1.; //Defined as float to avoid data type mismatch later
    for (int i = 0; i < WPs.size() - 1; i ++)
        if (score >= WPs.at(i) && score < WPs.at(i+1)){
            score_discrete = i;
            break;
        }
    return score_discrete; 
};
