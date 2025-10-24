# Email Automation Design Document

## Overview

This document outlines the design for integrating Gmail OAuth 2.0 authentication into the existing email automation system. The design extends the current SMTP-based email settings with OAuth 2.0 support, providing users with secure Gmail access without requiring app passwords.

## Architecture

### High-Level Architecture

```
┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐
│   Email Settings    │    │   Email Service     │    │   Gmail Client      │
│      Dialog         │◄──►│                     │◄──►│   (OAuth 2.0)       │
└─────────────────────┘    └─────────────────────┘    └─────────────────────┘
           │                           │                           │
           │                           │                           │
           ▼                           ▼                           ▼
┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐
│   Configuration     │    │   SMTP Client       │    │   Gmail API         │
│     Storage         │    │   (Fallback)        │    │   (Primary)         │
└─────────────────────┘    └─────────────────────┘    └─────────────────────┘
```

### Component Integration

1. **EmailSettingsDialog** - Extended with OAuth 2.0 UI components
2. **EmailService** - Enhanced to support both SMTP and Gmail API
3. **GmailClient** - New OAuth 2.0 client for Gmail operations
4. **ConfigManager** - Stores authentication method preferences

## Components and Interfaces

### 1. Enhanced EmailSettingsDialog

#### New UI Components:
- **Authentication Method Selection**: Radio buttons for SMTP vs Gmail OAuth
- **Credentials File Selection**: File browser button for credentials.json
- **OAuth Status Display**: Shows authentication status and user email
- **Test Connection**: Enhanced to test both SMTP and Gmail connections

#### Interface Changes:
```python
class EmailSettingsDialog(QDialog):
    # New signals
    oauth_authentication_requested = Signal(str)  # credentials.json path
    oauth_test_requested = Signal()
    
    # New methods
    def _create_auth_method_group(self) -> QGroupBox
    def _create_gmail_oauth_group(self) -> QGroupBox
    def _on_credentials_browse_clicked(self)
    def _on_oauth_authenticate_clicked(self)
    def _update_oauth_status(self, status: dict)
```

### 2. Enhanced EmailService

#### New Capabilities:
- **Dual Authentication**: Support both SMTP and Gmail OAuth
- **Automatic Fallback**: Use SMTP if Gmail OAuth fails
- **Unified Interface**: Same methods work with both backends

#### Interface Extensions:
```python
class EmailService:
    # New properties
    self.gmail_client: Optional[GmailClient] = None
    self.auth_method: str = "smtp"  # "smtp" or "gmail_oauth"
    
    # Enhanced methods
    def authenticate_gmail_oauth(self, credentials_path: str) -> tuple[bool, str]
    def test_gmail_connection(self) -> dict
    def _determine_send_method(self) -> str
    def _send_via_gmail_api(self, to: str, subject: str, body: str) -> bool
    def _fetch_gmail_emails(self, max_results: int = 10) -> List[Dict]
```

### 3. GmailClient Integration

#### OAuth Flow Integration:
```python
class GmailOAuthManager:
    def __init__(self, parent_widget: QWidget)
    def start_oauth_flow(self, credentials_path: str) -> bool
    def handle_oauth_callback(self, authorization_code: str) -> bool
    def refresh_tokens_if_needed(self) -> bool
```

## Data Models

### Email Configuration Model

```python
@dataclass
class EmailConfig:
    # Authentication method
    auth_method: str = "smtp"  # "smtp" or "gmail_oauth"
    
    # SMTP Configuration
    smtp_server: str = ""
    port: int = 587
    use_tls: bool = True
    email_address: str = ""
    password: str = ""
    
    # Gmail OAuth Configuration
    credentials_path: str = ""
    token_path: str = ""
    oauth_email: str = ""
    oauth_authenticated: bool = False
    
    # Optional settings
    api_key: str = ""
```

### Gmail Email Model

```python
@dataclass
class GmailEmail:
    id: str
    thread_id: str
    subject: str
    sender: str
    recipient: str
    date: str
    body: str
    snippet: str
    unread: bool
    timestamp: str
    labels: List[str]
```

## Error Handling

### OAuth Error Categories

1. **Authentication Errors**:
   - Invalid credentials.json
   - OAuth flow cancellation
   - Token refresh failures

2. **API Errors**:
   - Rate limiting
   - Insufficient permissions
   - Network connectivity issues

3. **Configuration Errors**:
   - Missing credentials file
   - Invalid file format
   - Scope mismatches

### Error Handling Strategy

```python
class EmailErrorHandler:
    def handle_oauth_error(self, error: GmailAuthError) -> str:
        """Return user-friendly error message with solutions"""
        
    def handle_api_error(self, error: GmailAPIError) -> str:
        """Return actionable error message"""
        
    def suggest_troubleshooting(self, error_type: str) -> List[str]:
        """Return list of troubleshooting steps"""
```

## Testing Strategy

### Unit Tests

1. **GmailClient Tests**:
   - OAuth flow simulation
   - API operation mocking
   - Error condition handling

2. **EmailService Tests**:
   - Dual authentication modes
   - Fallback mechanisms
   - Configuration validation

3. **UI Component Tests**:
   - File selection dialog
   - OAuth status updates
   - Form validation

### Integration Tests

1. **End-to-End OAuth Flow**:
   - Complete authentication process
   - Token storage and retrieval
   - API access verification

2. **Email Operations**:
   - Fetch emails via Gmail API
   - Send emails via Gmail API
   - Mark emails as read

### Manual Testing Scenarios

1. **First-Time Setup**:
   - Select Gmail OAuth method
   - Browse for credentials.json
   - Complete OAuth flow
   - Test connection

2. **Token Refresh**:
   - Simulate expired tokens
   - Verify automatic refresh
   - Handle refresh failures

3. **Error Recovery**:
   - Invalid credentials file
   - Network connectivity issues
   - API quota exceeded

## Security Considerations

### Token Storage

- **Encryption**: Store OAuth tokens encrypted at rest
- **Secure Location**: Use OS-specific secure storage when available
- **Access Control**: Limit token file permissions

### Credential Handling

- **No Plaintext Storage**: Never store credentials.json content in config
- **Path Validation**: Validate credentials.json file integrity
- **Scope Limitation**: Use minimal required OAuth scopes

### Network Security

- **HTTPS Only**: All OAuth and API communications over HTTPS
- **Certificate Validation**: Verify SSL certificates
- **Timeout Handling**: Implement reasonable request timeouts

## Implementation Phases

### Phase 1: Core Gmail Integration
- Implement GmailClient class
- Add OAuth flow handling
- Create basic email operations

### Phase 2: UI Integration
- Extend EmailSettingsDialog
- Add authentication method selection
- Implement file browser for credentials

### Phase 3: Service Integration
- Enhance EmailService with Gmail support
- Implement dual authentication modes
- Add automatic fallback mechanisms

### Phase 4: Testing and Polish
- Comprehensive error handling
- User experience improvements
- Performance optimizations

## Configuration Storage

### Config File Structure

```json
{
  "email_config": {
    "auth_method": "gmail_oauth",
    "smtp_config": {
      "smtp_server": "smtp.gmail.com",
      "port": 587,
      "use_tls": true,
      "email_address": "user@gmail.com",
      "password": ""
    },
    "gmail_oauth_config": {
      "credentials_path": "/path/to/credentials.json",
      "token_path": "/path/to/token.json",
      "oauth_email": "user@gmail.com",
      "oauth_authenticated": true
    }
  }
}
```

### Migration Strategy

- **Backward Compatibility**: Existing SMTP configs remain functional
- **Gradual Migration**: Users can switch authentication methods
- **Config Validation**: Validate configurations on load

## Performance Considerations

### API Rate Limiting

- **Request Batching**: Batch multiple operations when possible
- **Exponential Backoff**: Implement retry logic with backoff
- **Quota Management**: Monitor and respect API quotas

### Caching Strategy

- **Email Metadata**: Cache email headers for quick access
- **Token Caching**: Cache valid tokens to avoid unnecessary refreshes
- **Configuration Caching**: Cache validated configurations

### Memory Management

- **Lazy Loading**: Load Gmail client only when needed
- **Resource Cleanup**: Properly dispose of API clients
- **Memory Monitoring**: Monitor memory usage during email operations

## Monitoring and Logging

### Logging Strategy

```python
# OAuth operations
logger.info("Starting Gmail OAuth flow")
logger.debug(f"Using credentials from: {credentials_path}")
logger.error(f"OAuth authentication failed: {error}")

# API operations
logger.info(f"Fetching {count} unread emails")
logger.warning(f"API rate limit approaching: {remaining_quota}")
logger.error(f"Gmail API error: {error_code} - {error_message}")
```

### Metrics Collection

- **Authentication Success Rate**: Track OAuth flow completion
- **API Response Times**: Monitor Gmail API performance
- **Error Frequencies**: Track common error patterns
- **User Adoption**: Monitor authentication method preferences