# Troubleshooting Report: Facebook Integration Authentication Issues

## Issue Summary
The bot was intermittently failing to post to Facebook with an `OAuthException` (Error Code 190). The error messages evolved from "user has not authorized application" to "session invalidated because the user changed their password or security reasons."

## Root Causes Identified
1. **Token Expiration/Revocation:** Even though a "long-lived" token was used, Facebook's security systems periodically invalidate sessions (especially when running from different IP addresses like GitHub Actions). 
2. **Auth Session State:** The specific error code indicated that the session associated with the `FACEBOOK_LONG_LIVED_USER_ACCESS_TOKEN` had been revoked or invalidated by Facebook backend.

## Resolutions Applied

### Reliability Fixes (`wotdb/main.py`)
- Modified the `post_facebook` retry loop to raise a final `Exception` if all 10 attempts fail instead of silently returning `None`. This ensures that GitHub Actions correctly identifies failed runs as "failed" status rather than "pass."

## Final Resolution
The issue was resolved by manually re-authenticating through the [Graph API Explorer](https://developers.facebook.com/tools/explorer/) and generating a fresh set of access tokens in the `.env` file. This successfully established a new authorized session with Facebook's backend.

### Required Permissions
To successfully generate the token, ensure the following permissions are granted:
- `pages_manage_posts`
- `pages_show_list`
- `pages_read_engagement`

---
*Date: June 06, 2026*
