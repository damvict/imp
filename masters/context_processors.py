def group_check(request):
    user = request.user
    show_common_masters_menu = False
    if request.user.is_authenticated:
        user_groups = request.user.groups.values_list('name', flat=True)
        print("DEBUG: Authenticated user:", user.username)
        print("DEBUG: User groups:", user_groups)
        show_common_masters_menu = bool(set(user_groups) & {"Imports Department", "Admin"})
        print("DEBUG: Show menu?", show_common_masters_menu)
    else:
        show_common_masters_menu = False
        print("DEBUG: User is not authenticated")
    return {
        'show_common_masters_menu': show_common_masters_menu
    }


