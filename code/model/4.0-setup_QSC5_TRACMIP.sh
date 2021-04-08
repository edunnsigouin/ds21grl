#!/bin/bash

# Script that sets up and submits a CAM5 slab ocean aquaplanet control
# run following the TRACMIP protocol (Voigt et al. 2016 JAMES) on the FRAM cluster. 
# The model version is CESM 2.1.0. 


# define inputs 
expname="QSC5.TRACMIP"
docn_som_filepath="/cluster/home/edu061/SETUP_RUN/SOM_FORCING"
docn_som_filename="som.QSC5.TRACMIP.nc"
resubmit=49
stop_n=1
stop_option="nyears"
wallclock="03:30:00"

# create case 
cd $HOME/cesm2.1.0/cime/scripts/
./create_newcase --case $HOME/cesm2.1.0/cases/$expname --compset QSC5 --res f09_f09_mg17 --machine fram --pecount L --project nn9039k --run-unsupported


# set up case 
cd $HOME/cesm2.1.0/cases/$expname
./case.setup


# modify CAM data output format
echo "avgflag_pertape    = 'A','I','I','I','A'" >> user_nl_cam
echo "nhtfrq             = 0,-24,-24,-24,-24" >> user_nl_cam
echo "mfilt              = 1,73,73,73,73" >> user_nl_cam
echo "fincl1             = 'SST'" >> user_nl_cam
echo "fincl2             = 'V','Z3'" >> user_nl_cam
echo "fincl3             = 'U','T'" >> user_nl_cam
echo "fincl4             = 'Q','OMEGA','PS'" >> user_nl_cam
echo "fincl5             = 'SST','TREFHT','TS','PRECC','PRECL','PRECSC','PRECSL','QFLX','CLDHGH','CLDLOW','CLDMED','CLDTOT',
   'ICEFRAC','SNOWHICE','SNOWHLND','FSNS','FSNSC','FSDS','FSDSC','FLNS','FLNSC','FLDS','FLDSC','SHFLX','LHFLX',
     'SOLIN','FSNT','FSNTC','FSNTOA','FSNTOAC','FSUTOA','FLNT','FLNTC','FLUT','FLUTC','LWCF','SWCF'" >> user_nl_cam

# TRACMIP modification
# setup aerosols following APE protocol and Medeiros. 
# 1) prescribe aerosol concentrations and remove emissions 
# 2) turn radiative effects of aerosols off: make sure ozone is from prescribed APE values
echo "seasalt_emis_scale        = 0.0" >> user_nl_cam
echo "ext_frc_specifier         = ''" >> user_nl_cam
echo "tracer_cnst_specifier     = ''" >> user_nl_cam
echo "srf_emis_specifier        = ''" >> user_nl_cam
echo "micro_mg_nccons           = .TRUE." >> user_nl_cam
echo "micro_mg_nicons           = .TRUE." >> user_nl_cam
echo "prescribed_ozone_cycle_yr = 1990" >> user_nl_cam
echo "prescribed_ozone_datapath = '/cluster/projects/nn9625k/cesm/inputdata/atm/cam/ozone'" >> user_nl_cam
echo "prescribed_ozone_file     = 'apeozone_cam3_5_54.nc'" >> user_nl_cam
echo "prescribed_ozone_name	  = 'OZONE'" >> user_nl_cam


# TRACMIP modification for seasonal cycle
# change parameters and source code (Isla Simpson personal communication)
search1="orb_obliq = 0."
search2="orb_mvelp = 0."
replace1="orb_obliq = 23.5"
replace2="orb_mvelp = 102.7"
sed -i "s#${search1}#${replace1}#g" user_nl_cpl
sed -i "s#${search2}#${replace2}#g" user_nl_cpl
cp $HOME/SETUP_RUN/SRC_MOD/SEASONAL_CYCLE/seq_infodata_mod.F90 $HOME/cesm2.1.0/cases/$expname/SourceMods/src.drv/


# specify SOM forcing file
./preview_namelists
cp $HOME/cesm2.1.0/cases/$expname/CaseDocs/docn.streams.txt.som $HOME/cesm2.1.0/cases/$expname/user_docn.streams.txt.som
chmod +rw user_docn.streams.txt.som
search1="/cluster/projects/nn9625k/cesm/inputdata/ocn/docn7/SOM"
search2="default.som.forcing.aquaplanet.Qflux0_h30_sstQOBS.1degFV_c20170421.nc"
sed -i "s#${search1}#${docn_som_filepath}#g" user_docn.streams.txt.som
sed -i "s#${search2}#${docn_som_filename}#g" user_docn.streams.txt.som
./xmlchange DOCN_SOM_FILENAME=$docn_som_filename

# specify runtime and chunk size
./xmlchange JOB_WALLCLOCK_TIME=$wallclock,RESUBMIT=$resubmit,STOP_N=$stop_n,STOP_OPTION=$stop_option

# Build run
./case.build --skip-provenance-check

# submit run
./case.submit
