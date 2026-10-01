import time
from datetime import datetime

def get_timestamp_str():
    return datetime.now().strftime("%H:%M:%S")

def format_log_entry(state, message):
    return f"[{get_timestamp_str()}] [{state}]: {message}"

def format_diff_code():
    return """diff --git a/package.json b/package.json
index a1b2c3d..e5f6g7h 100644
--- a/package.json
+++ b/package.json
@@ -12,4 +12,4 @@
-    "express": "^4.17.1",
+    "express": "^5.0.0",
-    "axios": "^0.21.1"
+    "axios": "^1.7.2"
"""
