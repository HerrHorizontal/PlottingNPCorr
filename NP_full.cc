//this program plots all NP Correction factors on single canvas
#include <iostream>
#include "cmath"

using namespace std;
void NP_full()

{

  
  TCanvas *c = new TCanvas("c", "NP Correction Factor",500,400);
  c->Range(2.106318,-8.082687,3.353915,7.77261);
  c->SetBorderSize(2);
  c->SetLeftMargin(0.1560694);
  c->SetRightMargin(0.04238921);
  c->SetTopMargin(0.04872881);
  c->SetBottomMargin(0.1313559);
  c->SetTicky(1);
  c->SetLogx();
  c->SetGrid();

TFile *f1 = TFile::Open("LHC_100M_had.root");      // Root file with Hadronization On
TFile *f2 = TFile::Open("LHC_100M_nohad.root");    // Root file with Hadronization Off

TH1D *h1, *h2, *h3, *h4, *h5;
TH1D *k1, *k2, *k3, *k4, *k5;


f1->GetObject("CMS_2013_I1208923/d01-x01-y01;1",h1);
f1->GetObject("CMS_2013_I1208923/d01-x01-y02;1",h2);
f1->GetObject("CMS_2013_I1208923/d01-x01-y03;1",h3);
f1->GetObject("CMS_2013_I1208923/d01-x01-y04;1",h4);
f1->GetObject("CMS_2013_I1208923/d01-x01-y05;1",h5);


f2->GetObject("CMS_2013_I1208923/d01-x01-y01;1", k1);
f2->GetObject("CMS_2013_I1208923/d01-x01-y02;1", k2);
f2->GetObject("CMS_2013_I1208923/d01-x01-y03;1", k3);
f2->GetObject("CMS_2013_I1208923/d01-x01-y04;1", k4);
f2->GetObject("CMS_2013_I1208923/d01-x01-y05;1", k5);


h1->SetTitle("");
h1->Divide(k1);

h2->SetTitle("");
h2->Divide(k2);

h3->SetTitle("");
h3->Divide(k3);

h4->SetTitle("");
h4->Divide(k4);

h5->SetTitle("");
h5->Divide(k5);

h1->SetLineColor(6);
h2->SetLineColor(4);
h3->SetLineColor(3);
h4->SetLineColor(2);
h5->SetLineColor(1);

h1->SetTitle("NP correction factors");
h1->GetYaxis()->SetRangeUser(0.98,1.1);        
h1->GetXaxis()->SetTitle("jet pT");
h1->GetYaxis()->SetTitle("NP Correction Factor");
h1->Draw();
h2->Draw("same");
h3->Draw("same");
h4->Draw("same");
h5->Draw("same");

gStyle->SetOptStat(0);

TLegend *legend1=new TLegend(0.6313993,0.6485261,0.9300341,0.9183673);
  legend1->SetTextFont(42);
  legend1->SetTextSize(0.03);
  legend1->SetLineStyle(1);
  legend1->SetLineWidth(1);
  legend1->SetFillColor(0);
  legend1->SetBorderSize(0);
  legend1->SetLineColor(1);
  legend1->AddEntry(h1,"|y|< 0.5" );
  legend1->AddEntry(h2,"0.5 #leq |y|< 1.0" );
  legend1->AddEntry(h3,"1.0 #leq |y|< 1.5 ");
  legend1->AddEntry(h4,"1.5 #leq |y|< 2.0 ");
  legend1->AddEntry(h5,"2.0 #leq |y|< 2.5 ");
  legend1->Draw();  
  c->Update();
  c->Draw();

  c->SaveAs("NP_full.pdf");
  c->SaveAs("NP_full.png");


}



