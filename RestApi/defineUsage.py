compile_params = {
    'GET':{
        'Pattern':{
            '1':None,
            '2':{
                'subjectId : string'},
            '3':{
                'subjectId':'string',
                'assignId':'string'}
            }
        },
    'POST':{
        'Required fields':{
            'fileAssignment': 'file', 
            'subjectId': 'string', 
            'assignId': 'string', 
            'language': 'string',
            },
            'Additional fields':{
                'api': 'string  ##use for receive request about score',
                'otherFiles':'file  ##use for tasks that require additional files'
            },
        }
    }

compile_return = {
    'GET':{'id':'string',
            'idSubject':'string',
            'assignment':'string',
            'score':'int',
            'check':'boolean',},
    'POST':{
        'Queue': {
            'code':'string', 
            'description':'string',
            'queue':'string'
        }
    }
}

problem_params = {
    'GET':{
        'Pattern':{
            '1':None,
            '2':{
                'subjectId : string'
                },
            '3':{
                'subjectId':'string',
                'assignId':'string'
                }
            }
        },
    'POST':{
        'Required fields':{
            'file':{
                'pattern':{
                    '1':{
                        'fileAssignment': 'file',
                        'filesInput': 'file',
                        'filesOutput': 'file',
                        },
                    '2':{
                        'fileAssignment': 'file',
                        'filesInput': 'file',
                        },
                    '3':{
                        'filesInput': 'file',
                        'filesOutput': 'file',
                        },
                    },
            'subjectId': 'string', 
            'assignId': 'string', 
            'language': 'string',
            'format': 'boolean',
            },
            'Additional fields':{
                'api': 'string  ##use for receive request about score',
                'otherFiles':'file  ##use for tasks that require additional files'
            },
        }
    },
    'DELETE':{
        'Required parameter':{
            'subjectId':'string',
            'assignId':'string',
        }
    },
    'PUT':{
        'Required fields':{
            'file':{
                'pattern':{
                    '1':{
                        'fileAssignment': 'file',
                    },
                    '2':{
                        'filesInput': 'file',
                    },
                    '3':{
                        'filesOutput': 'file',
                    },
                    '4':{
                        'fileAssignment': 'file',
                        'filesInput': 'file',
                    },
                    '5':{
                        'fileAssignment': 'file',
                        'filesOutput': 'file',
                    },
                    '6':{
                        'filesInput': 'file',
                        'filesOutput': 'file',
                    },
                    '7':{
                        'fileAssignment': 'file',
                        'filesInput': 'file',
                        'filesOutput': 'file',
                    },
                },
            'subjectId': 'string', 
            'assignId': 'string', 
            'language': 'string',
            'format':'string'
            },
            'Additional fields':{
                'api': 'string  ##use for receive request about score',
                'otherFiles':'file  ##use for tasks that require additional files'
            },
        }
    }
}

problem_return = {
    'GET':{
            '/problem':{
                'idSubject':'string',
            },
            '/problem/subjectId=string':{
                'idSubject':'string',
                'assignment':'string',
                'score':'string',
                'format':'boolean',
            },
            '/problem/subjectId=string&assignId=string':{
                'Subject':'string',
                'Assignment':'string',
                'Score':'string',
                'Files Input':'string',
                'Files Output':'string',
                'Result':'string',
            },
        },
    'POST':{
        'Queue': {
            'code':'string', 
            'description':'string',
            'queue':'string'
        }
    },
    'DELETE':{
        'result':'string',
    },
    'PUT':{
        'Queue': {
            'code':'string', 
            'description':'string',
            'queue':'string'
        }
    }
}
