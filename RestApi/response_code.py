#Compile response
COMPILE_STATUS_OK = {
    "Status":True,
    "Code": 100,
    "Description":"OK"}
COMPILE_STATUS_EROOR_1 = {
    "Status":False,
    "Code": 101,
    "Description":"Field language does not match language supported by the system."}
COMPILE_STATUS_EROOR_2 = {
    "Status":False,
    "Code": 102,
    "Description":"This file type does not match the file type supported by the system."}
COMPILE_STATUS_EROOR_3 = {
    "Status":False,
    "Code": 103,
    "Description":"Subject not found. Please contact admin"}
COMPILE_STATUS_EROOR_4 = {
    "Status":False,
    "Code": 104,
    "Description":"Assignment not found. Please contact admin"}
COMPILE_STATUS_EROOR_5 = {
    "Status":False,
    "Code": 105,
    "Description":"Solution not found. Please contact admin"}
COMPILE_STATUS_ERROR_6 = {
    "Status":False,
    "Code": 106,
    "Description":"field language or type file not match with type assignment"}

#Problem response
PROBLEM_STATUS_OK = {
    "Status":True,
    "Code": 200,
    "Description":"OK"}
PROBLEM_STATUS_ERROR_1 = {
    "Status":False,
    "Code": 201,
    "Description":"Field language does not match language supported by the system."}
PROBLEM_STATUS_ERROR_2 = {
    "Status":False,
    "Code": 202,
    "Description":"This file type does not match the file type supported by the system."}
PROBLEM_STATUS_ERROR_3 = {
    "Status":False,
    "Code": 203,
    "Description":"Subject not found. please register this subject."}
PROBLEM_STATUS_ERROR_4 = {
    "Status":False,
    "Code": 204,
    "Description":"Assignment already exist"}
PROBLEM_STATUS_ERROR_5 = {
    "Status":False,
    "Code": 205,
    "Description":"Subject not found. Please contact admin"}
PROBLEM_STATUS_ERROR_6 = {
    "Status":False,
    "Code": 206,
    "Description":"Assignment not found. Please contact admin"}
PROBLEM_STATUS_ERROR_7 = {
    "Status":False,
    "Code": 207,
    "Description":"Input and Output file must have same number"}
PROBLEM_STATUS_ERROR_8 = {
    "Status":False,
    "Code": 208,
    "Description":"Input and Output files must have same name"}
PROBLEM_STATUS_ERROR_9 = {
    "Status":False,
    "Code": 209,
    "Description":"Out of data file name. If you want to add new file input or output, please add new filesInput and filesOutput with the same number and the same name."}
PROBLEM_STATUS_ERROR_10 = {
    "Status":False,
    "Code": 210,
    "Description":"Wrong format. field format must be true or false"}
PROBLEM_STATUS_ERROR_11 = {
    "Status":False,
    "Code": 211,
    "Description":"field language or type file not match with type assignment"}