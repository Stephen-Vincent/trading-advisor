#!/usr/bin/env python3
"""
Development server runner for Trading Advisor Backend
"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "api.api:app",  # Changed from "api.main:app" to "api.api:app"
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["src", "api"],
        log_level="info"
    )