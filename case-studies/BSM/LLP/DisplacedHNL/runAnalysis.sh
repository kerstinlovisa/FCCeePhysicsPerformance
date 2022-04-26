#!/bin/bash

#for i in 5 10 12 15 20 30 40 50 70 90
for i in 30
do
    python3 analysis_HNL_read.py -i HNL_sample_creation/HNL_eenu_"$i"GeV_1p41e-6Ve.root
done

#python3 analysis_HNL_read.py -i HNL_sample_creation/HNL_eenu_20GeV_0p1Ve_withBothAntiNu.root 
#python3 analysis_HNL_read.py -i HNL_sample_creation/HNL_eenu_20GeV_0p1Ve_withBothAntiNu_localDelphes_v2.root 
#python3 analysis_HNL_read.py -i HNL_sample_creation/HNL_eenu_50GeV_1p41e-6Ve_withBothAntiNu.root
#python3 analysis_HNL_read.py -i HNL_sample_creation/HNL_eenu_50GeV_1p41e-6Ve_withBothAntiNu_localDelphes_v2.root
