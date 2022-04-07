#run this with:
#python runAnalysis_general_batch.py

from config.common_defaults import deffccdicts
import config.runDataFrameBatch as rdf
import os

basedir=os.path.join(os.getenv('FCCDICTSDIR', deffccdicts), '') + "yaml/FCCee/spring2021/IDEA/"
outdir="/afs/cern.ch/work/j/jalimena/FCCeeLLP/FCCeePhysicsPerformance/case-studies/BSM/LLP/DisplacedHNL/Batch_Analysis_general/"

NUM_CPUS=8
output_list=[]
fraction=1.

inputana="/afs/cern.ch/work/j/jalimena/FCCeeLLP/FCCeePhysicsPerformance/case-studies/BSM/LLP/DisplacedHNL/analysis_general.py"

process_list=['p8_ee_Zee_ecm91',
              #'p8_ee_Zbb_ecm91',
              #'p8_ee_Ztautau_ecm91',
              #'p8_ee_Zuds_ecm91',
              #'p8_ee_Zcc_ecm91',
              ]

myana=rdf.runDataFrameBatch(basedir,process_list, outlist=output_list)
myana.run(ncpu=NUM_CPUS,fraction=fraction, chunks=50 ,outDir=outdir, inputana=inputana, comp="group_u_ATLAST3.all")
#myana.run(ncpu=NUM_CPUS,fraction=fraction, chunks=50 ,outDir=outdir, inputana=inputana, comp="group_u_DEFAULT.all")
