# Implementation Plan

- [ ] 1. Simplify theme manager to dark-mode only
  - Remove Theme.LIGHT enum value from theme_manager.py
  - Remove LIGHT_THEME color dictionary completely
  - Remove toggle_theme() method
  - Remove set_theme() method and theme switching logic
  - Simplify is_dark_mode() to always return True
  - Remove theme persistence logic from config_manager integration
  - Remove light mode conditional logic from all styling methods
  - _Requirements: 3.1, 3.2, 3.3, 4.1, 4.2, 4.3, 4.4, 4.5_

- [ ] 2. Remove theme toggle from main window View menu
  - Remove dark_mode_action from main_window.py
  - Remove _toggle_dark_mode() method
  - Remove theme toggle menu item from _create_menu_bar()
  - Remove theme-related event handlers and signals
  - Clean up theme manager initialization to not handle switching
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 5.1, 5.2, 5.3, 5.4, 5.5_

- [ ] 3. Update all dialogs to always use dark theme
  - Update email_settings_dialog.py to remove theme detection
  - Update compose_email_dialog.py to always apply dark theme
  - Update preferences_dialog.py to remove theme options
  - Update about_dialog.py to always use dark theme
  - Update model_parameters_dialog.py to always use dark theme
  - Update system_prompts_dialog.py to always use dark theme
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 3.1, 3.2, 3.3, 4.1, 4.2, 4.3, 4.4, 4.5_

- [ ] 4. Simplify theme mixin to dark-mode only
  - Update DialogThemeMixin in theme_mixin.py to remove theme detection
  - Remove conditional theme logic from all mixin methods
  - Always return dark theme styles from styling methods
  - Remove theme detection parameters from mixin methods
  - Optimize styling methods for dark mode only
  - _Requirements: 3.1, 3.2, 3.3, 4.1, 4.2, 4.3, 4.4, 4.5_

- [ ] 5. Clean up configuration and remove theme settings
  - Remove theme-related configuration keys from config handling
  - Remove theme persistence logic from application startup
  - Clean up any existing theme configuration in user settings
  - Remove theme-related command line arguments if any exist
  - Update configuration documentation to reflect dark-mode only
  - _Requirements: 3.1, 3.2, 3.3, 5.1, 5.2, 5.3, 5.4, 5.5_

- [ ] 6. Update all tab components to use consistent dark theme
  - Update chat_tab.py to always use dark theme styling
  - Update summarization_tab.py to always use dark theme styling
  - Update email_automation_tab.py to always use dark theme styling
  - Update bulk_email_marketing_tab.py to always use dark theme styling
  - Update social_media_marketing_tab.py to always use dark theme styling
  - Remove any theme detection or switching logic from tabs
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 4.1, 4.2, 4.3, 4.4, 4.5_

- [ ] 7. Remove light theme code and optimize dark theme styles
  - Remove all light theme color definitions and references
  - Optimize dark theme CSS for better performance
  - Remove conditional styling logic throughout the codebase
  - Enhance dark theme colors for better contrast and readability
  - Remove unused theme-related imports and dependencies
  - _Requirements: 3.1, 3.2, 3.3, 4.1, 4.2, 4.3, 4.4, 4.5_

- [ ] 8. Update application initialization to always use dark mode
  - Update main.py to remove theme-related startup logic
  - Update app_controller.py to always initialize with dark theme
  - Remove theme detection from application startup sequence
  - Ensure all UI components initialize with dark theme by default
  - Remove theme-related error handling from startup
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 3.1, 3.2, 3.3_

- [ ] 9. Create comprehensive testing for dark-mode only functionality
  - Write unit tests to verify theme manager always returns dark mode
  - Test that no light mode methods or properties exist
  - Test that all dialogs consistently apply dark theme
  - Test that View menu has no theme-related options
  - Create integration tests for dark-mode only application behavior
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 2.1, 2.2, 2.3, 2.4_

- [ ] 10. Final cleanup and documentation updates
  - Remove any remaining theme-related comments or documentation
  - Update code comments to reflect dark-mode only nature
  - Clean up any dead code related to light theme
  - Verify no theme switching functionality remains anywhere
  - Update any help text or tooltips that reference theme options
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_