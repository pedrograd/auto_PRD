-- CURSOR_DRIVER.SCPT
-- ===================
-- AppleScript driver for interacting with Cursor IDE
--
-- PURPOSE:
-- This script automates AI interactions via Cursor's chat interface.
-- It activates Cursor, opens a new chat, pastes a prompt, sends it,
-- waits for the response, and copies the full transcript back.
--
-- USAGE:
--   osascript cursor_driver.scpt "<promptText>" "<waitSeconds>"
--
-- The script will:
--   1. Activate Cursor application
--   2. Open a new chat in the frontmost window
--   3. Paste the prompt text
--   4. Send the message
--   5. Wait for the AI response
--   6. Copy the full chat transcript to clipboard
--
-- REQUIREMENTS:
-- - Cursor must be installed and accessible
-- - macOS Accessibility permissions may be required for System Events
-- - User may need to customize keybindings if Cursor's shortcuts differ
--
-- CUSTOMIZATION:
-- If your Cursor setup uses different shortcuts, edit the USER CONFIG section below.

on run argv
    try
        -- Parse arguments
        if (count of argv) < 2 then
            error "Usage: osascript cursor_driver.scpt \"<promptText>\" \"<waitSeconds>\"" number 1
        end if
        
        set promptText to item 1 of argv
        set waitSecondsStr to item 2 of argv
        set waitSecs to waitSecondsStr as integer
        
        -- USER CONFIG: Customize these if your Cursor setup differs
        -- ============================================================
        -- New Chat shortcut: Try Cmd+Option+L or Cmd+K, Cmd+N, etc.
        -- If Cursor has a menu item, we'll try that first, then fall back to keyboard shortcut
        set newChatShortcut to {command down, option down, "l"}
        -- Alternative shortcuts to try (uncomment and modify if needed):
        -- set newChatShortcut to {command down, "k"}  -- Cmd+K then Cmd+N
        -- ============================================================
        
        -- Step 1: Activate Cursor
        tell application "Cursor"
            activate
        end tell
        
        -- Small delay to ensure Cursor is fully activated
        delay 0.5
        
        -- Step 2: Open a new chat
        -- Try menu item first (if available)
        try
            tell application "System Events"
                tell process "Cursor"
                    -- Try to find and click "New Chat" menu item
                    -- Common locations: File menu, Chat menu, or View menu
                    try
                        click menu item "New Chat" of menu "Chat" of menu bar 1
                    on error
                        try
                            click menu item "New Chat" of menu "File" of menu bar 1
                        on error
                            -- If menu item not found, use keyboard shortcut
                            keystroke "l" using {command down, option down}
                        end try
                    end try
                end tell
            end tell
        on error menuError
            -- Fallback: Use keyboard shortcut directly
            tell application "System Events"
                tell process "Cursor"
                    keystroke "l" using {command down, option down}
                end tell
            end tell
        end try
        
        -- Wait for new chat to open
        delay 1.0
        
        -- Step 3: Ensure chat input is focused
        -- After opening new chat, input should be focused, but we'll make sure
        tell application "System Events"
            tell process "Cursor"
                -- Click in the chat input area (this may vary by Cursor version)
                -- For now, assume it's already focused after opening new chat
            end tell
        end tell
        
        delay 0.3
        
        -- Step 4: Clear any existing input and paste the prompt
        tell application "System Events"
            tell process "Cursor"
                -- Select all existing text (if any)
                keystroke "a" using {command down}
                -- Clear it
                keystroke (ASCII character 8) -- backspace
                delay 0.2
                
                -- Set clipboard to prompt text
                set the clipboard to promptText
                delay 0.2
                
                -- Paste
                keystroke "v" using {command down}
                delay 0.3
            end tell
        end tell
        
        -- Step 5: Send the message (press Enter/Return)
        tell application "System Events"
            tell process "Cursor"
                key code 36 -- Return key
            end tell
        end tell
        
        -- Step 6: Wait for AI response
        -- Note: This is a fixed delay. Future improvements could:
        -- - Poll for "typing" indicator to disappear
        -- - Detect when response is complete
        -- - Use a more sophisticated completion detection
        delay waitSecs
        
        -- Step 7: Select all and copy the chat transcript
        tell application "System Events"
            tell process "Cursor"
                -- Select all content in the chat
                keystroke "a" using {command down}
                delay 0.2
                
                -- Copy to clipboard
                keystroke "c" using {command down}
                delay 0.3
            end tell
        end tell
        
        -- Step 8: Get transcript from clipboard
        -- The transcript will be available via pbpaste in Python
        -- We return success (exit code 0) by not raising an error
        
        return "SUCCESS"
        
    on error errorMessage number errorNumber
        -- Error handling: write to stderr and exit with error code
        try
            do shell script "echo " & quoted form of ("ERROR: " & errorMessage) & " >&2"
        end try
        error errorMessage number errorNumber
    end try
end run
