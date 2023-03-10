import os
from typing import Optional


BEACON_API_VERSION = os.environ['BEACON_API_VERSION']
BEACON_ID = os.environ['BEACON_ID']
BEACON_NAME = os.environ['BEACON_NAME']
BEACON_ENVIRONMENT = os.environ['BEACON_ENVIRONMENT']
BEACON_ORG_ID = os.environ['BEACON_ORG_ID']
BEACON_ORG_NAME = os.environ['BEACON_ORG_NAME']
BEACON_ORG_DESCRIPTION = os.environ['BEACON_ORG_DESCRIPTION']
BEACON_ORG_ADRESS = os.environ['BEACON_ORG_ADRESS']
BEACON_ORG_WELCOME_URL = os.environ['BEACON_ORG_WELCOME_URL']
BEACON_ORG_CONTACT_URL = os.environ['BEACON_ORG_CONTACT_URL']
BEACON_ORG_LOGO_URL = os.environ['BEACON_ORG_LOGO_URL']
BEACON_DESCRIPTION = os.environ['BEACON_DESCRIPTION']
BEACON_VERSION = os.environ['BEACON_VERSION']
BEACON_WELCOME_URL = os.environ['BEACON_WELCOME_URL']
BEACON_ALTERNATIVE_URL = os.environ['BEACON_ALTERNATIVE_URL']
BEACON_CREATE_DATETIME = os.environ['BEACON_CREATE_DATETIME']
BEACON_UPDATE_DATETIME = os.environ['BEACON_UPDATE_DATETIME']
BEACON_HANDOVERS = os.environ['BEACON_HANDOVERS']
BEACON_DOCUMENTATION_URL = os.environ['BEACON_DOCUMENTATION_URL']
BEACON_SERVICE_TYPE_GROUP = os.environ['BEACON_SERVICE_TYPE_GROUP']
BEACON_SERVICE_TYPE_ARTIFACT = os.environ['BEACON_SERVICE_TYPE_ARTIFACT']
BEACON_SERVICE_TYPE_VERSION = os.environ['BEACON_SERVICE_TYPE_VERSION']

'''
This document contains sample responses needed by this API endpoint
'''

# returning multiple analyses
result_sets_response = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "info": {

    },
    "meta": {
        "beaconId": BEACON_ID,
        "apiVersion": BEACON_API_VERSION,
        "returnedSchemas": [
            {
                "entityType": "info",
                "schema": "beacon-map-v2.0.0"
            }
        ],
        "returnedGranularity": "record",
        "receivedRequestSummary": {
            "apiVersion": "",  # TODO
            "requestedSchemas": [],  # TODO
            "pagination": {
                "currentPage": "",
                "limit": "",
                "nextPage": "",
                "previousPage": "",
                "skip": ""
            },
            "requestedGranularity": "record"  # TODO
        }
    },
    "response": { # OUTPUT TARGET
        "resultSets": [
            {
                "exists": False,
                "id": "datasetB",
                "results": [

                ],
                "resultsCount": 2,
                "resultsHandovers": [
                    {
                        "handoverType": {
                            "id": "EFO:0004157",
                            "label": "BAM format"
                        },
                        "note": "This handover link provides access to a summarized VCF.",
                        "url": "https://api.mygenomeservice.org/Handover/9dcc48d7-fc88-11e8-9110-b0c592dbf8c0"
                    }
                ],
                "setType": "dataset"
            }
        ]
    },
    "responseSummary": {
        "exists": True,
        "numTotalResults": 100
    }
}

# returning counts
counts_response = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "info": {

    },
    "meta": {
        "beaconId": BEACON_ID,
        "apiVersion": BEACON_API_VERSION,
        "returnedSchemas": [
            {
                "entityType": "info",
                "schema": "beacon-map-v2.0.0"
            }
        ],
        "returnedGranularity": "count",
        "receivedRequestSummary": {
            "apiVersion": "",  # TODO
            "requestedSchemas": [],  # TODO
            "pagination": {},  # TODO
            "requestedGranularity": "record"  # TODO
        }
    },
    "responseSummary": {
        "exists": True,
        "numTotalResults": 100 # OUTPUT TARGET
    }
}

# returning boolean
boolean_response = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "info": {

    },
    "meta": {
        "beaconId": BEACON_ID,
        "apiVersion": BEACON_API_VERSION,
        "returnedSchemas": [
            {
                "entityType": "info",
                "schema": "beacon-map-v2.0.0"
            }
        ],
        "returnedGranularity": "boolean",
        "receivedRequestSummary": {
            "apiVersion": "",  # TODO
            "requestedSchemas": [],  # TODO
            "pagination": {},  # TODO
            "requestedGranularity": "boolean"  # TODO
        }
    },
    "responseSummary": {
        "exists": True # OUTPUT TARGET
    }
}


# Helpers start


def get_pagination_object(skip, limit):
    return {
        "limit": limit,
        "skip": skip
    }


def get_cursor_object(currentPage, nextPage, previousPage):
    return {
        "currentPage": currentPage,
        "nextPage": nextPage,
        "previousPage": previousPage,
    }


def get_result_sets_response(*, 
        reqAPI=BEACON_API_VERSION, 
        reqPagination={}, 
        results=[], 
        setType=None, 
        info={},
        exists=False,
        total=0):

    return { 
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "info": info,
        "meta": {
            "beaconId": BEACON_ID,
            "apiVersion": BEACON_API_VERSION,
            "returnedSchemas": [
                {
                    "entityType": "info",
                    "schema": "beacon-map-v2.0.0"
                }
            ],
            "returnedGranularity": 'record',
            "receivedRequestSummary": {
                "apiVersion": reqAPI,
                "requestedSchemas": [], # TODO define this
                "pagination": reqPagination,
                "requestedGranularity": 'record'
            }
        },
        "response": { # OUTPUT TARGET
            "resultSets": [
                {
                    "exists": len(results) > 0,
                    "id": "redacted",
                    "results": results,
                    "resultsCount": len(results),
                    "resultsHandovers": [], # TODO update when available
                    "setType": setType
                }
            ]
        },
        "responseSummary": {
            "exists": exists,
            "numTotalResults": total
        }
    }


def get_counts_response(*, 
        reqAPI=BEACON_API_VERSION, 
        reqGranularity='count',
        exists=False,
        count=0,
        info={}):
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "info": info,
        "meta": {
            "beaconId": BEACON_ID,
            "apiVersion": BEACON_API_VERSION,
            "returnedSchemas": [
                {
                    "entityType": "info",
                    "schema": "beacon-map-v2.0.0"
                }
            ],
            "returnedGranularity": "count",
            "receivedRequestSummary": {
                "apiVersion": reqAPI,  # TODO
                "requestedSchemas": [],  # TODO
                "pagination":{},
                "requestedGranularity": reqGranularity
            }
        },
        "responseSummary": {
            "exists": exists,
            "numTotalResults": count
        }
    }


def get_boolean_response(*, 
        reqAPI=BEACON_API_VERSION, 
        reqGranularity='boolean',
        exists=False,
        info={}):
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "info": info,
        "meta": {
            "beaconId": BEACON_ID,
            "apiVersion": BEACON_API_VERSION,
            "returnedSchemas": [
                {
                    "entityType": "info",
                    "schema": "beacon-map-v2.0.0"
                }
            ],
            "returnedGranularity": "boolean",
            "receivedRequestSummary": {
                "apiVersion": reqAPI,  # TODO
                "requestedSchemas": [],  # TODO
                "pagination": {},  # TODO
                "requestedGranularity": reqGranularity
            }
        },
        "responseSummary": {
            "exists": exists
        }
    }

# Helpers end

# 
# Start Thirdparty Code
# Code from https://github.com/EGA-archive/beacon2-ri-api
# Apache License 2.0
# 

from .requests import RequestParams, Granularity
from .schemas import DefaultSchemas


def build_meta(qparams: RequestParams, entity_schema: Optional[DefaultSchemas], returned_granularity: Granularity):
    """"Builds the `meta` part of the response

    We assume that receivedRequest is the evaluated request (qparams) sent by the user.
    """
    # CHANGE: variables taken from terraform
    meta = {
        'beaconId': BEACON_ID,
        'apiVersion': BEACON_API_VERSION,
        'returnedGranularity': returned_granularity,
        'receivedRequestSummary': qparams.summary(),
        'returnedSchemas': [entity_schema.value] if entity_schema is not None else []
    }
    return meta


def build_response_summary(exists, num_total_results):
    if num_total_results is None:
        return {
            'exists': exists
        }
    else:
        return {
            'exists': exists,
            'numTotalResults': num_total_results
        }


def build_response(data, num_total_results, qparams, func):
    """"Fills the `response` part with the correct format in `results`"""

    response = {
        'id': '', # TODO: Set the name of the dataset/cohort
        'setType': '', # TODO: Set the type of collection
        'exists': num_total_results > 0,
        'resultsCount': num_total_results,
        'results': data,
        # 'info': None,
        'resultsHandover': None,  # build_results_handover
    }

    return response


########################################
# Resultset Response
########################################

def build_beacon_resultset_response(data,
                                    num_total_results,
                                    qparams: RequestParams,
                                    func_response_type,
                                    entity_schema: DefaultSchemas):
    """"
    Transform data into the Beacon response format.
    """

    beacon_response = {
        'meta': build_meta(qparams, entity_schema, Granularity.RECORD),
        'responseSummary': build_response_summary(num_total_results > 0, num_total_results),
        # TODO: 'extendedInfo': build_extended_info(),
        'response': {
            'resultSets': [build_response(data, num_total_results, qparams, func_response_type)]
        },
        # CHANGE: variables taken from terraform
        'beaconHandovers': BEACON_HANDOVERS,
    }
    return beacon_response

########################################
# Count Response
########################################

def build_beacon_count_response(data,
                                    num_total_results,
                                    qparams: RequestParams,
                                    func_response_type,
                                    entity_schema: DefaultSchemas):
    """"
    Transform data into the Beacon response format.
    """

    beacon_response = {
        'meta': build_meta(qparams, entity_schema, Granularity.COUNT),
        'responseSummary': build_response_summary(num_total_results > 0, num_total_results),
        # TODO: 'extendedInfo': build_extended_info(),
        # CHANGE: variables taken from terraform
        'beaconHandovers': BEACON_HANDOVERS,
    }
    return beacon_response

########################################
# Boolean Response
########################################

def build_beacon_boolean_response(data,
                                    num_total_results,
                                    qparams: RequestParams,
                                    func_response_type,
                                    entity_schema: DefaultSchemas):
    """"
    Transform data into the Beacon response format.
    """

    beacon_response = {
        'meta': build_meta(qparams, entity_schema, Granularity.BOOLEAN),
        'responseSummary': build_response_summary(num_total_results > 0, None),
        # TODO: 'extendedInfo': build_extended_info(),
        # CHANGE: variables taken from terraform
        'beaconHandovers': BEACON_HANDOVERS,
    }
    return beacon_response

########################################
# Collection Response
########################################

def build_beacon_collection_response(data, num_total_results, qparams: RequestParams, func_response_type, entity_schema: DefaultSchemas):
    beacon_response = {
        'meta': build_meta(qparams, entity_schema, Granularity.RECORD),
        'responseSummary': build_response_summary(num_total_results > 0, num_total_results),
        # TODO: 'info': build_extended_info(),
        'beaconHandovers': BEACON_HANDOVERS,
        'response': {
            'collections': func_response_type(data, qparams)
        }
    }
    return beacon_response

########################################
# Info Response
########################################

def build_beacon_info_response(data, qparams, func_response_type, authorized_datasets=None):
    if authorized_datasets is None:
        authorized_datasets = []

    # CHANGE: variables taken from terraform
    beacon_response = {
        'meta': build_meta(qparams, None, Granularity.RECORD),
        'response': {
            'id': BEACON_ID,
            'name': BEACON_NAME,
            'apiVersion': BEACON_API_VERSION,
            'environment': BEACON_ENVIRONMENT,
            'organization': {
                'id': BEACON_ORG_ID,
                'name': BEACON_ORG_NAME,
                'description': BEACON_ORG_DESCRIPTION,
                'address': BEACON_ORG_ADRESS,
                'welcomeUrl': BEACON_ORG_WELCOME_URL,
                'contactUrl': BEACON_ORG_CONTACT_URL,
                'logoUrl': BEACON_ORG_LOGO_URL,
            },
            'description': BEACON_DESCRIPTION,
            'version': BEACON_VERSION,
            'welcomeUrl': BEACON_WELCOME_URL,
            'alternativeUrl': BEACON_ALTERNATIVE_URL,
            'createDateTime': BEACON_CREATE_DATETIME,
            'updateDateTime': BEACON_UPDATE_DATETIME,
            'datasets': func_response_type(data, qparams, authorized_datasets),
        }
    }

    return beacon_response

########################################
# Service Info Response
########################################

def build_beacon_service_info_response():
    # CHANGE: variables taken from terraform
    beacon_response = {
        'id': BEACON_ID,
        'name': BEACON_NAME,
        'type': {
            'group': BEACON_SERVICE_TYPE_GROUP,
            'artifact': BEACON_SERVICE_TYPE_ARTIFACT,
            'version': BEACON_SERVICE_TYPE_VERSION
        },
        'description': BEACON_DESCRIPTION,
        'organization': {
            'name': BEACON_ORG_NAME,
            'url': BEACON_WELCOME_URL
        },
        'contactUrl': BEACON_ORG_CONTACT_URL,
        'documentationUrl': BEACON_DOCUMENTATION_URL,
        'createdAt': BEACON_CREATE_DATETIME,
        'updatedAt': BEACON_UPDATE_DATETIME,
        'environment': BEACON_ENVIRONMENT,
        'version': BEACON_VERSION,
    }

    return beacon_response

########################################
# Filtering terms Response
########################################

def build_filtering_terms_response(filtering_terms, resources, qparams: RequestParams):
    return {
        "meta": build_meta(qparams, None, Granularity.RECORD),
        "response": {
            "resources": resources,
            "filteringTerms": filtering_terms
        }
    }

# 
# End Thirdparty Code
#
