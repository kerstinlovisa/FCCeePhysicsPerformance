#!/bin/bash



########################################################### backgrounds ######################################################################
# spring2021 samples
python3 analysis_general.py -i /eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA/p8_ee_Zee_ecm91/events_199283914.root -o ./read_EDM4HEP/Zee/
python3 analysis_general.py -i /eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA/p8_ee_Zbb_ecm91/events_199984817.root -o ./read_EDM4HEP/Zbb/
python3 analysis_general.py -i /eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA/p8_ee_Ztautau_ecm91/events_198604879.root -o ./read_EDM4HEP/Ztautau/
python3 analysis_general.py -i /eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA/p8_ee_Zuds_ecm91/events_199878624.root -o ./read_EDM4HEP/Zuds/
python3 analysis_general.py -i /eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA/p8_ee_Zcc_ecm91/events_199973752.root -o ./read_EDM4HEP/Zcc/

# dev samples
#python3 analysis_general.py -i /eos/experiment/fcc/ee/generation/DelphesEvents/dev/IDEA/p8_ee_Zee_ecm91/events_195988098.root -o ./read_EDM4HEP/Zee/

# private sample made by Emmanuel:
#python3 analysis_general.py -i /eos/experiment/fcc/users/e/eperez/test_Zee_for_Juliette.root #where electrons are stored before the overlap removal
#python3 analysis_general.py -i /eos/experiment/fcc/users/e/eperez/test_Zee_for_Juliette_v2.root #AllElectron collection contains all electrons before the isolation requirement



########################################################### signals ######################################################################
# private signal samples
# python3 analysis_general.py -i /afs/cern.ch/user/l/lrygaard/public/HNL_root_files/HNL_eenu_90GeV_1p41e-6Ve.root
#python3 analysis_general.py -i /afs/cern.ch/user/l/lrygaard/public/HNL_root_files/HNL_eenu_70GeV_1p41e-6Ve.root
#python3 analysis_general.py -i /afs/cern.ch/user/l/lrygaard/public/HNL_root_files/HNL_eenu_50GeV_1p41e-6Ve.root
# python3 analysis_general.py -i /afs/cern.ch/user/l/lrygaard/public/HNL_root_files/HNL_eenu_30GeV_1p41e-6Ve.root
python3 analysis_general.py -i /afs/cern.ch/user/l/lrygaard/public/HNL_root_files/HNL_eenu_30GeV_1e-5Ve.root
python3 analysis_general.py -i /afs/cern.ch/user/l/lrygaard/public/HNL_root_files/HNL_eenu_40GeV_1e-5Ve.root
