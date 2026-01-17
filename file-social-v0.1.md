# Take the Power Back — File Social Spec v0.1

**Status:** Draft (v0.1 locked)  
**Spec name:** `file-social`  
**Spec version:** `0.1`

---

## 1. Purpose

This document defines a minimal, durable, file-based specification for social interaction.

The goal is to enable social software that:
- requires no centralized infrastructure
- is chronological by default
- is manually connected
- is user-owned by construction

This spec defines data formats only.  
UI, sync transport, hosting, and business logic are explicitly out of scope.

---

## 2. Design Constraints (Non-Negotiable)

1. No ranking or recommendation algorithms are required or implied.
2. No centralized feed or discovery service is required.
3. Timelines MUST be derivable from timestamps and user-selected sources.
4. Connections/subscriptions MUST be manual and explicit.
5. Clients MUST be able to operate fully offline against local storage.
6. Global identity, virality, and growth mechanics are explicitly out of scope.

---

## 3. Terminology

- **User Folder**: A directory representing one identity.
- **Client**: Software that reads/writes files defined by this spec.
- **Entry**: A post.
- **Media**: Binary attachments referenced by entries.
- **MUST / SHOULD / MAY**: As defined in RFC 2119.

---

## 4. Storage Model

### 4.1 User Folder Layout

Each User Folder MUST contain:

- `profile.json`
- `posts/`
- `comments/`
- `media/`

Recommended structure:

```
users/
  <user_id>/
    profile.json
    posts/
    comments/
    media/
```

Clients MAY support alternate layouts but MUST support this structure.

---

## 5. File Encoding

- All JSON MUST be UTF-8 encoded.
- Strict JSON only (no comments, no trailing commas).
- Timestamps MUST be ISO-8601 UTC with `Z`.

Example:
```
2026-01-17T09:32:00Z
```

---

## 6. Common Envelope Fields

All JSON objects MUST include:

```json
{
  "spec": { "name": "file-social", "version": "0.1" },
  "type": "profile|post|comment",
  "id": "string",
  "created_at": "YYYY-MM-DDTHH:MM:SSZ"
}
```

Optional:
- `updated_at`
- `client`
- `extensions`

### 6.1 ID Rules

- IDs MUST be globally unique.
- IDs are opaque strings.
- Recommended formats: UUIDv4, ULID.

---

## 7. Profile (`profile.json`)

### 7.1 Location
`profile.json` MUST exist at the root of the User Folder.

### 7.2 Required Fields
- `display_name`
- `handle`

Rules:
- `handle` is a display label only.
- Handles are NOT globally unique.

### 7.3 Optional Fields
- `bio`
- `avatar` (MediaRef)
- `links`
- `public_keys` (reserved)

Example:

```json
{
  "spec": { "name": "file-social", "version": "0.1" },
  "type": "profile",
  "id": "user_01HXYZ",
  "created_at": "2026-01-01T00:00:00Z",
  "display_name": "Kevin",
  "handle": "kevin",
  "bio": "Optional.",
  "links": []
}
```

---

## 8. Posts

### 8.1 Storage
Each post MUST be stored as a single JSON file under `posts/`.

### 8.2 Filename Convention (Recommended)

```
<created_at_compact>__<id>.json
```

Clients MUST NOT rely on filenames for identity.

### 8.3 Required Fields
- `author_id` (MUST match owning profile id)
- `visibility`
- `content`

### 8.4 Optional Fields
- `attachments`
- `reply_to`
- `tags`

Example:

```json
{
  "spec": { "name": "file-social", "version": "0.1" },
  "type": "post",
  "id": "post_01HPOST",
  "created_at": "2026-01-17T09:32:00Z",
  "author_id": "user_01HXYZ",
  "visibility": "public",
  "content": { "text": "Hello world." },
  "attachments": []
}
```

---

## 9. Comments

### 9.1 Storage
Each comment MUST be stored under `comments/`.

### 9.2 Required Fields
- `author_id`
- `parent`
- `content`

Example:

```json
{
  "spec": { "name": "file-social", "version": "0.1" },
  "type": "comment",
  "id": "cmt_01HCMT",
  "created_at": "2026-01-17T09:40:00Z",
  "author_id": "user_01HOTHER",
  "parent": { "type": "post", "id": "post_01HPOST" },
  "content": { "text": "Reply." }
}
```

---

## 10. Media References

### 10.1 MediaRef Schema

A MediaRef MUST include:
- `media_id`
- `mime`
- exactly one of `path` or `url`

```json
{
  "media_id": "med_01HABC",
  "mime": "image/jpeg",
  "path": "media/med_01HABC.jpg",
  "url": "https://example.com/media.jpg",
  "width": 512,
  "height": 512
}
```

Rules:
- `path` MUST be relative.
- `url` MUST be absolute.
- Clients SHOULD cache external media.
- Clients MUST tolerate missing metadata.

---

## 11. Visibility

Allowed values:
- `public`
- `unlisted`
- `friends`
- `private`

Rules:
- `friends` means either-direction manual relationship.
- No global enforcement is defined.
- Clients SHOULD respect `private` content by default.

---

## 12. Feed Construction

Clients MUST construct timelines by:
1. Selecting User Folders manually.
2. Reading `posts/`.
3. Filtering by `visibility`.
4. Sorting by `created_at` descending.

No ranking or scoring is permitted by this spec.

---

## 13. Deletions and Edits

### 13.1 Edits
- Files MAY be rewritten.
- `created_at` MUST remain unchanged.
- `updated_at` SHOULD be set.

### 13.2 Deletions

Two deletion modes are supported:

**A) Physical deletion**  
**B) Tombstones**

Tombstone example:

```json
{
  "spec": { "name": "file-social", "version": "0.1" },
  "type": "post",
  "id": "post_01HPOST",
  "created_at": "2026-01-17T09:32:00Z",
  "updated_at": "2026-01-18T10:00:00Z",
  "deleted": true
}
```

Rules:
- Tombstones override live objects with the same `id`.
- Newer `updated_at` wins.

---

## 14. Conflict Handling

Clients SHOULD:
- Deduplicate by `id`
- Prefer latest `updated_at`
- Fall back to latest `created_at`
- Resolve ties deterministically

Conflicts MUST NOT block rendering.

---

## 15. Extensions

Objects MAY include:

```json
"extensions": {
  "com.example": {}
}
```

Rules:
- Extensions MUST NOT redefine required fields.
- Unknown extensions MUST be ignored.

---

## 16. Non-Goals

This spec intentionally does NOT define:
- discovery
- recommendations
- global identity
- ads
- engagement metrics
- monetization
- moderation policy

---

## 17. Compatibility

Clients MUST ignore unknown fields.
Clients SHOULD warn but not fail on newer spec versions.

---

## 18. Summary

This spec defines social interaction as files.
Chronology replaces algorithms.
Ownership replaces platforms.

Anything that requires central control is out of scope by design.
