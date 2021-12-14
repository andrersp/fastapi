# -*- coding: utf-8 -*-

from fastapi import Depends
from fastapi_permissions import (
    Allow, Authenticated, Deny, Everyone, configure_permissions, All)

from app.core.auth import get_current_user
from app.models.user import Users
from app.ext.exceptions import CustomException


acl_roles = [
    (Allow, Authenticated, 'view'),
    (Allow, 'role:dev', All),
    (Allow, "role:admin", "admin"),
    (Allow, "role:operational", "operator"),
    (Allow, "role:client", "client"),

]


def get_user_role(user: Users = Depends(get_current_user)):

    if user:
        # user is logged in
        principals = [Everyone, Authenticated]
        principals.append(user.role.role)
    else:
        # user is not logged in
        principals = [Everyone]
    
    return principals


role_exception = CustomException(status_code=403, message=[
                                 'Insufficient permissions'])

Permission = configure_permissions(get_user_role, role_exception)
