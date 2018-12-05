from django.contrib.auth.models import Group, Permission

permissions = Permission.objects.all()


def create_groups():
    """
    Creating groups of users
    """
    Group.objects.all().delete()
    print("All groups were deleted.")
    create_curators_group()
    create_students_group()


def create_curators_group():
    """
    Creating curators group
    """
    group_curators = Group.objects.create(name="curators")
    print("Group: {} is created.".format(group_curators))
    group_curators_permissions = [
        # curator
        permissions.get(codename="change_curator"),
        permissions.get(codename="view_curator"),
        # skill
        permissions.get(codename="view_skill"),
        # student
        permissions.get(codename="view_student"),
        # subject
        permissions.get(codename="view_subject"),
        # suggestion theme
        permissions.get(codename="add_suggestiontheme"),
        permissions.get(codename="change_suggestiontheme"),
        permissions.get(codename="delete_suggestiontheme"),
        permissions.get(codename="view_suggestiontheme"),
        # suggestion theme comment
        permissions.get(codename="change_suggestionthemecomment"),
        permissions.get(codename="view_suggestionthemecomment"),
        # suggestion theme progress
        permissions.get(codename="view_suggestionthemeprogress"),
        # suggestion theme status
        permissions.get(codename="view_suggestionthemestatus"),
        # theme
        permissions.get(codename="add_theme"),
        permissions.get(codename="change_theme"),
        permissions.get(codename="delete_theme"),
        permissions.get(codename="view_theme"),
        # work
        permissions.get(codename="add_work"),
        permissions.get(codename="change_work"),
        permissions.get(codename="delete_work"),
        permissions.get(codename="view_work"),
        # work step
        permissions.get(codename="add_workstep"),
        permissions.get(codename="change_workstep"),
        permissions.get(codename="delete_workstep"),
        permissions.get(codename="view_workstep"),
        # work step comment
        permissions.get(codename="add_workstepcomment"),
        permissions.get(codename="change_workstepcomment"),
        permissions.get(codename="delete_workstepcomment"),
        permissions.get(codename="view_workstepcomment"),
        # work step material
        permissions.get(codename="add_workstepmaterial"),
        permissions.get(codename="change_workstepmaterial"),
        permissions.get(codename="delete_workstepmaterial"),
        permissions.get(codename="view_workstepmaterial"),
        # work step status
        permissions.get(codename="view_workstepstatus"),
    ]
    for permission in group_curators_permissions:
        group_curators.permissions.add(permission)
    group_curators.save()
    print("Group: {} permissions granted.".format(group_curators))


def create_students_group():
    """
    Creating students group
    """
    group_students = Group.objects.create(name="students")
    print("Group: {} is created.".format(group_students))
    # group_students_permissions = [
    #     # curator
    #     permissions.get(codename="change_curator"),
    #     permissions.get(codename="view_curator"),
    #     # skill
    #     permissions.get(codename="view_skill"),
    #     # student
    #     permissions.get(codename="view_student"),
    #     # subject
    #     permissions.get(codename="view_subject"),
    #     # suggestion theme
    #     permissions.get(codename="add_suggestiontheme"),
    #     permissions.get(codename="change_suggestiontheme"),
    #     permissions.get(codename="delete_suggestiontheme"),
    #     permissions.get(codename="view_suggestiontheme"),
    #     # suggestion theme comment
    #     permissions.get(codename="change_suggestionthemecomment"),
    #     permissions.get(codename="view_suggestionthemecomment"),
    #     # suggestion theme progress
    #     permissions.get(codename="view_suggestionthemeprogress"),
    #     # suggestion theme status
    #     permissions.get(codename="view_suggestionthemestatus"),
    #     # theme
    #     permissions.get(codename="add_theme"),
    #     permissions.get(codename="change_theme"),
    #     permissions.get(codename="delete_theme"),
    #     permissions.get(codename="view_theme"),
    #     # work
    #     permissions.get(codename="add_work"),
    #     permissions.get(codename="change_work"),
    #     permissions.get(codename="delete_work"),
    #     permissions.get(codename="view_work"),
    #     # work step
    #     permissions.get(codename="add_workstep"),
    #     permissions.get(codename="change_workstep"),
    #     permissions.get(codename="delete_workstep"),
    #     permissions.get(codename="view_workstep"),
    #     # work step comment
    #     permissions.get(codename="add_workstepcomment"),
    #     permissions.get(codename="change_workstepcomment"),
    #     permissions.get(codename="delete_workstepcomment"),
    #     permissions.get(codename="view_workstepcomment"),
    #     # work step material
    #     permissions.get(codename="add_workstepmaterial"),
    #     permissions.get(codename="change_workstepmaterial"),
    #     permissions.get(codename="delete_workstepmaterial"),
    #     permissions.get(codename="view_workstepmaterial"),
    #     # work step status
    #     permissions.get(codename="view_workstepstatus"),
    # ]
    # for permission in group_curators_permissions:
    #     group_curators.permissions.add(permission)
    # group_curators.save()
    # print("Group: {} permissions granted.".format(group_curators))


def do():
    create_curators_group()
    create_students_group()
