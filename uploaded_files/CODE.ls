/PROG CODE
/ATTR
OWNER		= NOC_FANU;
COMMENT		= "NOC_FANUC";
PROG_SIZE	= 328;
CREATE		= DATE 97-07-08  TIME 03:05:20;
MODIFIED	= DATE 17-07-08  TIME 03:05:26;
FILE_NAME	= ;
VERSION		= 0;
LINE_COUNT	= 10;
MEMORY_SIZE	= 692;
PROTECT		= READ_WRITE;
TCD:  STACK_SIZE	= 0,
      TASK_PRIORITY	= 0,
      TIME_SLICE	= 0,
      BUSY_LAMP_OFF	= 0,
      ABORT_REQUEST	= 0,
      PAUSE_REQUEST	= 0;
DEFAULT_GROUP	= 1,*,*,*,*;
CONTROL_CODE	= 00000000 00000000;
/APPL
/MN
1:UFRAME_NUM=1 ;
2: CALL CODE1_0;
3: CALL CODE1_1;
2: CALL CODE2;
2: CALL CODE3;
2: CALL CODE4;
2: CALL CODE5;
2: CALL CODE6;

/END