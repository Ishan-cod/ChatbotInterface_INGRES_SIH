import requests
from langchain.tools import tool
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@tool
def get_blockcount_classification(state : str, year : int):

    """
    Get the count of the blocks in a state which falls in safe, over_exploited, semi_critical and critical category based on stage of extraction.
    
    Args:
        state: Name of the Indian state (e.g., "MADHYA PRADESH", "RAJASTHAN")
        year: Year for data (eg : 2025 , 2024)
    
    Returns:
        Dictionary with count of blocks in a state categorized into over_exploited, semi_critical, critical and safe.
    """
    try: 
        required_state = state.upper().strip();

        if year < 2014 and year > 2025:
            return {"success" : False,
                    "message" : "Data fetch failed"}
        
        url = 'https://ingres.iith.ac.in/api/gec/getBusinessDataForUserOpen'

        payload = {
        "approvalLevel": 1,
        "category": "all",
        "component": "recharge",
        "computationType": "normal",
        "locname": "INDIA",
        "loctype": "COUNTRY",
        "locuuid": "ffce954d-24e1-494b-ba7e-0931d8ad6085",
        "parentuuid": "ffce954d-24e1-494b-ba7e-0931d8ad6085",
        "period": "annual",
        "stateuuid": None,
        "verificationStatus": 1,
        "view": "admin",
        "year": '2024-2025'
        }
        
        api_response = requests.post(url=url,json=payload)
        if not api_response or api_response.status_code != 200:
            return {'success' : False,
                    'message' : 'API request failed'}
        
        data = api_response.json();

        match = next((item for item in data if item["locationName"] == required_state), None)

        if not match:
            return {'success' : False,
                    'message' : 'State data not available'}

        if match:
            return {
                'success' : True,
                'message' : f"The count of blocks for state of ${required_state} is fetched with categories safe, over_exploited, semi_critical and critical categorization made according to stage of extraction",
                'data defination' : {
                    'Stage of Extraction' : 'The ratio of total annual groundwater extraction to net annual groundwater availability in percentage',
                    'over_exploited' : 'number of blocks whose stage of extraction is more than 100%',
                    'semi_critical' : 'number of blocks whose stage of extraction is more than 70percent but less than or equal to 90%',
                    'critical' : 'number of blocks whose stage of extraction is more than 90 percent but less than or equal to 100%',
                    'safe' : 'number of blocks whose stage of extraction is less than or equal to 70%'
                },
                'data' : {
                    'over_exploited' : match['reportSummary']['total']['BLOCK']['over_exploited'] ,
                    'semi_critical' : match['reportSummary']['total']['BLOCK']['semi_critical'],
                    'critical' : match['reportSummary']['total']['BLOCK']['critical'],
                    'safe':match['reportSummary']['total']['BLOCK']['safe']
                }
            }
                    
    except requests.exceptions.Timeout:
        return {
            'success': False,
            'message': 'API request timed out. Please try again.'
        }
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error: {str(e)}")
        return {
            'success': False,
            'message': f'Network error: {str(e)}'
        }
    except Exception as e:
        logger.error(f"Unexpected error in getgroundwater: {str(e)}")
        return {
            'success': False,
            'message': f'Unexpected error occurred: {str(e)}'
        }