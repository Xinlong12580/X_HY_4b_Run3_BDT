class DDT_map{
public:
    TF2 f;
    DDT_map(std::string para_file, std::string func);
    ~DDT_map(){};
    bool eval(float MVA, float MX, float MY);
    
};
DDT_map::DDT_map(std::string para_file, std::string func = "1.99/(1+exp(- [5] /x * ( [0] + [1]*x+[2]*y + [3]*x*x + [4]*y*y ))) - 1"){
    f = TF2("DDT_f", func.c_str(), 0, 4000, 0, 3500);
    std::ifstream infile(para_file);
    std::string line;
    std::vector<float> paras = {};
    while (std::getline(infile, line)) {
        float value = std::stof(line);
        paras.push_back(value);
    }
    std::cout<<"DDT map funcion: "<<func<<std::endl;
    std::cout<<"DDT map parameters: "<<std::endl;
    for(int i = 0; i < paras.size(); i++){
        std::cout<<i<<" "<<paras.at(i)<<std::endl;
        f.SetParameter(i, paras.at(i));
    }
     
};


bool DDT_map::eval(float MVA, float MX, float MY){
    float wp = f.Eval(MX, MY);
    //std::cout<<MVA<<" "<<wp<<" "<<MX<<" "<<MY<<std::endl;
    return (MVA > wp);
}
