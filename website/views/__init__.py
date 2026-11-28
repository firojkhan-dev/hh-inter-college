from .admissions import admission_enquiry
from .gallery import gallery_list
from .language import switch_language
from .notices import notice_detail, notice_list
from .pages import information_page
from .public import home
from .search import site_search
from .staff import (
    staff_admissions,
    staff_dashboard,
    staff_logout,
    staff_login,
    staff_messages,
    update_admission_status,
)
from .teachers import teacher_detail

__all__ = [
    "admission_enquiry",
    "gallery_list",
    "home",
    "information_page",
    "notice_detail",
    "notice_list",
    "site_search",
    "staff_admissions",
    "staff_dashboard",
    "staff_login",
    "staff_logout",
    "staff_messages",
    "switch_language",
    "teacher_detail",
    "update_admission_status",
]
