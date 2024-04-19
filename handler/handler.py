import requests
from vk_api import VkApiError
from logger import logger
from tools.keyboards import Keyboard, Callback, ButtonColor
from db import db
from .abc import ABCHandler


class PunishmentHandler(ABCHandler):
    banners = {
        1: "photo219135617_457239020",
        2: "photo219135617_457239021",
        3: "photo219135617_457239022",
        4: "photo219135617_457239023",
        5: "photo219135617_457239024",
        6: "photo219135617_457239025",
        7: "photo219135617_457239026",
        8: "photo219135617_457239027",
        9: "photo219135617_457239028",
        10: "photo219135617_457239029",
    }

    async def _handle(self, event: dict, kwargs) -> bool:
        if event.get("target_message_cmid"):
            await self._delete_msg(event)

        log_text = f"{event.get('author_name')}|id{event.get('author_id')}, punished {event.get('target_name')}|id{event.get('target_id')}. "
        setting = event.get("setting")

        if setting:
            log_text += f'By setting "{setting}".'
            warns = await self._get_warns(event)

        else:
            warns = event.get("warn_count")

        if warns == 0:
            log_text += "Punishment: message deleted. "
            await logger.info(log_text)
            return True

        current_warns = await self._get_current_warns(event)
        user_tag = await self._tag(event.get("target_name"), event.get("target_id"))
        message = f"⚠️ {user_tag}, {event.get('reason_message')}\n Получено предупреждений: {warns}"
        sum_warns = current_warns + warns if current_warns + warns <= 10 else 10
        await self._send_direct_alert(event, message, sum_warns)

        days_interval = 0
        if sum_warns <= 3:
            days_interval = await self._get_zone_interval(event, "green_zone")

        elif sum_warns <= 6:
            days_interval = await self._get_zone_interval(event, "yellow_zone")

        elif sum_warns <= 9:
            days_interval = await self._get_zone_interval(event, "red_zone")

        await self._update_warn_points(event, days_interval, sum_warns)
        if sum_warns == 10:
            log_text += "Punishment: kick. "
            # TODO: Kick user
        else:
            log_text += "Punishment: add warns. "

        await logger.info(log_text)
        return True

    async def _tag(self, user_name, user_id) -> int:
        return f"[id{user_id}|{user_name}]"

    async def _get_warns(self, event) -> int:
        result = db.execute.select(
            schema="toaster_settings",
            table="settings",
            fields=("warn_point",),
            conv_id=event.get("peer_id"),
            setting_name=event.get("setting"),
        )

        if result:
            return int(result[0][0])

        return 0

    async def _delete_msg(self, event) -> None:
        try:
            self.api.messages.delete(
                delete_for_all=1,
                peer_id=event.get("peer_id"),
                cmids=event.get("target_message_cmid"),
            )
        except VkApiError:
            ...

    async def _get_current_warns(self, event) -> int:
        result = db.execute.select(
            schema="toaster",
            table="warn_points",
            fields=("points",),
            conv_id=event.get("peer_id"),
            user_id=event.get("target_id"),
        )

        if result:
            return int(result[0][0])

        return 0

    async def _send_direct_alert(self, event, text, warns) -> None:
        photo = self.banners[warns]
        keyboard = (
            Keyboard(inline=True, one_time=False, owner_id=event.get("target_id"))
            .add_row()
            .add_button(
                Callback(label="Скрыть", payload={"call_action": "cancel_command"}),
                ButtonColor.PRIMARY,
            )
        )
        self.api.messages.send(
            peer_id=event.get("peer_id"),
            random_id=0,
            message=text,
            attachment=photo,
            keyboard=keyboard.json,
        )

    async def _get_zone_interval(self, event, zone_name) -> int:
        interval = db.execute.select(
            schema="toaster_settings",
            table="delay",
            fields=("delay",),
            conv_id=event.get("peer_id"),
            setting_name=zone_name,
        )

        return int(interval[0][0]) if interval else 0

    async def _update_warn_points(self, event, interval, points) -> None:
        query = f"""
        INSERT INTO 
            warn_points (conv_id, user_id, points, expire)
        VALUES 
            (
                '{event.get("peer_id")}',
                '{event.get("target_id")}',
                '{points}',
                NOW() + INTERVAL {interval} DAY
            )
        ON DUPLICATE KEY UPDATE
            points = '{points}',
            expire = NOW() + INTERVAL {interval} DAY;
        """
        db.execute.raw(schema="toaster", query=query)


punishment_executer = PunishmentHandler()
