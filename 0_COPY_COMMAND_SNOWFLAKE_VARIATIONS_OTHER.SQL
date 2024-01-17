##lIST FILE IN S3 BUCJET

list @NEXUS.JMAN.STAGE_HOME/SRCFILES/UAS_NURSE/


// //////////////////////Copy command with specified file(s)////////////////////

COPY INTO OUR_FIRST_DB.PUBLIC.ORDERS
    FROM @MANAGE_DB.external_stages.aws_stage
    file_format= (type = csv field_delimiter=',' skip_header=1)
    files = ('OrderDetails.csv');


//////////////////////// Copy command with pattern for file names///////////////

COPY INTO OUR_FIRST_DB.PUBLIC.ORDERS
    FROM @MANAGE_DB.external_stages.aws_stage
    file_format= (type = csv field_delimiter=',' skip_header=1)
    pattern='.*Order.*';


///////////// List files contained in stage/////////////////////////////////////

LIST @MANAGE_DB.external_stages.aws_stage;


/////////////////////////// Copy command syntax with files//////////////////////

cOPY INTO DW_OWNER.UAS_ASSES_DISEASE_257100
    FROM @NEXUS.JMAN.STAGE_HOME/SRCFILES/UAS/UAS/
    file_format= (type = csv field_delimiter=',' skip_header=1 FIELD_OPTIONALLY_ENCLOSED_BY = '\"')
    files = ('UAS_ASSES_DISEASE_257100_1.csv');


cOPY INTO VNS_CHOICE1.PRCH_JSON_ORDER_DTL
    FROM @NEXUS.JMAN.STAGE_HOME/SRCFILES/PARACHUTE/
    file_format= (type = csv field_delimiter='|' skip_header=1 FIELD_OPTIONALLY_ENCLOSED_BY = '\"')
    files = ('PRCH_JSON_ORDER_DTL.csv');


COPY INTO TEMP.TEMP_HP_CONTROL
    FROM @NEXUS.JMAN.STAGE_HOME/SRCFILES/HEALTHPLEX/CLAIMS/
    file_format = (type = csv field_delimiter=',' skip_header=1)
    files = ('wf_nexus2_vnschoice1_healthplex_claims.prm');


////////////////////////FOR QUERYING DATA FROM STAGE_HOME//////////////////////

select t.$1, t.$2 from @NEXUS.JMAN.STAGE_HOME/SRCFILES/BLOCKVISION/CLAIMS/MCARE/
 (file_format => 'NEXUS.JMAN.FF_CSV_PIPE_SKIP_HEADER ', pattern=>'.*VNSNY_MEDICARE_Claims_Aging_Detail.*txt') t;


 select  t.$1, 501142,current_timestamp(), current_timestamp()
 from @NEXUS.JMAN.STAGE_HOME/SRCFILES/PHGC/PATIENT_VISIT_DIAGNOSIS.txt
 (FILE_FORMAT => 'NEXUS.JMAN.FF_CSV_PIPE_SKIP_HEADER') t


 select  t.$1, 501142,current_timestamp(), current_timestamp()
 from @NEXUS.JMAN.STAGE_HOME/SRCFILES/PHGC/PATIENT_VISIT_DIAGNOSIS.txt
 (FILE_FORMAT => 'NEXUS.JMAN.FF_CSV_PIPE_SKIP_HEADER') t


 select  NEXUS.TEMP.DW_OWNER_SF_NURSING_HOME_SEQ.NEXTVAL ,
t.$1,t.$2
from @NEXUS.JMAN.STAGE_HOME/SRCFILES/SF/NHP/NHP-Data-Dump-Nursing_Home__c.txt
(FILE_FORMAT => 'JMAN.FF_CSV_PIPE_SKIP_HEADER') t

//working 100%
select
t.$1,t.$2,t.$3,t.$4,t.$5,t.$6,t.$7,t.$8,t.$9,t.$10,t.$11,t.$12,t.$13,t.$14,t.$15,t.$16,t.$17,t.$18,t.$19,t.$20,t.$21,501876,current_timestamp(), current_timestamp()
from @NEXUS.JMAN.STAGE_HOME/SRCFILES/SF/NHP/NHP-Data-Dump-Nursing_Home__c.txt
(FILE_FORMAT => 'JMAN.FF_CSV_PIPE_SKIP_HEADER') t




////////////////////////Simple plain copy command //////////////////////////////

COPY INTO OUR_FIRST_DB.PUBLIC.ORDERS
    FROM @MANAGE_DB.external_stages.aws_stage
    file_format= (type = csv field_delimiter=',' skip_header=1);


/////// load data from csv to table ///////////






 COPY into DLAKE.CHOICE.REF_RISK_ADJ_ELIG_HCPCS_CODE from
 (select  metadata$filename, metadata$file_row_number, $1, $2, -99,current_timestamp(), current_timestamp()
  from @NEXUS.JMAN.STAGE_HOME/SRCFILES/SF/NHP/2022_Medicare_CPT_HCPCS_Codes.csv)FILE_FORMAT = NEXUS.JMAN.FF_CSV_COMMA_SKIP_HEADER_NO_ESC;


  select * from  DLAKE.CHOICE.REF_RISK_ADJ_ELIG_HCPCS_CODE


create or replace TABLE DLAKE.CHOICE.REF_RISK_ADJ_ELIG_HCPCS_CODE (
    FILE_NAME VARCHAR2,
	DL_RA_ELIG_HCPCS_SK NUMBER(38,0)  NULL,
	HCPCS_CD VARCHAR,
	HCPCS_DESC VARCHAR,
	DL_JOB_RUN_ID NUMBER(38,0) NOT NULL,
	DL_CRT_TS TIMESTAMP_NTZ(9) NOT NULL,
	DL_UPD_TS TIMESTAMP_NTZ(9) NOT NULL
);
