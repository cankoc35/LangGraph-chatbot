from langchain_core.tools import tool

QUERY_BANK = [
    {
        "name": "vehicle_route_by_date",
        "description": "Get where a vehicle went in a specific date range.",
        "params": ["plate", "start_date", "end_date"],
        "endpoint": "/vehicle/route"
    },
    {
        "name": "shipment_status_by_plate",
        "description": "Get current shipment status of a specific vehicle.",
        "params": ["plate", "shipment_id"],
        "endpoint": "/shipment/status"
    },
    {
        "name": "total_distance_by_date",
        "description": "Get total distance traveled by a vehicle in a given date range.",
        "params": ["plate", "start_date", "end_date"],
        "endpoint": "/vehicle/distance"
    },
    {
        "name": "current_location_by_plate",
        "description": "Get current location of a specific vehicle.",
        "params": ["plate"],
        "endpoint": "/vehicle/current_location"
    }
]

@tool
def vehicle_route_by_date(plate: str, start_date: str, end_date: str) -> str:
    """
    Get where a vehicle went in a specific date range.
    """
    return {"endpoint": "/vehicle/route", "params": {"plate": plate, "start_date": start_date, "end_date": end_date}}

@tool 
def shipment_status_by_plate(plate: str, shipment_id: str) -> str:
    """
    Get current shipment status of a specific vehicle.
    """
    return {"endpoint": "/shipment/status", "params": {"plate": plate, "shipment_id": shipment_id}}

@tool 
def total_distance_by_date(plate: str, start_date: str, end_date: str) -> str:
    """
    Get total distance traveled by a vehicle in a given date range.
    """
    return {"endpoint": "/vehicle/distance", "params": {"plate": plate, "start_date": start_date, "end_date": end_date}}

@tool
def current_location_by_plate(plate: str) -> str:
    """
    Get current location of a specific vehicle.
    """
    return {"endpoint": "/vehicle/current_location", "params": {"plate": plate}}

QUERY_BANK_TOOLS = [
    vehicle_route_by_date,
    shipment_status_by_plate,
    total_distance_by_date,
    current_location_by_plate
]
