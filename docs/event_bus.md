# EventBus Documentation

## Overview

The EventBus is a core component of the GGUF Loader App that implements the publisher-subscriber pattern. It allows different components of the application to communicate without direct dependencies, promoting loose coupling and modular design.

## Features

- **Synchronous and Asynchronous Events**: Support for both immediate (synchronous) and background (asynchronous) event processing
- **Event Priorities**: Subscribers can specify priority levels to control the order of event handling
- **Wildcard Subscriptions**: Subscribe to multiple events using wildcard patterns (e.g., `model.*` to catch all model-related events)
- **Event Filtering**: Filter events based on their content before processing
- **Async Coroutine Support**: Native support for async/await coroutines as event handlers
- **Thread Safety**: Safe to use from multiple threads

## Usage Examples

### Basic Usage

```python
from app.core.event_bus import EventBus

# Create an event bus
event_bus = EventBus()

# Define a callback function
def on_model_loaded(model_id, model_name):
    print(f"Model loaded: {model_name} (ID: {model_id})")

# Subscribe to an event
subscriber_id = event_bus.subscribe("model.loaded", on_model_loaded)

# Publish an event
event_bus.publish("model.loaded", "model123", "GPT-2")

# Unsubscribe when no longer needed
event_bus.unsubscribe("model.loaded", subscriber_id)
```

### Using Event Priorities

```python
from app.core.event_bus import EventBus, EventPriority

event_bus = EventBus()

# High priority subscriber (called first)
event_bus.subscribe("app.shutdown", 
                   lambda: print("High priority shutdown task"), 
                   priority=EventPriority.HIGH)

# Normal priority subscriber (called second)
event_bus.subscribe("app.shutdown", 
                   lambda: print("Normal priority shutdown task"))

# Low priority subscriber (called last)
event_bus.subscribe("app.shutdown", 
                   lambda: print("Low priority shutdown task"), 
                   priority=EventPriority.LOW)

# Publish the event
event_bus.publish("app.shutdown")
```

### Wildcard Subscriptions

```python
from app.core.event_bus import EventBus

event_bus = EventBus()

# Subscribe to all model events
def on_model_event(event_type, model_id):
    print(f"Model event: {event_type} for model {model_id}")

event_bus.subscribe("model.*", on_model_event)

# These will all trigger the callback
event_bus.publish("model.loaded", "loaded", "model123")
event_bus.publish("model.unloaded", "unloaded", "model123")
event_bus.publish("model.error", "error", "model123")
```

### Event Filtering

```python
from app.core.event_bus import EventBus, EventFilter

event_bus = EventBus()

# Create a filter that only processes events for a specific model
def model_filter(event_name, args, kwargs):
    return len(args) > 0 and args[0] == "model123"

filter = EventFilter(model_filter)

# Subscribe with the filter
event_bus.subscribe("model.updated", 
                   lambda model_id, param: print(f"Model {model_id} updated: {param}"),
                   filter_=filter)

# This will trigger the callback
event_bus.publish("model.updated", "model123", "size")

# This will be filtered out
event_bus.publish("model.updated", "model456", "name")
```

### Async Coroutines

```python
import asyncio
from app.core.event_bus import EventBus

event_bus = EventBus()

# Define an async callback
async def process_model_async(model_id):
    print(f"Starting async processing of model {model_id}")
    await asyncio.sleep(1)  # Simulate async work
    print(f"Finished async processing of model {model_id}")

# Subscribe with the async callback
event_bus.subscribe("model.process", process_model_async, is_async=True)

# Publish the event
event_bus.publish("model.process", "model123")
```

### Waiting for Events

```python
from app.core.event_bus import EventBus

event_bus = EventBus()

# Create an event to wait for
event = event_bus.wait_for_event("model.ready", timeout=5.0)

# In another part of the code:
event_bus.publish("model.ready")

# Wait for the event to be published
if event.wait(timeout=5.0):
    print("Model is ready")
else:
    print("Timed out waiting for model")
```

## Standard Event Names

The GGUF Loader App uses a hierarchical naming convention for events:

- `app.*` - Application-level events
  - `app.start` - Application has started
  - `app.exit` - Application is exiting
  - `app.error` - Application error occurred

- `model.*` - Model-related events
  - `model.loading` - Model is being loaded
  - `model.loaded` - Model has been loaded
  - `model.unloaded` - Model has been unloaded
  - `model.error` - Error occurred with a model

- `ui.*` - UI-related events
  - `ui.theme_changed` - UI theme has changed
  - `ui.layout_changed` - UI layout has changed

- `addon.*` - Addon-related events
  - `addon.installed` - Addon has been installed
  - `addon.enabled` - Addon has been enabled
  - `addon.disabled` - Addon has been disabled
  - `addon.uninstalled` - Addon has been uninstalled
  - `addon.error` - Error occurred with an addon

- `config.*` - Configuration-related events
  - `config.changed` - Configuration has changed
  - `config.saved` - Configuration has been saved
  - `config.loaded` - Configuration has been loaded

## Best Practices

1. **Use Descriptive Event Names**: Use clear, hierarchical event names that describe the event's purpose.

2. **Keep Callbacks Small**: Event callbacks should be small and focused on a single responsibility.

3. **Handle Exceptions**: Always handle exceptions in event callbacks to prevent them from affecting other subscribers.

4. **Clean Up Subscriptions**: Unsubscribe from events when they are no longer needed to prevent memory leaks.

5. **Use Appropriate Priority**: Use event priorities to ensure events are processed in the correct order.

6. **Consider Performance**: Be mindful of the performance impact of event processing, especially for high-frequency events.

7. **Document Events**: Document the events your component publishes and subscribes to for better maintainability.