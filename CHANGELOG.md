# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0).

---

## [2.3.0] - 2026-01-18

### Added

- `update_all_commands` method in MaxSender class.


## [2.2.0] - 2026-01-16

### Changed

- `Receiver` is generic class.
- `Receiver` constructor gets `webhook_data` arg.
- `parse_webhook` method doesn't bind processing funcs to the events, but just creates WebhookEvent object

### Added

- `process_webhook` method binds processing funcs to the events.

## [2.1.3] - 2026-01-07

- Readme updated.

## [2.1.2] - 2026-01-07

- Small changes.

## [2.1.1] - 2026-01-07

### Added

- GitHub workflow for auto-publishing to PyPI.

## [2.1.0] - 2026-01-07

### Added

- Constructor for the `MaxKeyboard` class.<br>
Now the max-keyboard could be created by passing arguments to the constructor: single button, list of buttons, list of lists of buttons.

### Removed

Deprecated functions:

- `send_text_message`
- `send_keyboard_message`
- `send_image_message`

Use `send_message` function instead.

## [2.0.0] - 2025-12-23

- Function for send message with attachments added.

## [1.1.0] - 2025-12-21

- Added decorators for for bot events

## [1.0.0] - 2025-12-18

- The basic functionality
