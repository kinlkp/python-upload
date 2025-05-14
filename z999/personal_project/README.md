# BBNext
Monitoring tool Big Brother next generation

The project is successor of Big Brother monitoring tool https://en.wikipedia.org/wiki/Big_Brother_(software) and the remembrance  of my career. The client will generate a json out and push the json to the REST API server. The stored statistics will be used to generate a performance dashboard.

Start command: docker run -d -e FLASK_RUNTIME_ENV='DEV' -p 5000:5000 docker-name

Ideal client JSON output:
```json
{
  "memory": [
    {
      "timestamp": "1685878369",
      "MemTotal": "16261028",
      "MemFree": "10243028",
      "MemAvailable": "12909036",
      "Cached": "2483124",
      "SwapTotal": "2097148",
      "SwapFree": "2097148"
    },
    {
      "timestamp": "1685878370",
      "MemTotal": "16261028",
      "MemFree": "10243028",
      "MemAvailable": "12909036",
      "Cached": "2483124",
      "SwapTotal": "2097148",
      "SwapFree": "2097148"
    },
    {
      "timestamp": "1685878371",
      "MemTotal": "16261028",
      "MemFree": "10243028",
      "MemAvailable": "12909036",
      "Cached": "2483124",
      "SwapTotal": "2097148",
      "SwapFree": "2097148"
    },
    ...
  ],
  "cpu": [
    {
      "timestamp": "1685878369",
      "CpuUsgae": "70"
    },
    {
      "timestamp": "1685878370",
      "CpuUsgae": "65"
    },
    {
      "timestamp": "1685878371",
      "CpuUsgae": "30"
    },
    ...
  ]
}
```
Sever side: TODO 
