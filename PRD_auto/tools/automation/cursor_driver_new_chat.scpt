on run argv
	set promptText to item 1 of argv
	set waitSeconds to item 2 of argv as integer
	
	try
		-- Activate Cursor
		tell application "Cursor"
			activate
			delay 0.5
		end tell
		
		-- Open new chat in Cursor
		-- Method: Cmd+K opens command palette, then type "new chat" or use arrow keys
		tell application "System Events"
			tell process "Cursor"
				-- Open command palette (Cmd+K)
				keystroke "k" using command down
				delay 0.8
				
				-- Type "new chat" to find new chat option
				keystroke "new chat"
				delay 0.5
				
				-- Press Enter to select "New Chat"
				key code 36
				delay 1.5
				
				-- Alternative: If Cmd+K doesn't work, try Cmd+L then Cmd+Shift+N
				-- keystroke "l" using command down
				-- delay 0.5
				-- keystroke "n" using {command down, shift down}
				-- delay 1.5
				
				-- Paste the prompt
				set the clipboard to promptText
				keystroke "v" using command down
				delay 0.5
				
				-- Send (Enter key)
				key code 36
				delay waitSeconds
				
				-- Select all and copy transcript
				keystroke "a" using command down
				delay 0.3
				keystroke "c" using command down
				delay 0.3
			end tell
		end tell
		
		-- Get transcript from clipboard
		set transcriptText to the clipboard as string
		return transcriptText
		
	on error errMsg
		return "ERROR: " & errMsg
	end try
end run

