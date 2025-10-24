# Implementation Plan

## Overview

This implementation plan converts the Gmail OAuth 2.0 integration design into specific coding tasks. Each task builds incrementally on previous work, ensuring the email settings dialog supports both SMTP and Gmail OAuth authentication with proper file navigation for credentials.json selection.

## Tasks

### Phase 1: Core Gmail Integration Setup

- [x] 1. Set up Gmail OAuth dependencies and imports


  - Install required packages: google-auth, google-auth-oauthlib, google-api-python-client
  - Add import statements to EmailService and EmailSettingsDialog
  - Create error handling classes for Gmail operations
  - _Requirements: 11.1, 11.2_

- [x] 2. Enhance EmailService with Gmail OAuth support


  - Add gmail_client property and auth_method configuration to EmailService
  - Implement authenticate_gmail_oauth() method to initialize GmailClient
  - Add test_gmail_connection() method for connection validation
  - Create _determine_send_method() to choose between SMTP and Gmail API
  - _Requirements: 11.3, 11.4, 11.5_

- [x] 3. Implement dual email sending capability


  - Create _send_via_gmail_api() method in EmailService
  - Modify existing send_email_smtp() to support method selection
  - Add fallback logic from Gmail API to SMTP when needed
  - Implement proper error handling for both sending methods
  - _Requirements: 7.1, 7.2, 11.6_

### Phase 2: Email Settings Dialog UI Enhancement

- [x] 4. Add authentication method selection to EmailSettingsDialog


  - Create _create_auth_method_group() method with radio buttons for SMTP vs Gmail OAuth
  - Add auth_method_changed signal to handle selection changes
  - Implement _on_auth_method_changed() to show/hide relevant sections
  - Update dialog layout to accommodate new authentication options
  - _Requirements: 2.4, 2.5, 2.6_

- [x] 5. Create Gmail OAuth configuration section

  - Implement _create_gmail_oauth_group() method with OAuth-specific controls
  - Add credentials file path display and browse button
  - Create OAuth status label to show authentication state
  - Add "Authenticate with Google" button for OAuth flow initiation
  - _Requirements: 2.6, 11.1_

- [x] 6. Implement credentials.json file navigation

  - Create _on_credentials_browse_clicked() method with QFileDialog
  - Add file validation to ensure selected file is valid JSON
  - Implement _validate_credentials_file() to check Google OAuth format
  - Update UI to display selected credentials file path
  - _Requirements: 11.1, 11.2_

- [x] 7. Add OAuth authentication flow handling


  - Implement _on_oauth_authenticate_clicked() to start OAuth process
  - Create _handle_oauth_success() and _handle_oauth_error() callbacks
  - Add progress dialog for OAuth flow with cancel capability
  - Update OAuth status display based on authentication results
  - _Requirements: 11.2, 11.3_

### Phase 3: Enhanced Connection Testing

- [x] 8. Extend test connection functionality for Gmail OAuth





  - Modify _on_test_connection_clicked() to support both authentication methods
  - Create _test_gmail_oauth_connection() method for Gmail API testing
  - Add provider-specific success/error messages for Gmail OAuth
  - Implement _show_gmail_test_success() and _show_gmail_test_error() methods
  - _Requirements: 9.1, 9.2, 9.3, 9.4_

- [x] 9. Implement Gmail-specific error handling and user guidance





  - Create detailed error messages for OAuth authentication failures
  - Add troubleshooting suggestions for common Gmail OAuth issues
  - Implement _show_oauth_setup_help() with step-by-step Google Cloud setup
  - Add links to Google Cloud Console and Gmail API documentation
  - _Requirements: 9.5, 9.6, 11.8_

### Phase 4: Configuration Management

- [x] 10. Update configuration storage for dual authentication











  - Modify EmailService.save_email_config() to handle both auth methods
  - Add validation for Gmail OAuth configuration parameters
  - Implement secure token storage using OS-specific secure storage when available
  - Create configuration migration logic for existing SMTP-only configs
  - _Requirements: 2.7, 11.3, 11.4_

- [x] 11. Implement configuration loading and validation





  - Update EmailService._load_email_config() to support both authentication types
  - Add _validate_gmail_oauth_config() method for OAuth configuration validation
  - Implement automatic token refresh handling on configuration load
  - Create fallback logic when OAuth tokens are invalid or expired
  - _Requirements: 11.4, 11.8_

### Phase 5: Email Operations Integration

- [x] 12. Implement Gmail API email fetching





  - Create _fetch_gmail_emails() method in EmailService using GmailClient
  - Add email format conversion from Gmail API to internal email format
  - Implement proper error handling for Gmail API rate limits and quotas
  - Add caching mechanism for recently fetched emails
  - _Requirements: 11.5, 11.6_

- [x] 13. Integrate Gmail email operations with EmailAutomationTab





  - Modify EmailAutomationTab to support Gmail API email sources
  - Update _add_placeholder_emails() to use real Gmail emails when OAuth is configured
  - Implement _refresh_gmail_emails() method for manual email refresh
  - Add Gmail-specific email metadata display (labels, thread info)
  - _Requirements: 3.1, 3.2, 3.3, 11.5_

- [x] 14. Implement Gmail API email marking and management





  - Add mark_gmail_as_read() method to EmailService using GmailClient
  - Implement email labeling and organization features
  - Create batch operations for multiple email management
  - Add proper error handling for Gmail API modification operations
  - _Requirements: 11.7, 11.8_

### Phase 6: Error Handling and User Experience

- [x] 15. Implement comprehensive error handling for OAuth flows




  - Create GmailOAuthError exception class with specific error types
  - Add user-friendly error messages for common OAuth issues
  - Implement retry logic for transient OAuth and API errors
  - Create error recovery suggestions based on error type
  - _Requirements: 11.8, 9.4, 9.5_

- [x] 16. Add user experience improvements and visual feedback






  - Implement loading indicators for OAuth flow and API operations
  - Add success animations and confirmations for completed operations
  - Create tooltips and help text for Gmail OAuth configuration
  - Implement keyboard shortcuts for common email operations
  - _Requirements: 10.1, 10.2, 10.3_

### Phase 7: Testing and Validation

- [x] 17. Create unit tests for Gmail OAuth integration





  - Write tests for GmailClient OAuth flow simulation
  - Create mock Gmail API responses for testing email operations
  - Test EmailService dual authentication mode switching
  - Implement configuration validation and error handling tests
  - _Requirements: 11.1, 11.2, 11.3, 11.4_

- [x] 18. Implement integration tests for email automation workflow




  - Create end-to-end tests for complete OAuth authentication flow
  - Test email fetching, sending, and management operations via Gmail API
  - Validate fallback mechanisms from Gmail API to SMTP
  - Test configuration persistence and loading across application restarts
  - _Requirements: 7.1, 7.2, 11.5, 11.6, 11.7_

- [x] 19. Final integration testing and user acceptance validation























  - Test complete email automation workflow with Gmail OAuth
  - Validate AI-powered email generation works with Gmail API emails
  - Test error recovery and user guidance for common issues
  - Perform security validation of token storage and credential handling
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 6.4, 6.5_

## Implementation Notes

### Dependencies
- All tasks assume the GmailClient module is available in app/services/gmail_client.py
- Gmail API dependencies must be installed: google-auth, google-auth-oauthlib, google-api-python-client
- Tasks build incrementally - complete earlier tasks before proceeding to later ones

### Testing Strategy
- Each task should include basic unit tests for new functionality
- Integration tests should be added after completing related task groups
- Manual testing should be performed for OAuth flows and user interactions

### Security Considerations
- OAuth tokens should be stored securely using OS-specific secure storage
- Credentials.json files should never be stored in application configuration
- All Gmail API communications must use HTTPS with certificate validation

### Error Handling
- Each task should implement proper error handling with user-friendly messages
- Fallback mechanisms should be tested and validated
- Logging should be comprehensive for debugging OAuth and API issues