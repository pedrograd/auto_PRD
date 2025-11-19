on run argv
	if (count of argv) is less than 4 then
		error "Usage: cursor_driver.scpt <prompt_path> <output_path> <chat_strategy> <wait_seconds>"
	end if

	set promptPath to POSIX file (item 1 of argv)
	set transcriptPath to POSIX file (item 2 of argv)
	set chatStrategy to item 3 of argv
	set waitSeconds to item 4 of argv as integer

	set promptText to read promptPath

	tell application "Cursor"
		activate
	end tell

	delay 0.5

	tell application "System Events"
		tell process "Cursor"
			if chatStrategy is "multi_chat" then
				-- Open a fresh chat tab/window (Cursor specific shortcut placeholder: Cmd+Shift+N)
				keystroke "N" using {command down, shift down}
				delay 0.5
			else
				-- Reuse existing chat: ensure input box is focused and cleared
				keystroke "l" using {command down}
				delay 0.2
			end if

			set the clipboard to promptText
			delay 0.2
			keystroke "v" using {command down}
			delay 0.2
			key code 36 -- Return key
		end tell
	end tell

	delay waitSeconds

	tell application "System Events"
		tell process "Cursor"
			keystroke "a" using {command down}
			delay 0.2
			keystroke "c" using {command down}
			delay 0.2
		end tell
	end tell

	set transcriptText to the clipboard

	set transcriptFile to open for access transcriptPath with write permission
	try
		set eof transcriptFile to 0
		write transcriptText to transcriptFile
	ensure
		close access transcriptFile
	end try

	if chatStrategy is "multi_chat" then
		tell application "System Events"
			tell process "Cursor"
				keystroke "w" using {command down}
			end tell
		end tell
	end if
end run

