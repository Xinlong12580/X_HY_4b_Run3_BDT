void test_mass(){
    ROOT::Math::PtEtaPhiMVector sum;
    sum.SetCoordinates(0,0,0,0);
    ROOT::Math::PtEtaPhiMVector v1(1045.26,-0.356628,1.71411,33.5627);
    ROOT::Math::PtEtaPhiMVector v2(0,-0.380554,1.51709,0);
    std::cout<<sum.Pt()<<" "<<sum.Eta()<<" "<<sum.Phi()<<" "<<sum.M()<<std::endl; 
    sum = sum + v1;
    std::cout<<sum.Pt()<<" "<<sum.Eta()<<" "<<sum.Phi()<<" "<<sum.M()<<std::endl; 
    sum = sum + v2;
    std::cout<<sum.Pt()<<" "<<sum.Eta()<<" "<<sum.Phi()<<" "<<sum.M()<<std::endl; 
    return ;
};

