# Health Check Endpoints

## Overview

The MyPacer API provides two health check endpoints for monitoring and orchestration tools.

## Endpoints

### `/health` - Liveness Probe

Basic health check to verify the API is running and responding.

**Response:**
```json
{
  "status": "healthy",
  "service": "mypacer-api"
}
```

**HTTP Status:** 200 OK

**Use cases:**
- Docker/Kubernetes liveness probes
- Load balancer health checks
- Uptime monitoring (UptimeRobot, Pingdom, etc.)
- CI/CD pipeline verification

### `/health/ready` - Readiness Probe

Advanced health check that verifies the API is ready to handle requests by checking database connectivity.

**Response (healthy):**
```json
{
  "status": "ready",
  "service": "mypacer-api",
  "database": "connected",
  "athletes_count": 150000
}
```

**HTTP Status:** 200 OK

**Response (unhealthy):**
```json
{
  "detail": "Service not ready: Database connection failed - ..."
}
```

**HTTP Status:** 503 Service Unavailable

**Use cases:**
- Kubernetes readiness probes
- Load balancer traffic routing decisions
- Pre-deployment verification
- Rolling updates (don't route until ready)

## Docker Healthcheck

The Dockerfile includes an automatic healthcheck:

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health').read()" || exit 1
```

**Parameters:**
- `interval`: Check every 30 seconds
- `timeout`: Fail if no response in 3 seconds
- `start-period`: Wait 40 seconds after container start before first check
- `retries`: Mark unhealthy after 3 consecutive failures

**View status:**
```bash
docker ps  # Shows (healthy) or (unhealthy) status
docker inspect --format='{{.State.Health.Status}}' mypacer-api
```

## Kubernetes Configuration

### Liveness Probe
```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 40
  periodSeconds: 30
  timeoutSeconds: 3
  failureThreshold: 3
```

### Readiness Probe
```yaml
readinessProbe:
  httpGet:
    path: /health/ready
    port: 8000
  initialDelaySeconds: 10
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 3
```

## Monitoring Integration

### Prometheus

```yaml
scrape_configs:
  - job_name: 'mypacer-api'
    metrics_path: '/health'
    static_configs:
      - targets: ['api.mypacer.fr:443']
    scheme: https
```

### UptimeRobot / Pingdom

- **URL:** `https://api.mypacer.fr/health`
- **Method:** GET
- **Expected:** HTTP 200
- **Check interval:** 5 minutes (or as needed)

### curl

```bash
# Simple check
curl https://api.mypacer.fr/health

# With verbose output
curl -v https://api.mypacer.fr/health

# Check readiness
curl https://api.mypacer.fr/health/ready

# Exit code (0 = healthy, non-zero = unhealthy)
curl -f https://api.mypacer.fr/health && echo "Healthy" || echo "Unhealthy"
```

## Troubleshooting

### Container shows (unhealthy)

1. Check logs:
   ```bash
   docker logs mypacer-api
   ```

2. Test endpoint manually:
   ```bash
   docker exec mypacer-api curl http://localhost:8000/health
   ```

3. Verify port is exposed:
   ```bash
   docker port mypacer-api
   ```

### /health/ready returns 503

Common causes:
- Database is down or unreachable
- Database credentials are incorrect
- Network connectivity issues
- Database is still initializing

**Check database:**
```bash
docker ps | grep postgres
docker logs mypacer-postgres
```

## Best Practices

1. **Use /health for liveness** - Simple, fast, no dependencies
2. **Use /health/ready for readiness** - Ensures DB is available
3. **Set appropriate timeouts** - 3-5 seconds is usually sufficient
4. **Don't check too frequently** - 30s interval is reasonable
5. **Allow startup time** - 40s start period for DB initialization
6. **Monitor both endpoints** - Different failure modes require different actions

## Integration with CI/CD

```bash
# Wait for API to be ready before running tests
until curl -f http://localhost:8000/health/ready; do
  echo "Waiting for API to be ready..."
  sleep 2
done

echo "API is ready, running tests..."
pytest tests/
```
