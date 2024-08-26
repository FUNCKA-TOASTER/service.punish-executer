import time  # Для костыля
from typing import Any, Tuple, NoReturn, Optional
from vk_api import VkApiError, VkApi
from loguru import logger
from funcka_bots.keyboards import Keyboard, Callback, ButtonColor
from funcka_bots.events import BaseEvent
from funcka_bots.handler import ABCHandler
from toaster.scripts import (
    get_log_peers,
    get_user_warns,
    open_menu_session,
    set_user_warns,
    get_chat_peers,
)
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


class PunishmentHandler(ABCHandler):
    """Punishment handler class."""

    def __call__(self, event: BaseEvent) -> None:
        try:
            result, summary = self._execute(event)
            if result:
                if event.punishment_type == "kick":
                    comment = "Исключён."
                elif event.punishment_type in ("warn", "unwarn"):
                    if event.punishment_type == "warn":
                        comment = "Выданы "
                        points = event.warn.points
                    else:
                        comment = "Сняты "
                        points = abs(event.unwarn.points)

                    comment += f"предупреждения: {points} ({summary}/10)"

                    self._alert_user(event, summary)
                    if summary == 10:
                        comment = "Исключён. | " + comment
                        self._kick_user(event)

                else:
                    logger.info("Messages deleted.")
                    return

                self._alert_about_execution(comment, event)
                logger.info("Punishment executed.")

        except Exception as error:
            logger.error(error)

        finally:
            self._delete_target_message(event)

    def _execute(self, event: BaseEvent) -> ExecResult:
        # TODO: Этот костыль нужен, чтобы алерт об отработке команды успел переслать сообщения
        # Нуждается в фиксе
        time.sleep(0.2)

        if event.punishment_type == "delete":
            return True, 0

        if event.punishment_type == "kick":
            self._kick_user(event, event.kick.mode)
            return True, 10

        if event.punishment_type in ("warn", "unwarn"):
            if event.punishment_type == "warn":
                points = event.warn.points
            else:
                points = event.unwarn.points

            warns_info = get_user_warns(uuid=event.user.uuid, bpid=event.peer.bpid)

            if warns_info:
                current_warns, _ = warns_info
            else:
                if event.punishment_type == "unwarn":
                    return False, 0
                current_warns = 0

            new_warns = max(0, min(current_warns + points, 10))

            set_user_warns(bpid=event.peer.bpid, uuid=event.user.uuid, points=new_warns)

            return True, new_warns

        return False, 0

    def _kick_user(self, event: BaseEvent, mode: str = "local") -> Optional[NoReturn]:
        api = self._get_api()

        if mode == "local":
            cids = [event.peer.bpid - config.VK_PEER_ID_DELAY]
        elif mode == "global":
            cids = [bpid - config.VK_PEER_ID_DELAY for bpid in get_chat_peers()]
        else:
            raise ValueError(f"Unknown kick mode '{mode}'.")

        for chat_id in cids:
            try:
                api.messages.removeChatUser(
                    chat_id=chat_id,
                    user_id=event.user.uuid,
                )
            except VkApiError as e:
                logger.info(f"Could not kick target user: {e}")

    def _delete_target_message(self, event: BaseEvent) -> None:
        try:
            if not event.message.cmid:
                raise ValueError("Message deletion cancelled. No target messages.")

            api = self._get_api()
            api.messages.delete(
                delete_for_all=1,
                peer_id=event.peer.bpid,
                cmids=event.message.cmid,
            )

        except (VkApiError, ValueError) as e:
            logger.info(f"Could not delete target message: {e}")

    def _alert_user(self, event: BaseEvent, points: int) -> None:
        banner = BANNERS.get(points)
        if not banner:
            raise ValueError("Unable to find suitable banner.")

        keyboard = (
            Keyboard(inline=True, one_time=False, owner_id=event.user.uuid)
            .add_row()
            .add_button(
                Callback(label="Скрыть", payload={"action_name": "close_menu"}),
                ButtonColor.PRIMARY,
            )
        )

        if event.punishment_type == "warn":
            points = event.warn.points
        else:
            points = abs(event.unwarn.points)

        text = (
            f"[id{event.user.uuid}|Пользователь]\n"
            f" {event.punishment_comment} \n"
            f"Кол-во предупреждений: {points}"
        )
        api = self._get_api()

        send_info = api.messages.send(
            peer_ids=event.peer.bpid,
            random_id=0,
            message=text,
            attachment=banner,
            keyboard=keyboard.json,
        )
        cmid = send_info[0]["conversation_message_id"]

        open_menu_session(bpid=event.peer.bpid, cmid=cmid)

    def _alert_about_execution(self, alert_comment: str, event: BaseEvent) -> None:
        answer_text = f"[id{event.user.uuid}|Пользователь] | {alert_comment} \n"

        api = self._get_api()
        for bpid in get_log_peers():
            api.messages.send(
                peer_ids=bpid,
                random_id=0,
                message=answer_text,
            )

    def _get_api(self) -> Any:
        session = VkApi(
            token=config.VK_GROUP_TOKEN,
            api_version=config.VK_API_VERSION,
        )
        return session.get_api()
