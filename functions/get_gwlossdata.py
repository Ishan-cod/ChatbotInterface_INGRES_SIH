import requests
from langchain.tools import tool
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@tool
def get_gwlossdata(state : str, year : int):

    """
    Get the summarized data for the loss in groundwater for an Indian state and year.
    Contain data for total loss, poor quality loss, loss in command and non-command areas.
    
    Args:
        state: Name of the Indian state (e.g., "MADHYA PRADESH", "RAJASTHAN")
        year: Year for data (eg : 2025 , 2024)
    
    Returns:
        Dictionary with groundwater loss in data including poor quality, total, command, and non_command values.
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
                'message' : f"The groundwater loss in due to various factors for state ${required_state} is fetched the unit of data is hectare-meter",
                'data defination' : {
                    'poor quality' : 'The quantity of groundwater lost due to its poor quality',
                    'total' : 'Net of groundwater lost.',
                    'command' : 'The rainwater which goes to recharge the groundwater of irrigated areas',
                    'non command' : 'The rainwater which goes to recharge the groundwater of non-irrigated areas'
                },
                'data' : {
                    'poor quality' : match['loss']['poor_quality'] ,
                    'total' : match['loss']['total'],
                    'command' : match['loss']['command'],
                    'non_command':match['loss']['non_command']
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