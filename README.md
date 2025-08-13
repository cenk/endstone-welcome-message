# endstone-welcome-message

A simple plugin for **Endstone** that sends a welcome message to players when they join. The message can be shown in **chat**, **tip**, **popup**, **toast**, **title**, or **form** format.

## Message types
### 1 - Chat message:
![Chat](https://raw.githubusercontent.com/cenk/endstone-welcome-message/refs/heads/main/images/chat.png "Chat")

### 2 - Tip message:
![Tip](https://raw.githubusercontent.com/cenk/endstone-welcome-message/refs/heads/main/images/tip.png "Tip")

### 3 - Popup message:
![Popup](https://raw.githubusercontent.com/cenk/endstone-welcome-message/refs/heads/main/images/popup.png "Popup")

### 4 - Toast message:
![Toast](https://raw.githubusercontent.com/cenk/endstone-welcome-message/refs/heads/main/images/toast.png "Toast")

### 5 - Title message:
![Title](https://raw.githubusercontent.com/cenk/endstone-welcome-message/refs/heads/main/images/title.png "Title")

### 6 - Form message:
![Form](https://raw.githubusercontent.com/cenk/endstone-welcome-message/refs/heads/main/images/form.png "Form")

---

## Available Commands

All configuration is done via in-game commands:

### `/wmset <key> <value>`
Used to update specific configuration options for the welcome message.

- `/wmset type <value>`
    - Sets the message type.
    - Valid values: `chat`, `tip`, `popup`, `toast`, `title`, `form`
    - Example: `/wmset type title`

- `/wmset header <value>`
    - Sets the message header.
    - Supports placeholders and Minecraft color codes.
    - Only used for `toast`, `title`, and `form` types.
    - Example: `/wmset header Welcome {player_name}!`

- `/wmset body <value>`
    - Sets the message body.
    - Supports placeholders and Minecraft color codes.
    - Use `\n` for new lines.
    - Note that the Toast message type does not support new lines.
    - Example: `/wmset body Hi {player_name}\nWelcome to our server`

- `/wmset button <value>`
    - Sets the form button text.
    - Only used for form type.
    - Example: `/wmset button Close`

- `/wmset wait <0-5>`
    - Delays message for 0–5 seconds after player joins.
    - Example: `/wmset wait 2`

### `/wmopts`
Displays the current configuration for the welcome message.

- `/wmopts`

### `/wmtest [value]`
Used to manually preview the welcome message for testing before enabling it server-wide.

- `/wmtest`
    - Previews a test message using the currently active type.

- `/wmtest [value]`
    - Previews a test message using the specified type.
    - Valid values: `chat`, `tip`, `popup`, `toast`, `title`, `form`
    - Example: `/wmtest popup`

### `/wmenable` or `/wmon`
Enables the welcome message system with the current configuration options.

- `/wmenable` or `/wmon`

### `/wmdisable` or `/wmoff`
Disables the welcome message system.

- `/wmdisable` or `/wmoff`

---

## Installation
1. Download the latest `.whl` file from [GitHub Releases](https://github.com/cenk/endstone-welcome-message/releases) and place it into your `plugins/` folder.
2. Restart or reload the server.

---

### Placeholders
You can use the following placeholders in your welcome message. 
| Placeholder | Description |
| --- | --- |
| {player_name} | Player's name |
| {player_locale} | Player's current locale |
| {player_device_os} | Player's operation system |
| {player_device_id} | Player's current device id |
| {player_hostname} | Player's hostname |
| {player_port} | Player's port number |
| {player_game_mode} | Player's current game mode |
| {player_game_version} | Player's current game version |
| {player_exp_level} | Player's current experience level |
| {player_total_exp} | Player's total experience points |
| {player_exp_progress} | Player's current experience progress towards the next level |
| {player_ping} | Player's average ping |
| {player_dimension_name} | Player's current dimension name |
| {player_dimension_id} | Player's current dimension id |
| {player_coordinate_x} | Player's current x coordinate |
| {player_coordinate_y} | Player's current y coordinate |
| {player_coordinate_z} | Player's current z coordinate |
| {player_health} | Player's health |
| {player_max_health} | Player's max health |
| {player_xuid} | Player's XUID |
| {player_uuid} | Player's UUID |
| {server_level_name} | Server's level name |
| {server_max_players} | The maximum amount of player's which can login to this server |
| {server_online_players} | Current online players count |
| {server_start_time} | Start time of the server |
| {server_locale} | Server's current locale |
| {server_endstone_version} | Server's Endstone version |
| {server_minecraft_version} | Server's Minecraft version |
| {server_port} | Server's IPv4 port |
| {server_port_v6} | Server's IPv6 port |
