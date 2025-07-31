from endstone.plugin import Plugin
from endstone.event import event_handler, PlayerJoinEvent
from endstone.form import ModalForm, Label
from endstone.command import Command, CommandSender
from endstone import Player
from enum import IntEnum
import string


class SafeFormatter(string.Formatter):
    def get_value(self, key, args, kwargs):
        return kwargs.get(key, f"<unknown:{key}>")


class MessageType(IntEnum):
    DISABLED = 0
    CHAT = 1
    TIP = 2
    POPUP = 3
    TOAST = 4
    TITLE = 5
    FORM = 6


class WelcomeMessage(Plugin):
    api_version = "0.6"

    commands = {
        "wmtest": {
            "description": "Tests welcome wessage. §gFor help: §3/wmtest help",
            "usages": [
                "/wmtest (help)[help: TestHelp]",
                "/wmtest (chat|tip|popup|toast|title|form)[type: TestType]"
            ],
            "permissions": ["welcome_message.command.wmtest"]
        },
        "wmset": {
            "description": "Sets welcome message options. §gFor help: §3/wmset help",
            "usages": [
                "/wmset (help)[help: SetHelp]",
                "/wmset (type)[typekey: SetTypeKey] (chat|tip|popup|toast|title|form)<typevalue: SetTypeValue>",
                "/wmset (header|body|button)[confkey: ConfKey] <confvalue: message>",
                "/wmset (wait)[wait: WaitKey] <seconds: int>"
            ],
            "permissions": ["welcome_message.command.wmset"]
        },
        "wmenable": {
            "description": "Enables the welcome message with the specified type. §gFor help: §3/wmenable help",
            "usages": [
                "/wmenable (help)[help: EnableHelp]",
                "/wmenable (chat|tip|popup|toast|title|form)<typevalue: EnableTypeValue>"
            ],
            "permissions": ["welcome_message.command.wmenable"]
        },
        "wmdisable": {
            "description": "Disables the welcome message. §gFor help: §3/wmdisable help",
            "usages": [
                "/wmdisable (help)[help: DisableHelp]",
                "/wmdisable"
            ],
            "permissions": ["welcome_message.command.wmdisable"]
        },
        "wmopts": {
            "description": "Prints the current options for the welcome message. §gFor help: §3/wmopts help",
            "usages": [
                "/wmopts (help)[help: OptsHelp]",
                "/wmopts"
            ],
            "permissions": ["welcome_message.command.wmopts"]
        }
    }

    permissions = {
        "welcome_message.command.wmtest": {
            "description": "Allow usage of /wmtest command",
            "default": "op"
        },
        "welcome_message.command.wmset": {
            "description": "Allow usage of /wmset command",
            "default": "op"
        },
        "welcome_message.command.wmenable": {
            "description": "Allow usage of /wmenable command",
            "default": "op"
        },
        "welcome_message.command.wmdisable": {
            "description": "Allow usage of /wmdisable command",
            "default": "op"
        },
        "welcome_message.command.wmopts": {
            "description": "Allow usage of /wmopts command",
            "default": "op"
        }
    }

    def on_enable(self) -> None:
        self.save_default_config()
        self.register_events(self)
        self._load_config()

    def _set_config(self, key, val):
        match key:
            case "type":
                val = MessageType[val.upper()].value
            case "body":
                val = val.replace("\\n", "\n")
            case "button":
                key = "form_button_text"
            case "wait":
                key = "wait_before"
                val = max(0, min(int(val), 5))

        self.config["welcome_message"][key] = val
        self.save_config()

    def _load_config(self):
        cfg = self.config["welcome_message"]
        self.msg_type = MessageType(max(0, min(int(cfg["type"]), 6)))
        self.msg_header = str(cfg["header"])
        self.msg_body = str(cfg["body"])
        self.btn_text = str(cfg["form_button_text"])
        self.wait_secs = max(0, min(int(cfg["wait_before"]), 5))

    @event_handler
    def on_player_join(self, event: PlayerJoinEvent):
        if self.msg_type == MessageType.DISABLED:
            return

        if self.wait_secs > 0:
            wait_ticks = self.wait_secs * 20
            task = self._task(event.player)
            self.server.scheduler.run_task(self, task, delay=wait_ticks)
        else:
            self._show_msg(event.player)

    def _task(self, p):
        def run():
            self._show_msg(p)
        return run

    def _show_msg(self, p, test_type = None):
        header, body = self._fill_placeholders(p)
        if test_type:
            msg_type = test_type
        else:
            msg_type = self.msg_type

        match msg_type:
            case MessageType.CHAT:
                p.send_message(body)
            case MessageType.TIP:
                p.send_tip(body)
            case MessageType.POPUP:
                p.send_popup(body)
            case MessageType.TOAST:
                p.send_toast(header, body)
            case MessageType.TITLE:
                p.send_title(header, body)
            case MessageType.FORM:
                form = ModalForm(
                    title=header,
                    controls=[Label(text=body + "\n")],
                    submit_button=self.btn_text
                )
                p.send_form(form)

    def _fill_placeholders(self, p):
        s = self.server

        values = {
            'player_name': p.name,
            'player_locale': p.locale,
            'player_device_os': p.device_os,
            'player_device_id': p.device_id,
            'player_hostname': p.address.hostname,
            'player_port': p.address.port,
            'player_game_mode': p.game_mode.name.capitalize(),
            'player_game_version': p.game_version,
            'player_exp_level': p.exp_level,
            'player_total_exp': p.total_exp,
            'player_exp_progress': f"{p.exp_progress:.2f}",
            'player_ping': p.ping,
            'player_dimension_name': p.location.dimension.type.name.replace("_", " ").title(),
            'player_dimension_id': p.location.dimension.type.value,
            'player_coordinate_x': int(p.location.x),
            'player_coordinate_y': int(p.location.y),
            'player_coordinate_z': int(p.location.z),
            'player_xuid': p.xuid,
            'player_uuid': p.unique_id,
            'player_health': p.health,
            'player_max_health': p.max_health,
            'server_level_name': s.level.name.replace("_", " ").title(),
            'server_max_players': s.max_players,
            'server_online_players': len(s.online_players),
            'server_start_time': s.start_time.strftime('%d %b %Y %H:%M:%S'),
            'server_locale': s.language.locale,
            'server_endstone_version': s.version,
            'server_minecraft_version': s.minecraft_version,
            'server_port': s.port,
            'server_port_v6': s.port_v6
        }

        formatter = SafeFormatter()
        header = formatter.format(self.msg_header, **values)
        body = formatter.format(self.msg_body, **values)

        return header, body

    def _print_config(self, p):
        conf = f"""§gWelcome Message options:§r
§3type:§r {MessageType(self.msg_type).name.lower()}§r
§3header:§r {self.msg_header}§r
§3body:§r {self.msg_body.replace("\n", "\\n")}§r
§3button:§r {self.btn_text}§r
§3wait:§r {self.wait_secs}"""
        p.send_message(conf)

    def on_command(self, sender: CommandSender, command: Command, args: list[str]) -> bool:
        if not isinstance(sender, Player):
            sender.send_error_message("Only players can use this command.")
            return False

        match command.name:
            case "wmtest":
                if len(args) == 0 or args[0] == "help":
                    sender.send_message("§gUsage: §3/wmtest chat|tip|popup|toast|title|form\n§gExample: §3/wmtest chat")
                else:
                    self._show_msg(sender, MessageType[args[0].upper()])

            case "wmset":
                if len(args) == 0 or args[0] == "help":
                    sender.send_message("§gUsage: §3/wmset type|header|body|button|wait <value>\n§gExamples:\n§3/wmset type title\n/wmset header Hello {player_name}\n/wmset body Welcome to our Server\\nYour ping is {player_ping}\n/wmset button Close\n/wmset wait 3")
                else:
                    self._set_config(args[0], args[1])
                    self._load_config()
                    self._print_config(sender)

            case "wmenable":
                if len(args) == 0 or args[0] == "help":
                    sender.send_message("§gUsage: §3/wmenable chat|tip|popup|toast|title|form\n§gExample: §3/wmenable chat")
                else:
                    self._set_config("type", args[0])
                    self._load_config()
                    sender.send_message("§gWelcome essage is §aenabled §gwith §3", args[0], "§gtype.")

            case "wmdisable":
                if len(args) == 0:
                    self._set_config("type", "disabled")
                    self._load_config()
                    sender.send_message("§gWelcome message §cdisabled§g.")
                elif args[0] == "help":
                    sender.send_message("§gUsage: §3/wmdisable")

            case "wmopts":
                if len(args) == 0:
                    self._print_config(sender)
                elif args[0] == "help":
                    sender.send_message("§gUsage: §3/wmopts")

        return True
