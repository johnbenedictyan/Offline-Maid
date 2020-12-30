# Imports from the system

# Imports from django

# Imports from foreign installed apps

# Start of Context Processors

def authority(request):
    authority = None
    authority_groups = [
        'Potential Employers',
        'Agency Owners',
        'Agency Administrators',
        'Agency Managers',
        'Agency Sales Staff'
    ]
    if request.user.is_anonymous != True:
        for authority_name in authority_groups:
            if request.user.groups.filter(
                name = authority_name
            ).exists():
                authority = authority_name

    return {
        'authority': authority
    }