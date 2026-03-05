from roles.models import RoleChoices


ROLE_PERMISSIONS = {
    RoleChoices.ADMIN.value: [
        "users.read",
        "users.update",
        "services.manage",
    ],
    RoleChoices.MUSICIAN.value: [
        "profile.read",
        "profile.update",
        "services.view",
    ],
    RoleChoices.TALENT_HUNTER.value: [
        "profile.read",
        "profile.update",
        "musicians.search",
    ],
    RoleChoices.STUDENT.value: [
        "profile.read",
        "services.view",
    ],
}