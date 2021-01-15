//This code take histograms from two files and divide them and save them seperatly in a root file

{

TCanvas *c1 = new TCanvas("c1","ratio",10,10,900,500);

TFile *f1 = TFile::Open("LHC_100M_had.root");       // Root file with Hadronization On
TFile *f2 = TFile::Open("LHC_100M_nohad.root");     // Root file with Hadronization On

TFile *NP = new TFile("1_NP_Corr.root","RECREATE");

TH1D *i1, *i2, *i3, *i4, *i5;
TH1D *k1, *k2, *k3, *k4, *k5;


f1->GetObject("CMS_2013_I1208923/d01-x01-y01;1",i1);     
f1->GetObject("CMS_2013_I1208923/d01-x01-y02;1",i2);
f1->GetObject("CMS_2013_I1208923/d01-x01-y03;1",i3);
f1->GetObject("CMS_2013_I1208923/d01-x01-y04;1",i4);
f1->GetObject("CMS_2013_I1208923/d01-x01-y05;1",i5);


f2->GetObject("CMS_2013_I1208923/d01-x01-y01;1", k1);
f2->GetObject("CMS_2013_I1208923/d01-x01-y02;1", k2);
f2->GetObject("CMS_2013_I1208923/d01-x01-y03;1", k3);
f2->GetObject("CMS_2013_I1208923/d01-x01-y04;1", k4);
f2->GetObject("CMS_2013_I1208923/d01-x01-y05;1", k5);


i1->SetTitle("");
i1->Divide(k1);

i2->SetTitle("");
i2->Divide(k2);

i3->SetTitle("");
i3->Divide(k3);

i4->SetTitle("");
i4->Divide(k4);

i5->SetTitle("");
i5->Divide(k5);

i1->Draw();
i2->Draw();
i3->Draw();
i4->Draw();
i5->Draw();


i1->Write();
i2->Write();
i3->Write();
i4->Write();
i5->Write();

NP->Write();
NP->Close();
}
