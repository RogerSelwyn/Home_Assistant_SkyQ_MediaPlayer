# Key sequences

## Initialise sequence

```mermaid
sequenceDiagram
participant I as Integration
participant M as Module
participant J as 9006
I->>M:+ Initialise
M->>J: system/deviceinformation
M->>J: system/information
M->>J: system/time
M->>I: Combined system information
```

## Update sequence

```mermaid
sequenceDiagram
participant I as Integration
participant M as Module
participant J as 9006 JSON
participant W as 9006 Websocket
participant X as 49153 XML
participant S as 49153 SOAP
participant W as 9006 Websocket
participant E as EPG
opt
  I->>M: Initialise (1st time)
end
opt
  I->>M: Get channel list (1st time)
end
M->>J: services/{bouquet}/{subbouquet}
I->>M: Get power status
M->>J: system/information
alt powered on
  I->>M: Get current state
  opt 1st SOAP call
    M->>X: description{0-n}.xml
  end
  M->>S: GetTransportInfo
  I->>M: Get active application
  M->>W: apps/status
  alt Not application
    I->>M: Get current media
    M->>S: GetMediaInfo
    alt Live programme
      I->>M: Get current live TV
      opt Get EPG if required
        M->>E: Get EPG
      end
      opt Get live record status
        M->>J: pvr/?limit=1000&offset=0
      end
    else Recording
      I->>M: Get recording
      M->>S: pvr/details/{pvrid}
    end
  end
end
```

## Quota sequence

```mermaid
sequenceDiagram
participant I as Integration
participant M as Module
participant J as 9006 JSON
I->>M: Get quota
M->>J: pvr/storage
