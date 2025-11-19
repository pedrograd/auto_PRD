on run argv
	try
		set promptText to item 1 of argv as string
		set waitSeconds to (item 2 of argv) as integer
		
		-- Step 1: Ensure Cursor is running
		tell application "System Events"
			if not (exists process "Cursor") then
				return "ERROR: Cursor is not running. Please open Cursor first."
			end if
		end tell
		
		-- Step 2: Activate Cursor (bring to front, do NOT create new window)
		tell application "Cursor"
			activate
		end tell
		
		-- Wait for Cursor to be ready
		delay 1.0
		
		-- Step 3: Interact with Cursor window
		tell application "System Events"
			tell process "Cursor"
				-- Ensure Cursor window is frontmost
				set frontmost to true
				delay 0.5
				
				-- Step 4: Open new chat tab (Cmd+Shift+L or Cmd+K)
				-- Try Cmd+K first (common shortcut for AI chat in Cursor)
				try
					keystroke "k" using command down
					delay 1.5
				on error
					-- Fallback: try Cmd+Shift+L
					try
						keystroke "l" using {command down, shift down}
						delay 1.5
					end try
				end try
				
				-- Step 5: Ensure we're in the chat input area
				-- Click in chat area to ensure focus is in Cursor, not terminal
				try
					set mainWindow to window 1
					set windowBounds to bounds of mainWindow
					set windowWidth to (item 3 of windowBounds) - (item 1 of windowBounds)
					set windowHeight to (item 4 of windowBounds) - (item 2 of windowBounds)
					
					-- Click in chat input area (right side, bottom - typical chat position)
					set clickX to (item 1 of windowBounds) + (windowWidth * 0.75)
					set clickY to (item 2 of windowBounds) + (windowHeight * 0.85)
					
					click at {clickX, clickY}
					delay 0.5
				end try
				
				-- Step 6: Clear any existing text
				keystroke "a" using command down
				delay 0.2
				key code 51 -- Delete/Backspace
				delay 0.2
				
				-- Step 7: Set clipboard and paste prompt
				set the clipboard to promptText
				delay 0.3
				keystroke "v" using command down
				delay 0.5
				
				-- Step 8: Send message (Enter)
				key code 36 -- Enter/Return
			end tell
		end tell
		
		-- Step 9: Wait for AI response
		delay waitSeconds
		delay 5 -- Extra buffer for response completion
		
		-- Step 10: Copy chat transcript
		-- CRITICAL: Ensure we're still in Cursor, not terminal
		tell application "System Events"
			-- Make absolutely sure Cursor is frontmost
			tell process "Cursor"
				set frontmost to true
			end tell
			delay 0.5
			
			tell process "Cursor"
				-- Click in chat area to ensure focus is in Cursor
				try
					set mainWindow to window 1
					set windowBounds to bounds of mainWindow
					set windowWidth to (item 3 of windowBounds) - (item 1 of windowBounds)
					set windowHeight to (item 4 of windowBounds) - (item 2 of windowBounds)
					
					-- Click in chat history area (right side, middle)
					set clickX to (item 1 of windowBounds) + (windowWidth * 0.75)
					set clickY to (item 2 of windowBounds) + (windowHeight * 0.5)
					
					click at {clickX, clickY}
					delay 0.5
				end try
				
				-- Deselect input box
				key code 53 -- Escape
				delay 0.5
				
				-- Move focus to chat history (scroll up a bit)
				repeat 5 times
					key code 126 -- Up arrow
					delay 0.2
				end repeat
				
				-- Select all chat content
				keystroke "a" using command down
				delay 0.5
				
				-- Copy to clipboard
				keystroke "c" using command down
				delay 0.5
			end tell
		end tell
		
		-- Step 11: Get transcript from clipboard
		delay 0.5
		set transcriptText to (the clipboard as string)
		
		-- Validate transcript
		if length of transcriptText < 10 then
			return "ERROR: Transcript too short. May not have copied correctly."
		end if
		
		return transcriptText
		
	on error errMsg
		return "ERROR: " & (errMsg as string)
	end try
end run
