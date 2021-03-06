"""
Запись данных в сессию Streamlit.
"""

import streamlit.report_thread as report_thread
from streamlit.server.server import Server


class SessionState(object):
    def __init__(self, **kwargs):
        """
        Инициализация объекта сессии
        :param kwargs:
        """

        for key, val in kwargs.items():
            setattr(self, key, val)


def get(**kwargs):
    """
    Получить данные из сессии Streamlit
    :param kwargs:
    :return:
    """

    ctx = report_thread.get_report_ctx()

    this_session = None

    current_server = Server.get_current()
    if hasattr(current_server, '_session_infos'):
        session_infos = Server.get_current()._session_infos.values()
    else:
        session_infos = Server.get_current()._session_info_by_id.values()

    for session_info in session_infos:
        s = session_info.session
        if (
                # Streamlit < 0.54.0
                (hasattr(s, '_main_dg') and s._main_dg == ctx.main_dg)
                or
                # Streamlit >= 0.54.0
                (not hasattr(s, '_main_dg') and s.enqueue == ctx.enqueue)
                or
                # Streamlit >= 0.65.2
                (not hasattr(s, '_main_dg') and s._uploaded_file_mgr == ctx.uploaded_file_mgr)
        ):
            this_session = s

    if this_session is None:
        raise RuntimeError(
            "Произошла непредвиденная ошибка")

    if not hasattr(this_session, '_custom_session_state'):
        this_session._custom_session_state = SessionState(**kwargs)

    return this_session._custom_session_state
