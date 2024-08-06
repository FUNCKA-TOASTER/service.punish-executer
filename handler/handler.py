from Typing import Any, Tuple
from vk_api import VkApiError, VkApi
from loguru import logger
from toaster.keyboards import Keyboard, Callback, ButtonColor
from toaster.broker.event import Punishment
from toaster_utils.scripts import (
    get_log_peers,
    get_user_warns,
    open_menu_session,
    set_user_warns,
)
from db import TOASTER_DB
import config


ExecResult = Tuple[bool, int]

BANNERS = {
    0: "photo-219135617_457239030",
    1: "photo-219135617_457239031",
    2: "photo-219135617_457239032",
    3: "photo-219135617_457239033",
    4: "photo-219135617_457239034",
    5: "photo-219135617_457239035",
    6: "photo-219135617_457239036",
    7: "photo-219135617_457239037",
    8: "photo-219135617_457239038",
    9: "photo-219135617_457239039",
    10: "photo-219135617_457239029",
}


class PunishmentHandler:
    def __call__(self, event: Punishment) -> None:
        try:
            result, summary = self._execute(event)
            if result:
                if event.punishment_type == "kick":
                    comment = "Исключён."
                elif event.punishment_type == "warn":
                    comment = f"Выданы предупреждения: {event.points} ({summary}/10)"
                    if summary == 10:
                        comment = "Исключён. | " + comment

                    self._alert_user(event, summary)
                else:
                    logger.info("Messages deleted.")
                    return

                self._alert_about_execution(comment, event)
                logger.info("Punishment executed.")

        except Exception as error:
            logger.error(error)

        finally:
            self._delete_target_message(event)

    def _execute(self, event: Punishment) -> ExecResult:
        if event.punishment_type == "delete":
            return True, 0

        if event.punishment_type == "kick":
            self._kick_user(event)
            return True, 10

        if event.punishment_type == "warn":
            warns_info = get_user_warns(
                db_instance=TOASTER_DB,
                uuid=event.uuid,
                bpid=event.bpid,
            )

            if warns_info:
                current_warns, _ = warns_info
            else:
                current_warns = 0

            new_warns = max(0, min(current_warns + event.points, 10))

            set_user_warns(
                db_instance=TOASTER_DB,
                bpid=event.bpid,
                uuid=event.uuid,
                points=new_warns,
            )

            return True, new_warns

        return False, 0

    def _kick_user(self, event: Punishment) -> None:
        try:
            api = self._get_api()
            api.messages.removeChatUser(
                chat_id=event.bpid - 2000000000,
                user_id=event.uuid,
            )
        except VkApiError as e:
            logger.info(f"Could not kick target user: {e}")

    def _delete_target_message(self, event: Punishment) -> None:
        try:
            api = self._get_api()
            api.messages.delete(
                delete_for_all=1,
                peer_id=event.bpid,
                cmids=event.cmids,
            )

        except VkApiError as e:
            logger.info(f"Could not delete target message: {e}")

    def _alert_user(self, event: Punishment, points: int) -> None:
        banner = BANNERS.get(points)
        if not banner:
            raise ValueError("Unable to find suitable banner.")

        keyboard = (
            Keyboard(inline=True, one_time=False, owner_id=event.uuid)
            .add_row()
            .add_button(
                Callback(label="Скрыть", payload={"action_name": "close_menu"}),
                ButtonColor.PRIMARY,
            )
        )

        text = f"[id{event.uuid}|Пользователь] | {event.comment} | Предупреждения: {event.points} ({points}/10)"
        api = self._get_api()

        send_info = api.messages.send(
            peer_ids=event.bpid,
            random_id=0,
            message=text,
            keyboard=keyboard.json,
        )
        cmid = send_info[0]["conversation_message_id"]

        open_menu_session(
            db_instance=TOASTER_DB,
            bpid=event.peer.bpid,
            cmid=cmid,
        )

    def _alert_about_execution(self, comment: str, event: Punishment) -> None:
        answer_text = f"[id{event.uuid}|Пользователь] | {comment} \n"

        api = self._get_api()
        for bpid in get_log_peers(db_instance=TOASTER_DB):
            api.messages.send(
                peer_ids=bpid,
                random_id=0,
                message=answer_text,
            )

    def _get_api(self) -> Any:
        session = VkApi(
            token=config.TOKEN,
            api_version=config.API_VERSION,
        )
        return session.get_api()
