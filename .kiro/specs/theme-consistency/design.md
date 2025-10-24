# Theme Consistency Design Document

## Overview

This design document outlines the implementation of a comprehensive theme consistency system for the GGUF Loader application. The system will ensure that all UI elements properly adapt to light and dark modes, with particular focus on input fields, textboxes, and dialog backgrounds that currently have inconsistent theming.

## Architecture

### Theme Detection System
- **Automatic Detection**: Detect theme based on parent window's background color
- **Fallback Mechanism**: Default to light mode if detection fails
- **Dynamic Application**: Apply themes immediately when dialogs are created

### Centralized Styling System
- **Theme Manager Integration**: Extend existing theme_manager.py
- **CSS Style Generation**: Generate appropriate CSS for each theme mode
- **Component Coverage**: Handle all common UI elements consistently

## Components and Interfaces

### 1. Enhanced Theme Manager

**Location**: `app/ui/theme_manager.py`

**New Methods**:
```python
def get_dialog_theme_styles(self, is_dark_mode: bool) -> Dict[str, str]:
    """Return CSS styles for dialog elements based on theme mode"""
    
def detect_parent_theme(self, parent_widget) -> bool:
    """Detect if parent widget is using dark theme"""
    
def apply_dialog_theme(self, dialog: QDialog, parent_widget=None):
    """Apply appropriate theme to dialog based on parent"""
```

### 2. Dialog Theme Mixin

**Location**: `app/ui/mixins/theme_mixin.py` (new file)

**Purpose**: Provide common theming functionality for all dialogs

**Methods**:
```python
class DialogThemeMixin:
    def _apply_theme_to_dialog(self):
        """Apply theme to the current dialog"""
        
    def _get_input_field_styles(self, is_dark_mode: bool) -> str:
        """Get CSS styles for input fields"""
        
    def _get_button_styles(self, is_dark_mode: bool) -> str:
        """Get CSS styles for buttons"""
        
    def _get_group_box_styles(self, is_dark_mode: bool) -> str:
        """Get CSS styles for group boxes"""
```

### 3. Updated Email Settings Dialog

**Location**: `app/ui/email_settings_dialog.py`

**Changes**:
- Inherit from DialogThemeMixin
- Remove hardcoded theme detection
- Use centralized styling system
- Apply consistent theming to all elements

## Data Models

### Theme Style Configuration

```python
LIGHT_THEME_STYLES = {
    'input_fields': {
        'background': '#ffffff',
        'border': '#ced4da',
        'text': '#212529',
        'placeholder': '#6c757d',
        'focus_border': '#007bff'
    },
    'buttons': {
        'primary_bg': '#007bff',
        'primary_text': '#ffffff',
        'secondary_bg': '#6c757d',
        'secondary_text': '#ffffff'
    },
    'group_boxes': {
        'background': '#ffffff',
        'border': '#dee2e6',
        'title_color': '#495057'
    },
    'dialog': {
        'background': '#ffffff',
        'text': '#212529'
    }
}

DARK_THEME_STYLES = {
    'input_fields': {
        'background': '#1e1e1e',
        'border': '#404040',
        'text': '#ffffff',
        'placeholder': '#9ca3af',
        'focus_border': '#0078d4'
    },
    'buttons': {
        'primary_bg': '#0078d4',
        'primary_text': '#ffffff',
        'secondary_bg': '#404040',
        'secondary_text': '#ffffff'
    },
    'group_boxes': {
        'background': '#1e1e1e',
        'border': '#404040',
        'title_color': '#ffffff'
    },
    'dialog': {
        'background': '#1e1e1e',
        'text': '#ffffff'
    }
}
```

## Error Handling

### Theme Detection Failures
- **Fallback to Light Mode**: If parent theme detection fails
- **Logging**: Log theme detection issues for debugging
- **Graceful Degradation**: Ensure UI remains functional even with theme issues

### CSS Application Errors
- **Error Catching**: Catch and log CSS application errors
- **Partial Application**: Apply what styles are possible if some fail
- **User Notification**: Optionally notify user of theme issues

## Testing Strategy

### Unit Tests
- Test theme detection logic with various parent widget configurations
- Test CSS generation for both light and dark modes
- Test mixin functionality in isolation

### Integration Tests
- Test theme application across different dialogs
- Test theme switching scenarios
- Test parent-child theme inheritance

### Visual Tests
- Verify all input fields have correct backgrounds in both modes
- Verify text readability in both modes
- Verify button hover states work correctly
- Verify group box styling consistency

### Manual Testing Scenarios
1. **Light Mode Verification**:
   - Open Email Settings Dialog in light mode
   - Verify all textboxes have white/light backgrounds
   - Verify all text is dark and readable
   - Test input field focus states

2. **Dark Mode Verification**:
   - Open Email Settings Dialog in dark mode
   - Verify all textboxes have dark backgrounds
   - Verify all text is light and readable
   - Test input field focus states

3. **Theme Switching**:
   - Switch main application theme
   - Open dialogs and verify they match new theme
   - Test multiple dialogs simultaneously

## Implementation Phases

### Phase 1: Core Theme System
- Enhance theme_manager.py with dialog support
- Create DialogThemeMixin
- Implement theme detection logic

### Phase 2: Email Settings Dialog Update
- Integrate EmailSettingsDialog with new theme system
- Remove hardcoded styling
- Test theme consistency

### Phase 3: System-wide Application
- Apply theme system to other dialogs
- Update compose_email_dialog.py
- Update any other dialog components

### Phase 4: Testing and Refinement
- Comprehensive testing across all dialogs
- Performance optimization
- User feedback integration

## Performance Considerations

- **CSS Caching**: Cache generated CSS styles to avoid regeneration
- **Lazy Loading**: Only generate styles when needed
- **Minimal DOM Updates**: Apply styles efficiently to minimize UI updates

## Accessibility Considerations

- **Contrast Ratios**: Ensure text meets WCAG contrast requirements
- **Focus Indicators**: Maintain clear focus indicators in both themes
- **Color Independence**: Don't rely solely on color for information