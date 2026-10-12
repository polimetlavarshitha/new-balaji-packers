from .models import Branch

def business_context(request):
    """
    Supplies business metadata to all templates.
    Matches project requirements for New Balaji Packers and Movers.
    """
    try:
        branches = list(Branch.objects.all().order_by('order', '-is_head_office'))
    except Exception:
        branches = []

    return {
        'BUSINESS_NAME': 'New Balaji Packers and Movers',
        'PROPRIETOR': 'Mr. Kumar',
        'TAGLINE': 'Safe Move ... Happy Home | Your Trust, Our Responsibility',
        'PRIMARY_PHONE': '9014331173',
        'SECONDARY_PHONE': '9803558899',
        'TERTIARY_PHONE': '8099333910',
        'ALL_PHONES': ['9014331173', '9803558899', '8099333910'],
        'HEAD_OFFICE_CITY': 'Vuyyuru',
        'HEAD_OFFICE_ADDRESS': 'Thotlavallaru Road, Sai Baba Temple Back Side, Vuyyuru',
        'WHATSAPP_NUMBER': '919014331173',
        'BRANCHES_LIST': branches,
        'SERVICES_LIST': [
            {
                'title': 'Household Articles Shifting',
                'desc': 'Complete home shifting with premium carton packing and damage-free transportation.',
                'icon': '🏠',
                'badge': 'Most Popular'
            },
            {
                'title': 'Office Relocation',
                'desc': 'Safe moving of office workstations, computers, IT servers, and official records.',
                'icon': '🏢',
                'badge': 'Corporate'
            },
            {
                'title': 'Packing & Careful Loading',
                'desc': 'Specialized bubble wrap, waterproof stretch film, and heavy-duty box packing.',
                'icon': '📦',
                'badge': 'Zero Damage'
            },
            {
                'title': 'Car & Bike Transportation',
                'desc': 'Dedicated closed & open car carrier vehicles with insurance assistance across India.',
                'icon': '🚗',
                'badge': 'Pan India'
            },
            {
                'title': 'Local & Intercity Shifting',
                'desc': 'Fast local moves within Vuyyuru, Vijayawada, Machilipatnam and long-distance intercity.',
                'icon': '🚚',
                'badge': '24/7 Available'
            },
            {
                'title': 'Bank & GST Invoicing',
                'desc': 'Authorized moving bills for central/state government and bank transfer reimbursements.',
                'icon': '📋',
                'badge': '100% Approved'
            },
        ]
    }
