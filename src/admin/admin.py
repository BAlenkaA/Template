from sqladmin import ModelView

from src.databases.database import db_manager
from src.models.user import User, Role


class CustomModelView(ModelView):
    async def _run_query(self, stmt):
        async with db_manager.session() as session:
            result = await session.execute(stmt)
            return result.scalars().all()


class UserAdmin(CustomModelView, model=User):
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    column_list = ["username", "role_name"]
    column_details_list = ["username", "role_name"]
    column_labels = {
        "username": "Имя пользователя",
        "role_name": "Роль"
    }

    def get_role_name(self, user: User) -> str:
        return user.role.name if user.role else "No Role"

    column_formatters = {
        "role_name": lambda m, a: UserAdmin.get_role_name(a, m)
    }


class RoleAdmin(CustomModelView, model=Role):
    name = "Роль"
    name_plural = "Роли"
    icon = "fa-solid fa-user-secret"
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    column_list = ["name"]

    column_labels = {
        "name": "Название",
    }

# class GeoAdmin(CustomModelView, model=Geo):
#     name = "Гео запрос"
#     name_plural = "Гео запросы"
#     icon = "fa-solid fa-book"
#     can_create = False
#     can_edit = False
#     can_delete = False
#     can_view_details = True
#     column_list = ["cadastre_number", "latitude", "longitude", "result", "created_at"]
#
#     column_labels = {
#         "cadastre_number": "Кадастровый номер",
#         "latitude": "Широта",
#         "longitude": "Долгота",
#         "result": "Результат ответа сервера",
#         "created_at": "Дата запроса",
#     }
#
#     def format_created_at(self, created_at) -> str:
#         return created_at.strftime("%Y-%m-%d %H:%M:%S")
#
#     column_formatters = {
#         "created_at": lambda m, a: UserAdmin.format_created_at(a, m.created_at),
#     }